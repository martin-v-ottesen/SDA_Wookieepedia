# -*- coding: utf-8 -*-
"""
Created on Mon May 11 18:05:26 2015

@author: Tugsav
"""
import urllib2
import json
import requests
import unicodedata
import codecs
import re

fileObject = codecs.open('FlattenedCanon','r','utf-8-sig')
Canon_cat = json.load(fileObject)
fileObject.close()
fileObject = codecs.open('FlattenedLegends','r','utf-8-sig')
Legends_cat = json.load(fileObject)
fileObject.close()
fileObject = codecs.open('FlattenedNonCanon','r','utf-8-sig')
Non_Canon_cat = json.load(fileObject)
fileObject.close()

fileObject = codecs.open('CleanPageDataTest(0-2500)','r','utf-8-sig')
clean = json.load(fileObject)
fileObject.close()



CanonSorted = dict()
LegendSorted = dict()
nonCanonSorted = dict()

def sortDict(theDict):
    for key in theDict:
        if key in Canon_cat:
            CanonSorted[key] = theDict[key]
        if key in Non_Canon_cat:
            nonCanonSorted[key] = theDict[key]
        if key in Legends_cat:
            LegendSorted[key] = theDict[key]

sortDict(clean['Canon'])
sortDict(clean['nonCanon'])
sortDict(clean['hasNoCanon'])

result = dict()
result['Canon'] = CanonSorted
result['Legends'] = LegendSorted
result['nonCanon'] = nonCanonSorted

fileObject = codecs.open('SortedCleaned','w','utf-8-sig')
json.dump(result,fileObject)
fileObject.close()