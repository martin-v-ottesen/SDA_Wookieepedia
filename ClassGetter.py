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

def getFlatCategory(category_key,category_list,used_subs=[]):
    main_category = category_list[category_key]
    cat_items = []
    for item in main_category:
        if not(item['title'] in cat_items) and not(item['title'] in used_subs):          
            if 'Category:' in item['title']:
                used_subs.append( item['title'] )
                sub_res = getFlatCategory(item['title'],category_list,used_subs)
                cat_items += sub_res[0]
                used_subs += sub_res[1]
            else:
                cat_items.append(item['title'])
    print len(cat_items)
    return [cat_items,used_subs]
    
    
############################CANON
flatCanon = getFlatCategory('Category:Canon articles',categories)

fileObject = codecs.open('FlattenedCanon','w','utf-8-sig')
json.dump(flatCanon,fileObject)
fileObject.close()

##Removing the array from memory
flatCanon = 0

############################NON Canon
flatNonCanon = getFlatCategory('Category:Non-canon articles',categories)

fileObject = codecs.open('FlattenedNonCanon','w','utf-8-sig')
json.dump(flatNonCanon,fileObject)
fileObject.close()

##Removing the array from memory
flatNonCanon = 0

############################LEGENDS
flatLegends = getFlatCategory('Category:Legends articles',categories)

fileObject = codecs.open('FlattenedLegends','w','utf-8-sig')
json.dump(flatLegends,fileObject)
fileObject.close()

##Removing the array from memory
flatLegends = 0


Print 'Hurray for the lord of the flattening!!!'