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
    lastContinue = {'continue': ''}
    while True:
        req = request.copy()
        req.update(lastContinue)
        result = requests.get('http://starwars.wikia.com/api.php',params=req).json()
        debugar.append(result)
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
def downloadWikiCategory(name):
    content = []
    for result in query({'list':'categorymembers','cmtitle':name}):
        content.append(result)
        
    res = flatten(content)
    
    subcats = []
    doombox = []
    for stuff in res:        
        if 'Category:' in stuff['title']:
            subcats.append(downloadWikiCategory(stuff['title']))
            doombox.append(stuff)
    print "Subcategories in "+name+": "+str(len(subcats))
    for result in subcats:
        res = res + result

    for destroyer in doombox:
        res.remove(destroyer)
    
    return res         
        
#test = downloadWikiCategory('Category:Years')

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
    return result

def getPagesWithCanon(category):
    canonPages = dict()
    nonCanonPages = dict()
    hasNoCanon = dict()
    for page in category:
        canonPage = getPage(getURL(page['title']+'/Canon'))
        if not isMissing(canonPage):
            canonPages[page['title']]=canonPage
            nonCanonPages[page['title']]=getPage(getURL(page['title']))
        else:
            hasNoCanon[page['title']]=getPage(getURL(page['title']))
    result = dict()
    result['Canon']=canonPages
    result['nonCanon']=nonCanonPages
    result['hasNoCanon']=hasNoCanon
    return result

test2 = getPagesWithCanon(test[1300:])