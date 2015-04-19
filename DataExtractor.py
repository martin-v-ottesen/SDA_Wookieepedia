# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 10:40:24 2015

@author: Tugsav
"""

import urllib2
import json
import requests    

##One way... no subcategories
response = urllib2.urlopen('http://starwars.wikia.com/wiki/Special:Export/Category:Browse')
html = response.read()
import xmltodict
o = xmltodict.parse(html)

print o['mediawiki']['page'].keys()
print o['mediawiki']['page']['revision'].keys()
print o['mediawiki']['page']['revision']['text'].keys()
print o['mediawiki']['page']['revision']['text']['#text']


##Second way - better. just like the old way. i discovered that there were a new type of endpoint
#http://starwars.wikia.com/api.php?format=json&action=query&titles=Main%20Page&prop=revisions&rvprop=content
response = urllib2.urlopen('http://starwars.wikia.com/api.php?format=json&action=query&titles=Main_Page&prop=revisions&rvprop=content')
html = response.read()
j = json.loads(html)
print j['query']['pages']['390551']['revisions'][0]['*']


def query(request):
    request['action'] = 'query'
    request['format'] = 'json'
    lastContinue = {'continue': ''}
    while True:
        req = request.copy()
        req.update(lastContinue)
        result = requests.get('http://starwars.wikia.com/api.php',params=req).json()
        if 'query' in result: yield result['query']
        if 'continue' not in result: break
        lastContinue = result['continue']

content = []
for result in query({'list':'categorymembers','cmtitle':'Category:Star_Wars'}):
    content.append(result)
    
