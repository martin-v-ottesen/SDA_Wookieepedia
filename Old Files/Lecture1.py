
# coding: utf-8

## Lecture 1

### Part 1

#### Ex 1B

# A list with elements from 1 to 100

# In[1]:

a = range(1,101)


# We slice the array to get the elements from 42 to 79

# In[2]:

b = a[41:79]


# We now define a simple function using def

# In[3]:

def f(x):
    return x*x+2


# We use this on each element of b in a for loop

# In[4]:

for x in b:
    f(x)


# If we want to save this to a file we need a new file object

# In[5]:

fileObject = open("Lect1.txt","r+")


# We reuse the for loop from before to write the data this time and close the fileobject

# In[6]:

for x in b:
    fileObject.write("%i \n" %f(x))
fileObject.close()


# In[12]:

x = "There are %d types of people." % 10
binary = "binary"
do_not = "don't"
y = "Those who know %s and those who %s." % (binary, do_not)

print x
print y

print "I said: %r." % x
print "I also said: '%s'." % y

hilarious = False
joke_evaluation = "Isn't that joke so funny?! %r"

print joke_evaluation % hilarious

w = "This is the left side of..."
e = "a string with a right side."

print w + e


### Part 2

#### 2a

# Wiki markup text test
# 
# Link to main page on wiki
# 
#     [[Main Page]]
#     
# Table with 4 elements
# 
#     {| class="wikitable"
#     |True Positive
#     |False Positive
#     |-
#     |False Negative
#     |True Negative
#     |}

### 2b Download of wiki page

# Download URL for the batman site
# 
# http://en.wikipedia.org/w/api.php?format=json&action=query&titles=Batman&prop=revisions&rvprop=content
# 
# format=json       : Self-explanatory
# 
# action=query      : We are requesting data
# 
# titles=Batman     : The title of the requested page is Batman
# 
# prop=revisions    : We are looking for a revision of the page
# 
# rvprop=content    : We are looking for the content of the revision

# We now attempt to download from python

# In[13]:

import urllib2
response = urllib2.urlopen('http://en.wikipedia.org/w/api.php?format=json&action=query&titles=Batman&prop=revisions&rvprop=content')
html = response.read()


# In[15]:

fileObject2 = open("batman.txt","r+")
fileObject2.write(html)
fileObject2.close()


# In[ ]:



