'''
Created on 08/05/2015

@author: Kevin
'''
import json
import codecs
import DataFiltering
import matplotlib.pyplot as plt
import math
import matplotlib.patches as mpatches

# --- Load data ---
with codecs.open('CleanPageDataTest3(0-4371)', 'r', 'utf-8-sig') as dataFile:
    data = json.load(dataFile)


def wordCount(txt):
    return len(txt.split())

# --- Histogram ---
counter = {'Canon':[], 'nonCanon':[], 'hasNoCanon':[]}

for cat in data.keys():
    for page in data[cat].keys():
        counter[cat].append(math.log(wordCount(data[cat][page])))

plt.hist(counter['Canon'], bins=20)
canon_patch = mpatches.Patch(color='blue', label='Canon')
plt.hist(counter['nonCanon'], bins=20)
legend_patch = mpatches.Patch(color='green', label='Legend')
plt.legend(handles=[canon_patch, legend_patch])
plt.ylabel("# of pages")
plt.xlabel("log(word count)")
plt.show()