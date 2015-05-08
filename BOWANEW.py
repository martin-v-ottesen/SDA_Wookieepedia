# -*- coding: utf-8 -*-
"""
Created on Thu May 07 10:18:58 2015

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


fileObject = codecs.open('cleanTestData','r','utf-8-sig')
clean = json.load(fileObject)
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
    VAD[word] = [float(row[2])-5,float(row[5])-5,float(row[8])-5]

#Get all words in the dict
def get_words(cleandict):
    resdict=dict()
    for key in cleandict:
        for word in cleandict[key].split(' '):
            resdict[word]=1
    return resdict.keys()

vocab = get_words(clean)            

##Setup Vectorizer
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(min_df=2)
##remove unwanted words from vocab

##Fit the vocabulary to vectorizer. Only these words (of length at least 2) will be in the array
X=vectorizer.fit_transform(vocab)

##Checking if append screws over the order of the array
#check = vectorizer.transform(clean.values()[:100]).toarray()
#x_bow = vectorizer.transform(clean.values()[:100]).toarray()
#x_bow = np.append(x_bow,vectorizer.transform(clean.values()[:100]).toarray(),0)

def checkTheSame(bow1,bow2):
    for j in range(0,len(bow1)):
        if bow1[j] != bow2[j]:
            return False
    return True
    
#for i in range(0,len(check)):
#    if not checkTheSame(check[i],x_bow[i]):
#        print 'Fail'
#    if not checkTheSame(check[i],x_bow[i+100]):
#        print 'Fail2'
##It does not :)    


###Get true X_BOW
x_bow = np.int16(vectorizer.transform(clean.values()[:100]).toarray())
i=100
while(i<len(clean.values())):
    print i    
    i+=100
    if(i>=len(clean.values())):
        x_bow = np.append(x_bow,np.int16(vectorizer.transform(clean.values()[i-100:]).toarray()),0)
    else:
        x_bow = np.append(x_bow,np.int16(vectorizer.transform(clean.values()[i-100:i]).toarray()),0)
        

###Search for very frequent words - method 1 (when stuf is very many times in the same article)
#maxi = []
#for line in x_bow:
#    maxi.append(max(line))

#maxval = max(maxi)
#words = dict()
#while maxval > 250:
#    maxval = max(maxi)
#    maxline = maxi.index(maxval)
#    wordindex = x_bow[maxline].tolist().index(maxval)
#    offendingword = vectorizer.get_feature_names()[wordindex]
#    words[offendingword]=1
#    x_bow[maxline][wordindex]=0    
#    maxi[maxline]=max(x_bow[maxline])
    
foundwords = [u'and', u'sith', u'would', u'force', u'br', u'starkiller', u'color', u'skywalker', u'jade', u'december', u'qel', u'horn', u'palpatine', u'as', u'loran', u'cade', u'in', u'miller', u'an', u'wicket', u'antilles', u'shesh', u'style', u'sidious', u'span', u'her', u'their', u'not', u'fel', u'had', u'jedi', u'by', u'jarael', u'to', u'droma', u'sup', u'vong', u'olin', u'td', u'shan', u'was', u'disambiguation', u'stele', u'2007', u'solo', u'from', u'his', u'star', u'that', u'iblis', u'thrawn', u'2005', u'wars', u'but', u'it', u'they', u'tenel', u'kenobi', u'be', u'on', u'with', u'him', u'is', u'he', u'carrick', u'utc', u'ka', u'yuuzhan', u'for', u'bel', u'vader', u'kneesaa', u'of', u'when', u'revan', u'2006', u'she', u'were', u'celchu', u'the', u'squadron', u'you', u'wraiths']

###Search for very frequent words - method 2 (when stuff is in the set more than the amount of pages)
#sums = []
#for line in np.transpose(x_bow):
#    sums.append(sum(line))

#words2 = []    
#for a_sum in sums:
#    if a_sum > len(x_bow):
#        words2.append(vectorizer.get_feature_names()[sums.index(a_sum)])
#print words2

foundwords = [u'an', u'and', u'as', u'at', u'be', u'but', u'by', u'color', u'for', u'from', u'had', u'he', u'his', u'in', u'is', u'it', u'jedi', u'not', u'of', u'on', u'republic', u'span', u'star', u'style', u'sup', u'talk', u'that', u'the', u'their', u'they', u'this', u'to', u'utc', u'wars', u'was', u'were', u'with']

###Search for very frequent words - method 3 (when a word is present in (allmost) all pages)
sums2 = []
for line in np.transpose(x_bow):
    sums2.append(sum(line==0))
    
words3 = []    
for a_sum in sums2:
    if a_sum > len(x_bow)-100:
        words3.append(vectorizer.get_feature_names()[sums2.index(a_sum)])
print words3    
    