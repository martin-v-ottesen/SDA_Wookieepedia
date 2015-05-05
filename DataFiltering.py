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
import re

#Load category data
fileObject = codecs.open('CategoryMapDataFull','r','utf-8-sig')
category_data = json.load(fileObject)
fileObject.close()

#Load page data
fileObject = codecs.open('PageDataFull','r','utf-8-sig')
page_data = json.load(fileObject)
fileObject.close()

#Getting content of page
def getContent(page):
    p=page['query']['pages'].values()[0]
    return p['revisions'][0]['*']
   
#Getting a dict of the character box
def getCharBox(content):
    mess = re.findall(r'\{\{Character\n[^\}\}]*\}\}',content)[0]
    linemess = re.findall(r'\n\|[^\n]*',mess)  
    linemess[-1] = re.sub(r'([^\}\}])\}\}*','\g<1>',linemess[-1])
    lines = dict()
    for line in linemess:
        val = line.split('=')[1]        
        if(val!=''):
            key = re.findall('\n\|([^=]*)=',line)[0]
            lines[key]=val
    return lines
   
def removeExTags(content):
    subLongRefs = re.sub(r'<ref[^>]*>[^<]*</ref>','',content)
    return re.sub(r'<ref[^/>]*/>','',subLongRefs)

def handlePicFiles(content):
    #For now just remove the entire file struct. May wanna extract picture text at some point
    return re.sub(r'\[\[File:[^\]\]]*\]\]','',content)

def unpackLinks(content):
    #content = removeExTags(content)
    subLongLinks = re.sub(r'\[\[[^\||\]]*\|([^\]\]]*)\]\]','\g<1>',content)
    return re.sub(r'\[\[([^\]\]]*)\]\]','\g<1>',subLongLinks)

#Cleaning the content of unwanted symbols and syntaxing
def cleanContent(content):
    #removing external tags
    tempcontent = removeExTags(content) 
    #getting char box data out
    tempdict=getCharBox(tempcontent)
    for key in tempdict:
        tempcontent += ' '+tempdict[key]
    #Removing tags
    iteration1 = re.sub(r'\{\{[^}]*\}\}','',tempcontent)
    #Removing Boldface syntax    
    iteration2 = re.sub(r'\'\'\'','',iteration1) 
    #Removing Italic syntax
    iteration3 = re.sub(r'\'\'','',iteration2)
    #Removing Category tags
    iteration4 = re.sub(r'\[\[Category:[^\]\]]*\]\]','',iteration3)
    #Remove subsection syntax
    iteration5 = re.sub(r'==([^==]*)==','\g<1>',iteration4)
    #Remove picture structs
    iteration6 = handlePicFiles(iteration5)
    #Unpack internal links
    iteration7 = unpackLinks(iteration6)
    #Remove "Safe" symbols
    iteration8 = re.sub(r'\*|"|&mdash;|,|:',' ',iteration7)
    #remove linespaces
    iteration9 = re.sub(r'\n',' ',iteration8)
    #remove multiple spaces
    iteration10 = re.sub(r' +',' ',iteration9)
    return iteration10

#Filtering files out
def isFilePage(page):
    p=page['query']['pages']
    title = p[p.keys()[0]]['title']
    return 'File:' in title

#Test of function
print isFilePage(page_data['hasNoCanon'].values()[6])

#Filtering redirects out
def isRedirectPage(page):
    content = getContent(page)
    way1 = ('#REDIRECT' in content)
    way2 = ('#redirect' in content)
    return way1 or way2

#Disambiguation page filering
def isDisambiguationPage(page):
    content = getContent(page)
    way1 = ('{{Disambig}}' in content)
    way2 = ('{{disambig}}' in content)
    way3 = ('[[Category:Disambiguation pages]]' in content)
    return way1 or way2 or way3

def isStubPage(page):
    content = getContent(page)
    way1 = '{{stub}}' in content
    way2 = '{{Stub}}' in content
    way3 = '{{Ship-stub}}' in content
    return way1 or way2 or way3

#Searching for other stub page stuff
checkdict = page_data['hasNoCanon']
count = 0
for key in checkdict:
    p=checkdict[key]['query']['pages'].values()[0]
    title = p['title']
    if isFilePage(checkdict[key]):
        continue
    if not 'revisions' in p.keys():
        print 'failing:    '+title
        print p
        continue
    if isRedirectPage(checkdict[key]):
        continue
    if isDisambiguationPage(checkdict[key]):     
        continue
    if isStubPage(checkdict[key]):
        continue
    content = p['revisions'][0]['*']
    if len(cleanContent(content)) < 100:
        print title
    count+=1
print "Pages after filtering "+str(count)