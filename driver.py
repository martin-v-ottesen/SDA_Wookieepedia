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
with codecs.open('FilteredPageDataTest(0-2500)', 'r', 'utf-8-sig') as dataFile:
    data = json.load(dataFile)

def wordCount(txt):
    return len(txt.split())

def factionCount(factions):
    return 0

def plotWordCount():
    # --- Histogram ---
    counter = {'Canon':[], 'nonCanon':[], 'hasNoCanon':[]}
    
    for cat in data.keys():
        for page in data[cat].keys():
            counter[cat].append(math.log(wordCount(DataFiltering.getContent(data[cat][page]))))
    
    plt.hist(counter['Canon'], bins=20)
    canon_patch = mpatches.Patch(color='blue', label='Canon')
    plt.hist(counter['nonCanon'], bins=20)
    legend_patch = mpatches.Patch(color='green', label='Legend')
    plt.legend(handles=[canon_patch, legend_patch])
    plt.ylabel("# of pages")
    plt.xlabel("log(word count)")
    plt.show()
    
def plotFactionSieze():
    counter = {'Canon':[], 'nonCanon':[], 'hasNoCanon':[]}
    
    for cat in data.keys():
        for page in data[cat].keys():
            counter[cat].append(DataFiltering.getBox(DataFiltering.getContent(data[cat][page]))[0]['affiliation'])
    
    plt.hist(counter['Canon'], bins=20)
    canon_patch = mpatches.Patch(color='blue', label='Canon')
    plt.hist(counter['nonCanon'], bins=20)
    legend_patch = mpatches.Patch(color='green', label='Legend')
    plt.legend(handles=[canon_patch, legend_patch])
    plt.ylabel("# of pages")
    plt.xlabel("log(word count)")
    plt.show()
    
plotWordCount()