# -*- coding: utf-8 -*-
"""
Created on Mon May 11 09:02:10 2015

@author: Tugsav
"""
import urllib2
import json
import requests
import unicodedata
import codecs
import re

fileObject = codecs.open('CategoryMapDataFull','r','utf-8-sig')
categories = json.load(fileObject)
fileObject.close()


cat_items = []
used_subs=[]
def getFlatCategory(category_key):
    main_category = categories[category_key]
    
    for item in main_category:
        if not(item['title'] in cat_items) and not(item['title'] in used_subs):
            if 'Category:' in item['title']:
                used_subs.append( item['title'] )
                getFlatCategory(item['title'])
            else:
                cat_items.append(item['title'])
    print len(cat_items)
    
    
############################CANON
getFlatCategory('Category:Canon articles')

fileObject = codecs.open('FlattenedCanon','w','utf-8-sig')
json.dump(cat_items,fileObject)
fileObject.close()

##Removing the array from memory
cat_items = []
used_subs=[]

############################NON Canon
getFlatCategory('Category:Non-canon articles')

fileObject = codecs.open('FlattenedNonCanon','w','utf-8-sig')
json.dump(cat_items,fileObject)
fileObject.close()

##Removing the array from memory
cat_items = []
used_subs=[]

############################LEGENDS
getFlatCategory('Category:Legends articles')

fileObject = codecs.open('FlattenedLegends','w','utf-8-sig')
json.dump(cat_items,fileObject)
fileObject.close()

##Removing the array from memory
cat_items = []
used_subs=[]


print 'Hurray for the lord of the flattening!!!'