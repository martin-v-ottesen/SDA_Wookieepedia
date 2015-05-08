'''
Created on 08/05/2015

@author: Kevin
'''
import json
import codecs
import DataFiltering
import matplotlib.pyplot as plt

dataFile = codecs.open('PageDataMerge(0-2500)', 'r', 'utf-8-sig')

data = json.load(dataFile)

dataFile.close()

print len(data.keys())
print data.keys()

print "Canon: " + str(len(data['Canon'].keys()))
print "nonCanon: " + str(len(data['nonCanon'].keys()))
print "hasNoCanon: " + str(len(data['hasNoCanon'].keys()))

clean_canon = DataFiltering.filterdata(data['Canon'])
# clean_non_canon = DataFiltering.filterdata(data['nonCanon'])
# clean_hasNo_canon = DataFiltering.filterdata(data['hasNoCanon'])

# print clean_canon.keys()



print clean_canon['Gungan/Canon']
exit()


def wordCount(txt):
    return len(txt.split())

word_count = []

for page in clean_canon:
    word_count.append(wordCount(page))


print len(word_count)
print word_count

plt.hist(word_count, bins=50)
plt.show()

