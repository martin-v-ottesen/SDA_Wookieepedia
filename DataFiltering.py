# -*- coding: utf-8 -*-
"""
Created on Sun May 03 14:09:53 2015

@author: Tugsav
"""
#Imports
import urllib2
import json
import requests
import unicodedata
import codecs

#Load category data
fileObject = codecs.open('CategoryMapDataFull','r','utf-8-sig')
category_data = json.load(fileObject)
fileObject.close()

#Load page data
fileObject = codecs.open('PageDataFull','r','utf-8-sig')
page_data = json.load(fileObject)
fileObject.close()

#Filtering files out
def isFilePage(page):
    p=page['query']['pages']
    title = p[p.keys()[0]]['title']
    return 'File:' in title

#Test of function
print isFilePage(page_data['hasNoCanon'].values()[6])

#Filtering redirects out
def isRedirectPage(page):
    p=page['query']['pages'].values()[0]
    content = p['revisions'][0]['*']
    return '#REDIRECT' in content

#Disambiguation page filering
def isDisambiguationPage(page):
    p=page['query']['pages'].values()[0]
    content = p['revisions'][0]['*']
    return ('{{Disambig}}' in content) or ('{{disambig}}' in content)



#Searching for other stub page stuff
for key in page_data['hasNoCanon']:
    p=page_data['hasNoCanon'][key]['query']['pages'].values()[0]
    title = p['title']
    if isFilePage(page_data['hasNoCanon'][key]):
        continue
    if not 'revisions' in p.keys():
        print 'failing:    '+title
        continue
    if isRedirectPage(page_data['hasNoCanon'][key]) or isDisambiguationPage(page_data['hasNoCanon'][key]):     
        continue
    content = p['revisions'][0]['*']
    if len(content) < 100:
        print title

page_data['hasNoCanon']['File:Heroes']