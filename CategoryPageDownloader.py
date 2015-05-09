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
import os

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
def getCategoryPages(pages,category_dict,start,end,depth=0):         
    downloadedKeys = extractKnownKeys(pages)
    #count = start-1 
    fileObject = codecs.open('FullPageData(0-'+str(start -1)+')','w','utf-8-sig')
    fileObject.close()
    lastsave = start -1
    #checkdict = subdict(category_dict,start,end)
    for x in range(start,end):      
        #count+=1
        category = category_dict.keys()[x]       
        print 'Nr. '+str(x) +': '+ category + ' ...of size ' + str(len(category_dict[category]))
        Ghostlings = 0        
        for page_dict in category_dict[category]:
            page = page_dict['title']
            if not page in downloadedKeys:        
                if 'Category:' in page:
                    Ghostlings = Ghostlings + 1
                else:
                    downloadedKeys.append(page)
                    canonPage = getPage(getURL(page+'/Canon'))
                    if not isMissing(canonPage):
                        pages['Canon'][page]=canonPage
                        pages['nonCanon'][page]=getPage(getURL(page))
                    else:
                        pages['hasNoCanon'][page]=getPage(getURL(page))
            else:
                Ghostlings = Ghostlings + 1
        print 'Amount of Ghosting pages: '+str(Ghostlings)

        if Ghostlings < len(category_dict[category]):
            fileObject = codecs.open('FullPageData(0-'+str(x)+')','w','utf-8-sig')
            json.dump(page_data,fileObject)
            fileObject.close()
            os.remove('FullPageData(0-'+str(lastsave)+')')
            lastsave = x
        
    print len('is Done! congratulations')
    
    return True

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
#subdata = subdict(category_data,0,300)

#Either load the already downloaded page data or create an empty dict
fileObject = codecs.open('FullPageData(0-2590)','r','utf-8-sig')
page_data = json.load(fileObject)
fileObject.close()
#page_data = dict()

#Download the pages
#knownKeys=extractKnownKeys(page_data)
#page_data2 = getCategoryPages(subdata,knownKeys)
#page_data = mergeResults(page_data,page_data2)
getCategoryPages(page_data,category_data,2501,len(category_data)-1)

#Save the new combined pages
#fileObject = codecs.open('newPageData','w','utf-8-sig')
#json.dump(page_data,fileObject)
#fileObject.close()