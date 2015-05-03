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
    way1 = ('#REDIRECT' in content)
    way2 = ('#redirect' in content)
    return way1 or way2

#Disambiguation page filering
def isDisambiguationPage(page):
    p=page['query']['pages'].values()[0]
    content = p['revisions'][0]['*']
    way1 = ('{{Disambig}}' in content)
    way2 = ('{{disambig}}' in content)
    way3 = ('[[Category:Disambiguation pages]]' in content)
    return way1 or way2 or way3

def isStubPage(page):
    p=page['query']['pages'].values()[0]
    content = p['revisions'][0]['*']
    way1 = '{{stub}}' in content
    return way1

#Searching for other stub page stuff
for key in page_data['hasNoCanon']:
    p=page_data['hasNoCanon'][key]['query']['pages'].values()[0]
    title = p['title']
    if isFilePage(page_data['hasNoCanon'][key]):
        continue
    if not 'revisions' in p.keys():
        print 'failing:    '+title
        print p
        continue
    if isRedirectPage(page_data['hasNoCanon'][key]) or isDisambiguationPage(page_data['hasNoCanon'][key]):     
        continue
    content = p['revisions'][0]['*']
    if len(content) < 150:
        print title

page_data['hasNoCanon']['File:Heroes']