# -*- coding: utf-8 -*-
"""
Created on Sun May 03 13:53:31 2015

@author: Tugsav
"""

#Imports
import urllib2
import json
import requests
import unicodedata
import codecs

#Query function
def query(request):
    request['action'] = 'query'
    request['format'] = 'json'
    request['cmlimit'] = 'max'
    lastContinue = {'continue': ''}
    while True:
        req = request.copy()
        req.update(lastContinue)
        result = requests.get('http://starwars.wikia.com/api.php',params=req).json()
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

#Function for getting the pages of the category
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

#Splitter function to get subset of the dict
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

#Function extracting known keys from a data dictionary            
def extractKnownKeys(data_dict):
    result = []
    for key in data_dict['nonCanon']:
        result.append(key)
    for key in data_dict['hasNoCanon']:
        result.append(key)
    return result

#Result merging function   
def mergeResults(result1,result2):
    result = dict()    
    result['Canon'] = dict(result1['Canon'],**result2['Canon'])
    result['nonCanon'] = dict(result1['nonCanon'],**result2['nonCanon'])
    result['hasNoCanon'] = dict(result1['hasNoCanon'],**result2['hasNoCanon'])
    return result
    
    
#######Actual stuff happening...
###Requires a downloaded category list
#Load the category list
fileObject = codecs.open('CategoryMapDataFull','r','utf-8-sig')
category_data = json.load(fileObject)
fileObject.close()

#select a subset of the data to download (this function prints the amount of pages so try running it first)
subdata = subdict(category_data,0,300)

#Either load the already downloaded page data or create an empty dict
fileObject = codecs.open('PageDataFull','r','utf-8-sig')
page_data = json.load(fileObject)
fileObject.close()
#page_data = dict()

#Download the pages
knownKeys=extractKnownKeys(page_data)
page_data2 = getCategoryPages(subdata,knownKeys)
page_data = mergeResults(page_data,page_data2)

#Save the new combined pages
fileObject = codecs.open('PageDataFull','w','utf-8-sig')
json.dump(page_data,fileObject)
fileObject.close()