# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 10:40:24 2015

@author: Tugsav
"""

import urllib2
import json
import requests    

##One way... no subcategories
#response = urllib2.urlopen('http://starwars.wikia.com/wiki/Special:Export/Category:Browse')
#html = response.read()
#import xmltodict
#o = xmltodict.parse(html)

#print o['mediawiki']['page'].keys()
#print o['mediawiki']['page']['revision'].keys()
#print o['mediawiki']['page']['revision']['text'].keys()
#print o['mediawiki']['page']['revision']['text']['#text']


##Second way - better. just like the old way. i discovered that there were a new type of endpoint
#http://starwars.wikia.com/api.php?format=json&action=query&titles=Main%20Page&prop=revisions&rvprop=content
response = urllib2.urlopen('http://starwars.wikia.com/api.php?format=json&action=query&titles=Anakin_Skywalker&prop=revisions&rvprop=content')
html = response.read()
j = json.loads(html)
##print j['query']['pages']['390551']['revisions'][0]['*']

debugar = []
def query(request):
    request['action'] = 'query'
    request['format'] = 'json'
    request['cmlimit'] = 'max'
    lastContinue = {'continue': ''}
    while True:
        req = request.copy()
        req.update(lastContinue)
        result = requests.get('http://starwars.wikia.com/api.php',params=req).json()
        debugar.append(result)
        if 'query' in result:        
            if 'categorymembers' in result['query']:
                print len(result['query']['categorymembers'])
        if 'query' in result: yield result['query']
        if 'continue' not in result:
            if 'query-continue' not in result:            
                break
            else:
                lastContinue = result['query-continue']['categorymembers']
        else:
            lastContinue = result['continue']

#content = []
#for result in query({'list':'categorymembers','cmtitle':'Category:Star_Wars'}):
#    content.append(result)

###Test of download of category
#content = []
#for result in query({'list':'categorymembers','cmtitle':'Category:Galactic_Republic_individuals'}):
#    content.append(result)
#resdict = []
#for binthing in content:
#    for thing in binthing['categorymembers']:
#        resdict.append(thing)

###Function for flattening result into array
def flatten(result):
    res = []
    for binthing in result:
        for thing in binthing['categorymembers']:
            res.append(thing)
    return res


###Recursive function for category and subcategory download
def downloadWikiCategory(name,oldresults):
    content = []
    for result in query({'list':'categorymembers','cmtitle':name}):
        content.append(result)
        
    flattened = flatten(content)
    
    result = oldresults
    result[name]=flattened
    for stuff in flattened:        
        if 'Category:' in stuff['title']:
            if not (stuff['title'] in result.keys()):           
                print stuff['title']
                subres = downloadWikiCategory(stuff['title'],result)
                result = dict(result,**subres)
#        else:
#            result[stuff['title']] = stuff['pageid']
    
    return result         

#print 'Downloading category'        
#test = downloadWikiCategory('Category:Star_Wars',dict())
#print 'Finished Downloading category' 

def getPage(name):
    response = urllib2.urlopen('http://starwars.wikia.com/api.php?format=json&action=query&titles='+name+'&prop=revisions&rvprop=content')
    html = response.read()
    j = json.loads(html)
    return j

def getPageById(id):
    response = urllib2.urlopen('http://starwars.wikia.com/api.php?format=json&action=query&pageids='+id+'&prop=revisions&rvprop=content')
    html = response.read()
    j = json.loads(html)
    return j

def isMissing(jsonPage):
    if 'missing' in jsonPage['query']['pages'].values()[0]:
        return True
    return False

def getURL(title):
    result = ''
    for char in title:
        if char == ' ':
            result=result+'_'
        else:
            result=result+char
    return codecs.encode(result,'utf8') ##Encoded to avoid weird char errors

def getCategoryPages(category_dict,downloadedkeys=[],depth=0):     
    canonPages = dict()
    nonCanonPages = dict()
    hasNoCanon = dict()
    print len(downloadedkeys)
    for category in category_dict:
        print category + ' of size ' + str(len(category_dict[category]))
        Ghostlings = 0        
        for page_dict in category_dict[category]:
            page = page_dict['title']
            if not page in downloadedkeys:        
                if 'Category:' in page:
                    Ghostlings = Ghostlings + 1
    #                print 'Now downloading '+page             
    #                subResult = getCategoryPages(category[page],downloadedkeys,depth+1)
    #                canonPages = dict(canonPages,**subResult['Canon'])
    #                nonCanonPages = dict(nonCanonPages,**subResult['nonCanon'])
    #                hasNoCanon = dict(hasNoCanon,**subResult['hasNoCanon'])
                else:
                    downloadedkeys.append(page)
                    canonPage = getPage(getURL(page+'/Canon'))
                    if not isMissing(canonPage):
                        canonPages[page]=canonPage
                        nonCanonPages[page]=getPage(getURL(page))
                    else:
                        hasNoCanon[page]=getPage(getURL(page))
            else:
                Ghostlings = Ghostlings + 1
        print 'Amount of Ghosting pages: '+str(Ghostlings)
    result = dict()
    result['Canon']=canonPages
    result['nonCanon']=nonCanonPages
    result['hasNoCanon']=hasNoCanon
    print len(downloadedkeys)
    return result

#test2 = getPagesWithCanon(test[1300:])
#print 'Downloading pages'
#test2 = getCategoryPages(test)

##Save dat shite
import unicodedata
import codecs
#fileObject = codecs.open('CategoryMapDataFull','w','utf-8-sig')
#json.dump(test,fileObject)
#fileObject.close()
#fileObject = codecs.open('PageDataFull','w','utf-8-sig')
#json.dump(test2,fileObject)
#fileObject.close()

##Load it again
fileObject = codecs.open('CategoryMapDataFull','r','utf-8-sig')
category_data = json.load(fileObject)
fileObject.close()

##Splitter function to get subset of the dict
def subdict(data,index_start,index_end):
    result = dict()
    maxcount = 0    
    for i in range(index_start,index_end+1):
        key = data.keys()[i]
        value = data[key]
        result[key]=value
        maxcount = maxcount + len(value)
    print maxcount
    return result
    

##Download pages
##Root category
#category_data['Category:Star_Wars']

subdata = subdict(category_data,0,300)
##Category 23 "Redirects from alternate spelling" includes SERIOUSLY weird chars
##and are useless pages anyway. Leave it aloooone
##Category 250 "Files without subject categorization" is also useless, large and contains funny symbols

#page_data = getCategoryPages(subdata)

def extractKnownKeys(data_dict):
    result = []
    for key in data_dict['nonCanon']:
        result.append(key)
    for key in data_dict['hasNoCanon']:
        result.append(key)
    return result

#fileObject = codecs.open('PageDataFull','w','utf-8-sig')
#json.dump(page_data,fileObject)
#fileObject.close()

##Load it again
fileObject = codecs.open('PageDataFull','r','utf-8-sig')
page_data = json.load(fileObject)
fileObject.close()

##Result merging function
def mergeResults(result1,result2):
    result = dict()    
    result['Canon'] = dict(result1['Canon'],**result2['Canon'])
    result['nonCanon'] = dict(result1['nonCanon'],**result2['nonCanon'])
    result['hasNoCanon'] = dict(result1['hasNoCanon'],**result2['hasNoCanon'])
    return result

##Download more pages
knownKeys=extractKnownKeys(page_data)
page_data2 = getCategoryPages(subdata,knownKeys)
page_data = mergeResults(page_data,page_data2)
#####Now rinse and repeat untill all pages have been downloaded (or attempt downloading all at once)

