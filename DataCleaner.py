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

print 'Loading File'
fileObject = codecs.open('FullPageData(0-2500)','r','utf-8-sig')
page_data = json.load(fileObject)
fileObject.close()

print 'Filtering Data'
filteredPages = dict()
filteredPages['Canon'] = DataFiltering.filterdata(page_data['Canon'])
filteredPages['nonCanon'] = DataFiltering.filterdata(page_data['nonCanon'])
filteredPages['hasNoCanon'] = DataFiltering.filterdata(page_data['hasNoCanon'])

print 'Saving Filtered Data'
fileObject = codecs.open('FilteredPageDataTest(0-2500)','w','utf-8-sig')
json.dump(filteredPages,fileObject)
fileObject.close()

print 'Cleaning Data'
cleanPages = dict()
cleanPages['Canon'] = DataFiltering.cleanData(filteredPages['Canon'])
cleanPages['nonCanon'] = DataFiltering.cleanData(filteredPages['nonCanon'])
cleanPages['hasNoCanon'] = DataFiltering.cleanData(filteredPages['hasNoCanon'])

print 'Saving Clean Data'
fileObject = codecs.open('CleanPageDataTest(0-2500)','w','utf-8-sig')
json.dump(cleanPages,fileObject)
fileObject.close()

print 'DONE!!!'