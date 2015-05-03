# -*- coding: utf-8 -*-
"""
Created on Sun May 03 13:49:16 2015

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
        
#Function for flattening result into array
def flatten(result):
    res = []
    for binthing in result:
        for thing in binthing['categorymembers']:
            res.append(thing)
    return res


#Recursive function for category and subcategory download
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
    return result
    
print 'Downloading category'        
category_list = downloadWikiCategory('Category:Star_Wars',dict())
print 'Finished Downloading category' 

fileObject = codecs.open('CategoryMapDataFull','w','utf-8-sig')
json.dump(category_list,fileObject)
fileObject.close()