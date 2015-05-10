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
#fileObject = codecs.open('CategoryMapDataFull','r','utf-8-sig')
#category_data = json.load(fileObject)
#fileObject.close()

#Load page data
#fileObject = codecs.open('PageDataMerge','r','utf-8-sig')
#page_data = json.load(fileObject)
#fileObject.close()

#Getting content of page
def getContent(page):
    p=page['query']['pages'].values()[0]
    return p['revisions'][0]['*']
   
#Getting a dict of the character box
def getBox(content):
    charCamps = re.sub(r'\{\{Campaign\n','{{Character\n',content)
    charLocs = re.sub(r'\{\{Location\n','{{Character\n',charCamps)
    charMoo = re.sub(r'\{\{MMO\n','{{Character\n',charLocs)
    charGames = re.sub(r'\{\{Video_game\n','{{Character\n',charMoo)
    charShips = re.sub(r'\{\{Starship_class\n','{{Character\n',charGames)
    charShips2 = re.sub(r'\{\{Individual_ship\n','{{Character\n',charShips)
    charBooks = re.sub(r'\{\{Book\n','{{Character\n',charShips2)
    safemess = re.sub(r'(\{\{Character\n[^\{}]*)\{\{([^\}]*)\}\}','\g<1>\g<2>',charBooks)
    mess = re.findall(r'\{\{Character\n[^\}\}]*\}\}',safemess)
    if len(mess)>0:
        mess=mess[0]
    else:
        return ['',safemess]
    linemess = re.findall(r'\n\|[^\n]*',mess)  
    linemess[-1] = re.sub(r'([^\}\}])\}\}*','\g<1>',linemess[-1])
    lines = dict()
    for line in linemess:   
        val = line.split('=')  
        if len(val)>1:
            val=val[1]
        else:
            continue
        if(val!=''):
            key = re.findall('\n\|([^=]*)=',line)[0]
            if(isAcceptedBoxLineKey(key)):
                lines[key]=val
    return [lines,safemess]
    
def isAcceptedBoxLineKey(key):
    way1 = key != 'image'
    way2 = key != 'isbn' 
    way3 = key != 'imageBG'
    way4 = key != 'max accel'
    way5 = key != 'max speed'
    way6 = key != 'length'
    return way1 and way2 and way3 and way4 and way5 and way6
   
def removeExTags(content):
    it1 = re.sub(r'<ref[^>]*>.*?</ref>','',content)
    it2 = re.sub(r'<div[^>]*>.*?</div>','',it1)
    it3 = re.sub(r'<div[^/>]*/>','',it2)    
    
    return re.sub(r'<ref[^/>]*/>','',it3)

def handlePicFiles(content):
    #For now just remove the entire file struct. May wanna extract picture text at some point
    return re.sub(r'\[\[File:[^\]\]]*\]\]','',content)

def unpackLinks(content):
    #content = removeExTags(content)
    subLongLinks = re.sub(r'\[\[[^\||\]]*\|([^\]\]]*)\]\]','\g<1>',content)
    return re.sub(r'\[\[([^\]\]]*)\]\]','\g<1>',subLongLinks)

#Filtering files out
def isFilePage(page):
    p=page['query']['pages']
    title = p[p.keys()[0]]['title']
    return 'File:' in title

#Test of function
# print isFilePage(page_data['hasNoCanon'].values()[6])

#Filtering card games out
def isCardGame(page):
    content = getContent(page)
    return '[[Category:Trading cards]]' in content


#Filtering redirects out
def isRedirectPage(page):
    content = getContent(page)
    way1 = ('#REDIRECT' in content)
    way2 = ('#redirect' in content)
    way3 = ('{{Softredirect|' in content)
    way4 = ('[[Category:Soft redirects]]' in content)
    return way1 or way2 or way3 or way4

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
    way3 = '{{Ship-stub}}' in content or '{{ship-stub}}' in content
    way4 = '{{Food-stub}}' in content or '{{food-stub}}' in content
    way5 = '{{Creature-stub}}' in content or '{{creature-stub}}' in content
    way6 = '{{City-stub}}' in content or '{{city-stub}}' in content
    way7 = '{{Book-stub}}' in content or '{{book-stub}}' in content
    return way1 or way2 or way3 or way4 or way5 or way6 or way7
    
def isTemplate(page):
    p=page['query']['pages']
    title = p[p.keys()[0]]['title']
    way1 = 'Template:' in title
    way2 = 'Template talk:' in title
    way3 = 'Module:' in title
    return way1 or way2 or way3
    
def isUser(page):
    p=page['query']['pages']
    title = p[p.keys()[0]]['title']
    way1 = 'User:' in title
    way2 = 'User talk:' in title
    way3 = 'Talk:' in title
    return way1 or way2 or way3
    
def isContest(page):
    p=page['query']['pages']
    title = p[p.keys()[0]]['title']
    way1 = 'Wookieepedia Contests talk:' in title
    way2 = 'Bracket:' in title
    way3 = 'Wookieepedia:' in title
    way4 = 'Forum:' in title
    way5 = 'Wookieepedia talk:' in title
    return way1 or way2 or way3 or way4 or way5
    
