# -*- coding: utf-8 -*-
"""
Created on Tue May 12 14:55:08 2015

@author: Tugsav
"""

import urllib2
import json
import requests
import unicodedata
import codecs
import re
import csv
import numpy as np

fileObject = codecs.open('CleanPageData(0-2500)','r','utf-8-sig')
data = json.load(fileObject)
fileObject.close()

fileObject = codecs.open('Vocabulary','r','utf-8-sig')
vocab = json.load(fileObject)
fileObject.close()

from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(min_df=1,token_pattern=r'\b\w[\w|\'|-]+\w\b')

X=vectorizer.fit_transform(vocab)
print 'Amount of words in final vocabulary: '+str(len(vectorizer.get_feature_names()))
vocab = vectorizer.get_feature_names()

print 'calculating Boolean BOW'
X = data['Canon'].values() + data['Legends'].values()
data=0
bow = np.int8(vectorizer.transform(X[:100]).toarray() > 0)
i=100
while(i<len(X)):
    if(i%1000==0):
        print 'You have reached: '+str(i)+' to '+str(i+100)
    i+=100
    if(i>=len(X)):
        bow = np.append(bow,np.int8(vectorizer.transform(X[i-100:]).toarray() > 0),0)
    else:
        bow = np.append(bow,np.int8(vectorizer.transform(X[i-100:i]).toarray() > 0),0)

print 'Summing'
sums = np.array(bow[0])
for i in range(1,len(X)):
    if i%1000 ==0:
        print 'You are at sum nr: '+str(i)
    sums += np.array(bow[i])

print 'Saving'
fileObject = codecs.open('BoolSums','w','utf-8-sig')
json.dump(sums,fileObject)
fileObject.close()

print min(sums)
print 'Done'
