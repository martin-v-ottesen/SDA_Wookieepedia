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
import matplotlib.pyplot as plt

fileObject = codecs.open('CleanPageData(0-2500)','r','utf-8-sig')
data = json.load(fileObject)
fileObject.close()

##Setup VAD
data_array = []
with open('ANEW.csv','r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',',quotechar='|')
    for row in reader:
        data_array.append(row);
VAD = dict()
for row in data_array[1:]:
    word = row[1]
    VAD[word] = [float(row[2]),float(row[5]),float(row[8])]


print 'Getting words...'
vocab = VAD.keys()

from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(min_df=1,vocabulary = VAD.keys())

X=vectorizer.fit_transform(vocab)
print 'Amount of words in final vocabulary: '+str(len(vectorizer.get_feature_names()))

###Getting the x- and y-class
def getFold(foldnr, K, data):
    L = len(data)    
    return data[L/K*(foldnr-1):L/K*foldnr]

def getInvFold(foldnr, K, data):
    L = len(data)    
    return np.append(data[:L/K*(foldnr-1)] , data[L/K*foldnr:],0)

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
    if(i >= 8100):
        print 'OK SCREW IT THEN!!!'        
        break
    if(i>=len(data['Legends'].values())):
        bow_legends = np.append(bow_legends,np.int16(vectorizer.transform(data['Legends'].values()[i-100:]).toarray()),0)
    else:
        bow_legends = np.append(bow_legends,np.int16(vectorizer.transform(data['Legends'].values()[i-100:i]).toarray()),0)

Z=np.dot(bow_canon,(np.array(VAD.values())))
x_Canon_ANEW = np.transpose(np.transpose(Z)/(np.sum(bow_canon,1)+1))
bow_canon=0
Z=np.dot(bow_legends,(np.array(VAD.values())))
x_Legends_ANEW = np.transpose(np.transpose(Z)/(np.sum(bow_legends,1)+1))
bow_legends=0

##Minimum sample split array (len 20)
from sklearn import tree
n_mss = 100
mss_array = np.logspace(0,12,n_mss,base=2)
cls_array=[]
for i in range(0,n_mss):
    cls_array.append(tree.DecisionTreeClassifier(min_samples_split = mss_array[i]))
Test_Errors = []
for index in range(0,len(cls_array)):
    Training_Errors = []
    for j in range(1,11):
        LFoldCanon = len(getFold(j,10,x_Canon_ANEW))
        X_train = np.append( getInvFold(j,10,x_Canon_ANEW) , getInvFold(j,10,x_Legends_ANEW) ,0)
        X_test = np.append( getFold(j,10,x_Canon_ANEW) , getFold(j,10,x_Legends_ANEW), 0)
        LFoldLegends = len(X_test)-LFoldCanon
        LInvFoldCanon = len(x_Canon_ANEW) - LFoldCanon
        LInvFoldLegends = len(x_Legends_ANEW) - LFoldLegends
    
        Y_train = []
        for it in range(0,LInvFoldCanon):
            Y_train.append('Canon Page')
        for it in range(0,LInvFoldLegends):
            Y_train.append('Legends Page')
        
        Y_test = []
        for it in range(0,LFoldCanon):
            Y_test.append('Canon Page')
        for it in range(0,LFoldLegends):
            Y_test.append('Legends Page')
    
        ##### Decision Tree
        #print 'Fitting Tree to fold nr... '+str(j)
        treeCls = cls_array[index]        
        treeCls = treeCls.fit(X_train, Y_train)
    
        
        ####Deciding for stuff
        #print 'Predicting...'
        Predict_Y = treeCls.predict(X_test)
        Train_Error = 0
        for it in range(0,len(Predict_Y)):
            if not Predict_Y[it] == Y_test[it]:
                Train_Error += 1
        Train_Error = (0.0+Train_Error)/len(Predict_Y)
        Training_Errors.append(Train_Error)
        #print 'Training error for fold nr: '+str(j)+' =... '+str(Train_Error)
     
    Test_Errors.append([(0.0+sum(Training_Errors))/len(Training_Errors),mss_array[index]])
    print 'MSS: '+str(mss_array[index])
    print 'Test error for the decision tree: '+str((0.0+sum(Training_Errors))/len(Training_Errors))

plt.figure(figsize=16)
plotter = np.transpose(Test_Errors)
plt.plot(plotter[1],plotter[0])
plt.ylabel('Test Error')
plt.xlabel('Minimum Sample Split')

#print 'Saving BOW data for CANON'
#fileObject = codecs.open('BOW_CANON','w','utf-8-sig')
#json.dump(bow_canon.tolist(),fileObject)
#fileObject.close()

#print 'Saving BOW data for LEGENDS'
#fileObject = codecs.open('BOW_LEGENDS','w','utf-8-sig')
#json.dump(bow_legends.tolist(),fileObject)
#fileObject.close()
#print Predict_Y[:10]
#print data['nonCanon'].keys()[:10]
##I got "Lightsaber pike/Canon" predicted as Canon yay!!!