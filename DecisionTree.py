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


fileObject = codecs.open('CleanPageData(0-2500)','r','utf-8-sig')
data = json.load(fileObject)
fileObject.close()

#fileObject = codecs.open('FilteredPageDataTest(0-2500)','r','utf-8-sig')
#filtered = json.load(fileObject)
#fileObject.close()

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
#vocab = get_words_array(data['Canon'].values()+data['Legends'].values())
fileObject = codecs.open('newVocabulary','r','utf-8-sig')
vocab = json.load(fileObject)
fileObject.close()

from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(min_df=1,token_pattern=r'\b\w[\w|\'|-]+\w\b')

X=vectorizer.fit_transform(vocab)
print 'Amount of words in final vocabulary: '+str(len(vectorizer.get_feature_names()))
vocab = vectorizer.get_feature_names()

###Getting the x- and y-class
def getFold(foldnr, K, data):
    L = len(data)    
    return data[L/K*foldnr*foldnr-1:L/K*foldnr*foldnr]

def getInvFold(foldnr, K, data):
    L = len(data)    
    return np.append(data[:L/K*foldnr*foldnr-1] , data[L/K*foldnr*foldnr:],0)

print 'Calculating Canon BOW values'        
bow_canon = np.int16(vectorizer.transform(data['Canon'].values()[:100]).toarray())
i=100
while(i<len(data['Canon'].values())):
    i+=100
    if(i>=len(data['Canon'].values())):
        bow_canon = np.append(bow_canon,np.int16(vectorizer.transform(data['Canon'].values()[i-100:]).toarray()),0)
    else:
        bow_canon = np.append(bow_canon,np.int16(vectorizer.transform(data['Canon'].values()[i-100:i]).toarray()),0)

print 'Calculating Legends BOW values'        
bow_legends = np.int16(vectorizer.transform(data['Legends'].values()[:100]).toarray())
i=100
while(i<len(data['Legends'].values())):
    i+=100
    if(i>=len(data['Legends'].values())):
        bow_legends = np.append(bow_legends,np.int16(vectorizer.transform(data['Legends'].values()[i-100:]).toarray()),0)
    else:
        bow_legends = np.append(bow_legends,np.int16(vectorizer.transform(data['Legends'].values()[i-100:i]).toarray()),0)

Training_Errors = []
from sklearn import tree
for j in range(1,11):
    LFoldCanon = len(getFold(j,10,bow_canon))
    X_train = np.append( getInvFold(j,10,bow_canon) , getInvFold(j,10,bow_legends) ,0)
    X_test = np.append( getFold(j,10,bow_canon) , getFold(j,10,bow_legends), 0)
    LFoldLegends = len(X_test)-LFoldCanon
    LInvFoldCanon = len(bow_canon) - LFoldCanon
    LInvFoldLegends = len(bow_legends) - LFoldLegends

    Y_train = []
    for it in range(0,LInvFoldCanon):
        Y_train.append('Canon Page')
    for it in range(0,LInvFoldLegends):
        Y_train.append('Legends Page')
    
    Y_test = []
    for it in range(0,LFoldCanon):
        Y_train.append('Canon Page')
    for it in range(0,LFoldLegends):
        Y_train.append('Legends Page')

    ##### Decision Tree
    print 'Fitting Tree to fold nr... '+str(j)
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X_train, Y_train)

    
    ####Deciding for stuff
    print 'Predicting...'
    Predict_Y = clf.predict(X_test)
    Train_Error = 0
    for it in range(0,len(Predict_Y)):
        if not Predict_Y[it] == Y_test[it]:
            Train_Error += 1
    Train_Error = Train_Error/len(Predict_Y)
    Training_Errors.append(Train_Error)
    print 'Training error for fold nr: '+str(j)+' =... '+Train_Error
 

print 'Test error for the decision tree: '+str(sum(Training_Errors)/len(Training_Errors))

#print Predict_Y[:10]
#print data['nonCanon'].keys()[:10]
##I got "Lightsaber pike/Canon" predicted as Canon yay!!!