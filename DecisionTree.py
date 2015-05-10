# -*- coding: utf-8 -*-
"""
Created on Sun May 10 21:22:06 2015

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


fileObject = codecs.open('CleanPageDataTest(0-2500)','r','utf-8-sig')
clean = json.load(fileObject)
fileObject.close()

fileObject = codecs.open('FilteredPageDataTest(0-2500)','r','utf-8-sig')
filtered = json.load(fileObject)
fileObject.close()

def get_words(cleandict):
    resdict = dict()
    for thing in cleandict.values():
        for word in thing.split(' '):
            resdict[word]=1        
    return resdict.keys()
    
def get_words_array(cleanarray):
    resdict = dict()
    for thing in cleanarray:
        for word in thing.split(' '):
            resdict[word]=1        
    return resdict.keys()

print 'Getting words...'
vocab = get_words_array(clean['Canon'].values()+clean['nonCanon'].values())

from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(min_df=1,token_pattern=r'\w[\w|\'|-]+\w')

X=vectorizer.fit_transform(vocab)
print 'Amount of words in final vocabulary: '+str(len(vectorizer.get_feature_names()))


###Getting the x- and y-class
X = clean['Canon'].values()+clean['nonCanon'].values()#+clean['hasNoCanon'].values()
Y = []
for i in range(0,len(clean['Canon'])):
    Y.append('Canon Page')
for i in range(0,len(clean['nonCanon'])):
    Y.append('Non Canon Page')
#for i in range(0,len(clean['hasNoCanon'])):
#    Y.append('Page with no distinction')

###Get true X_BOW
x_bow = np.int16(vectorizer.transform(X[:100]).toarray())
i=100
while(i<len(X)):
    print 'Calculating BOW values up to: ' + str(i)   
    i+=100
    if(i>=len(X)):
        x_bow = np.append(x_bow,np.int16(vectorizer.transform(X[i-100:]).toarray()),0)
    else:
        x_bow = np.append(x_bow,np.int16(vectorizer.transform(X[i-100:i]).toarray()),0)

##### Decision Tree
print 'Fitting Tree...'
from sklearn import tree
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x_bow, Y)

#### BOW some stuff
X_predict = clean['hasNoCanon'].values()
x_predict = np.int16(vectorizer.transform(X_predict[:100]).toarray())
i=100
while(i<len(X_predict)):
    print 'Calculating BOW values up to: ' + str(i)   
    i+=100
    if(i>=len(X_predict)):
        x_predict = np.append(x_predict,np.int16(vectorizer.transform(X_predict[i-100:]).toarray()),0)
    else:
        x_predict = np.append(x_predict,np.int16(vectorizer.transform(X_predict[i-100:i]).toarray()),0)

####Deciding for stuff
print 'Predicting some stuff...'
Predict_Y = clf.predict(x_predict)

print Predict_Y[:10]
print clean['hasNoCanon'].keys()[:10]
##I got "Lightsaber pike/Canon" predicted as Canon yay!!!