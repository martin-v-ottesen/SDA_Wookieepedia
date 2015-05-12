'''
Created on 08/05/2015

@author: Kevin
'''
import json
import codecs
import DataFiltering
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import re


# Load Vocab
with codecs.open('newVocabulary', 'r', 'utf-8-sig') as vocabFile:
    vocab = json.load(vocabFile)


# --- Load data ---
with codecs.open('CleanPageData(0-2500)', 'r', 'utf-8-sig') as dataFile:
    data = json.load(dataFile)

def getBagOfWords(txt):
    bow = []
    
    for v in vocab:
        count = 0
        for word in txt.split(' '):
            if word == v:
                count+=1
                
        bow.append(count)
    return bow

def train_classifier(clf):
    with open('train_data.json', 'r') as outfile:
        trainData = json.load(outfile)
    
    X = []
    y = []
    
    for cat in trainData.keys():
        for bw in trainData[cat]:
            X.append(bw)
            
    for i in range(0,100):
        y.append('Canon')
        
    for i in range(0,100):
        y.append('Legends')
        
    clf.fit(X,y)

def save_train_data():
    train_data = {'Canon':[], 'Legends':[]}
    for page in data['Canon'].values()[100:200]:
        bw = getBagOfWords(page)
        train_data['Canon'].append(bw)
        print "Canon"
    for page in data['Legends'].values()[100:200]:
        bw = getBagOfWords(page)
        train_data['Legends'].append(bw)
        print "Legend"
    
    print "Saving file"
    with open('train_data.json', 'w') as outfile:
            json.dump(train_data, outfile)

def save_test_data():
    test_data = {'Canon':[], 'Legends':[]}
    for page in data['Canon'].values()[0:10]:
        bw = getBagOfWords(page)
        test_data['Canon'].append(bw)
        print "Canon"
    for page in data['Legends'].values()[0:10]:
        bw = getBagOfWords(page)
        test_data['Legends'].append(bw)
        print "Legend"
    
    print "Saving file"
    with open('test_data.json', 'w') as outfile:
            json.dump(test_data, outfile)
# save_train_data()

# save_test_data()

with open('test_data.json', 'r') as outfile:
        testData = json.load(outfile)
    
clf = MultinomialNB()
train_classifier(clf)

y_hat = []
y_bow = ["Canon","Canon","Canon","Canon","Canon","Canon","Canon","Canon","Canon","Canon","Legends","Legends","Legends","Legends","Legends","Legends","Legends","Legends","Legends","Legends"]

for bw in testData['Canon']:
    y_hat.append(clf.predict(bw))
for bw in testData['Legends']:
    y_hat.append(clf.predict(bw))

failcount = 0.0
for i in range(0,len(y_hat)):
    if not(y_bow[i]==y_hat[i]):
        failcount = failcount+1
print failcount

training_error = failcount/len(y_hat)
print training_error
