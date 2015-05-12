'''
Created on 10/05/2015

@author: Martin
'''

import urllib2
import json
import requests
import unicodedata
import codecs
import re
import DataFiltering

CanonSorted = dict()
LegendSorted = dict()
nonCanonSorted = dict()
OthersSorted = dict()

def sortDict(theDict):
    for key in theDict:
        if key in FlattenedCategories['Canon']:
            CanonSorted[key] = theDict[key]
        elif key in FlattenedCategories['nonCanon']:
            nonCanonSorted[key] = theDict[key]
        elif key in FlattenedCategories['Legends']:
            LegendSorted[key] = theDict[key]
        else:
            OthersSorted[key] = theDict[key]


print 'Loading File'
fileObject = codecs.open('FullPageDataDONE','r','utf-8-sig')
page_data = json.load(fileObject)
fileObject.close()

print 'Filtering Data'
filteredPages = dict()
filteredPages['Canon'] = DataFiltering.filterdata(page_data['Canon'])
filteredPages['nonCanon'] = DataFiltering.filterdata(page_data['nonCanon'])
filteredPages['hasNoCanon'] = DataFiltering.filterdata(page_data['hasNoCanon'])

print 'Saving Filtered Data'
fileObject = codecs.open('FilteredPageData','w','utf-8-sig')
json.dump(filteredPages,fileObject)
fileObject.close()

print 'Loading File Filtered Flattened Categories'
fileObject = codecs.open('FlattenedCategories','r','utf-8-sig')
FlattenedCategories = json.load(fileObject)
fileObject.close()

print 'Sorting Canon'
sortDict(filteredPages['Canon'])
print 'Sorting nonCanon'
sortDict(filteredPages['nonCanon'])
print 'Sorting hasNoCanon'
sortDict(filteredPages['hasNoCanon'])

SortedPages = dict()
SortedPages['Canon'] = CanonSorted
SortedPages['Legends'] = LegendSorted
SortedPages['nonCanon'] = nonCanonSorted
SortedPages['Others'] = OthersSorted

print 'Saving Sorted Data'
fileObject = codecs.open('SortedPageData','w','utf-8-sig')
json.dump(SortedPages,fileObject)
fileObject.close()

print 'Cleaning Data'
cleanPages = dict()
cleanPages['Canon'] = DataFiltering.cleanData(SortedPages['Canon'])
cleanPages['Legends'] = DataFiltering.cleanData(SortedPages['Legends'])
cleanPages['nonCanon'] = DataFiltering.cleanData(SortedPages['nonCanon'])
cleanPages['Others'] = DataFiltering.cleanData(SortedPages['Others'])

print 'Saving Clean Data'
fileObject = codecs.open('CleanPageData','w','utf-8-sig')
json.dump(cleanPages,fileObject)
fileObject.close()

print 'DONE!!!'