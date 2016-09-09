
# coding: utf-8

# In[5]:

import string

file = open("annagrams.txt")
data = file.read()

annagrams = {}
words = []
word = ''

for char in data:
    if char in string.ascii_letters:
        word = word + char
    elif word:
        words.append(word)
        word = ''

for word in words:
    annagram = "".join(sorted(word))
    
    if not annagrams.get(annagram):
        annagrams[annagram] = []
    
    annagrams[annagram].append(word)

for annagram in annagrams.keys():
    print(annagrams[annagram])

