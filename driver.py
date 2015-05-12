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
import operator

# --- Load data ---
with codecs.open('SortedCleaned', 'r', 'utf-8-sig') as dataFile:
    data = json.load(dataFile)


def wordCount(txt):
    return len(txt.split())

def factionCount(factions):
    return 0

def plotWordCount():
    # --- Histogram ---
    counter = {'Canon':[], 'Legends':[], 'nonCanon':[], 'Others':[]}
    
    maxPage = 0
    title = ""
    for cat in data.keys():
        for page in data[cat].keys():
            count = wordCount(DataFiltering.getContent(data[cat][page]))
            
            if count > maxPage:
                maxPage = count
                title = page
            
            counter[cat].append(math.log10(count))
    
    
    print "maxPage: "+str(maxPage)
    print "title: "+title
    
    #legend
    plt.hist(counter['Legends'], bins=20, color='green')
    legend_patch = mpatches.Patch(color='green', label='Legend')
    
    #canon
    plt.hist(counter['Canon'], bins=20, color='blue')
    canon_patch = mpatches.Patch(color='blue', label='Canon')
    
    #nonCanon
    plt.hist(counter['nonCanon'], bins=20, color='red')
    nonCanon_patch = mpatches.Patch(color='red', label='Fan Fiction')
    
    #nonCanon
    plt.legend(handles=[canon_patch, legend_patch, nonCanon_patch])
    plt.ylabel("# of pages")
    plt.xlabel("log10(word count)")
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
    
def printLargestPagest(nr):
    pages = {'Canon':{}, 'Legends':{}, 'nonCanon':{}, 'Others':{}}
    for cat in data.keys():
        for page in data[cat].keys():
            count = wordCount(DataFiltering.getContent(data[cat][page]))
            pages[cat][page] = count
                
    for cat in data.keys():
        print len(pages[cat])
        sorted_cat = sorted(pages[cat].items(), key=operator.itemgetter(1))
        sorted_cat.reverse()
        print sorted_cat[:nr]

printLargestPagest(100)
plotWordCount()