def isSoundtrack(page):
    content = getContent(page)
    return '[[Category:Soundtracks]]' in content
    
def removeScores(content):
    it1 = re.sub(r'[^\w\'-]*(\w+)[^\w\'-]*',' \g<1> ',content) 
    it2 = re.sub(r'(\w*) ([\'-]) (\w*)','\g<1>\g<2>\g<3>',it1)
    return re.sub(r'(\w*)\'s','\g<1>',it2)

def removeSingleWordNumbers(content):
    return re.sub(r'\b\d*\b','',content)
    
def removeHTTPLinks(content):
    return re.sub(r'\[http://[^\]]*\]','',content)

def removePictureGalleries(content):
    it1 = re.sub(r'\<Gallery[^<]*\</Gallery\>','',content)    
    return re.sub(r'\<gallery[^<]*\</gallery\>','',it1) 

def removeSubSecSyntaxAndBookEditions(content):
    it1 = re.sub(r'====*([^===]*)====*','\g<1>',content)
    it2 = re.sub(r'==Editions==[^=]*(==[^=]*==)','\g<1>',it1)
    it3 = re.sub(r'==Bibliography==[^=]*(==[^=]*==)','\g<1>',it2)
    return re.sub(r'=+([^=]*)=+','\g<1>',it3)

def removeTags(content):
    it1=content
    for i in range(0,10):    
        it1 = re.sub(r'\{\{[^{}]*\}\}','',it1)
    return it1

#Cleaning the content of unwanted symbols and syntaxing
def cleanContent(content):
    #removing external tags
    tempcontent = removeExTags(content) 
    #getting char box data out
    boxData=getBox(tempcontent)
    for key in boxData[0]:
        boxData[1] += ' '+boxData[0][key]
    
    #Removing tags
    iteration1 = removeTags(boxData[1])
    #Removing Boldface and italic   
    iteration2 = re.sub(r'\'\'\'*','',iteration1) 
    #Removing Category tags
    iteration3 = re.sub(r'\[\[Category:[^\]\]]*\]\]','',iteration2)
    #Remove subsection syntax
    iteration4 = removeSubSecSyntaxAndBookEditions(iteration3)
    #Remove picture structs
    iteration5 = handlePicFiles(iteration4)
    #Remove web links
    iteration6 = removeHTTPLinks(iteration5)
    #Unpack internal links
    iteration7 = unpackLinks(iteration6)
    #Remove file galleries
    iteration8 = removePictureGalleries(iteration7)    
    #Remove "Safe" symbols
    iteration9 = removeScores(iteration8)
    #Remove singlular numbers
    iteration10 = removeSingleWordNumbers(iteration9)
    #remove linespaces
    iteration11 = re.sub(r'\n',' ',iteration10)
    #remove multiple spaces
    iteration12 = re.sub(r' +',' ',iteration11)
    return iteration12.lower()



#Searching for other stub page stuff
#checkdict = page_data['hasNoCanon']
#count = 0
#for key in checkdict:
#    p=checkdict[key]['query']['pages'].values()[0]
#    title = p['title']
#    if isFilePage(checkdict[key]):
#        continue
#    if not 'revisions' in p.keys():
#        #print 'failing:    '+title
#        #print p
#        continue
#    if isRedirectPage(checkdict[key]):
#        continue
#    if isDisambiguationPage(checkdict[key]):     
#        continue
#    if isStubPage(checkdict[key]):
#        continue
#    if isTemplate(checkdict[key]):
#        continue
#    if isUser(checkdict[key]):
#        continue
#    if isContest(checkdict[key]):
#        continue   
#    content = p['revisions'][0]['*']    
#    if len(cleanContent(content)) < 50:
#        print title
#    count+=1
#print "Pages after filtering "+str(count)

def filterdata(inputdict):
    resdict=dict()    
    for key in inputdict:
        p=inputdict[key]['query']['pages'].values()[0]
        title = p['title']
        if isFilePage(inputdict[key]):
            continue
        if isTemplate(inputdict[key]):
            continue
        if isUser(inputdict[key]):
            continue
        if isContest(inputdict[key]):
            continue   
        if not 'revisions' in p.keys():
            #print 'failing:    '+title
            #print p
            continue   
        if isSoundtrack(inputdict[key]):
            continue        
        if isCardGame(inputdict[key]):
            continue
        if isRedirectPage(inputdict[key]):
            continue
        if isDisambiguationPage(inputdict[key]):     
            continue
        if isStubPage(inputdict[key]):
            continue
        
        resdict[key]=inputdict[key]
    return resdict
    
def cleanData(inputdict):
    resdict=dict()    
    for key in inputdict:
        resdict[key]=cleanContent(getContent(inputdict[key]))
    # print "Pages after filtering "+str(count)
    return resdict