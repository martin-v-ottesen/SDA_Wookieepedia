# -*- coding: utf-8 -*-
"""
Created on Tue May 12 16:37:00 2015

@author: Tugsav
"""
import codecs
import json
import numpy as np

fileObject = codecs.open('Vocabulary','r','utf-8-sig')
vocab = json.load(fileObject)
fileObject.close()

fileObject = codecs.open('BoolSums','r','utf-8-sig')
sums = json.load(fileObject)
fileObject.close()

indexer = np.array(sums)<5

ban_list = np.array(vocab)[indexer]

print 'You just banned '+str(len(ban_list))+' words :)'

fileObject = codecs.open('BanList','w','utf-8-sig')
json.dump(list(ban_list),fileObject)
fileObject.close()

vocab = np.array(vocab)[indexer==False]

fileObject = codecs.open('newVocabulary','w','utf-8-sig')
json.dump(list(vocab),fileObject)
fileObject.close()