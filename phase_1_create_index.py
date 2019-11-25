#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
import os
import sys
import nltk
import xml.etree.cElementTree as et
import pickle
import base64
import time


# In[ ]:


stemmer = nltk.stem.SnowballStemmer('english')
stop_words = {}
stop_file = open("stop_words.txt", "r")
words = stop_file.read()
words = words.split(",")
for word in words:
    word = word.strip()
    if word:
        stop_words[word[1:-1]] = 1
# print(stop_words)


# In[ ]:


pattern = re.compile("[^a-zA-Z0-9]")
cssExp = re.compile(r'{\|(.*?)\|}',re.DOTALL)
linkExp = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',re.DOTALL)


# In[ ]:


# arguments = sys.argv
wikipedia_dump = sys.argv[1]
index_path = sys.argv[2]
# wikipedia_dump = "/home/vatsal/Documents/IIIT/Sem-3/IRE/wikipedia/wiki.xml"
content = et.iterparse(wikipedia_dump, events=("start", "end"))
content = iter(content)
# document_title = open("index/document_title.pickle", "wb")


# In[ ]:


title_inverted_index = {}
body_inverted_index = {}
category_inverted_index = {}
infobox_inverted_index = {}


# In[ ]:


document_no = 0
title_freq = {}
body_freq = {}
category_freq = {}
infobox_freq = {}
document_title = {}
document_word = {}
start = time.time()


# In[ ]:
def write_into_file(filename,inverted_object,flag):
    global document_word
    fileptr = open(filename, "w+")
    pointer = 0
    for word in inverted_object:
        posting_list = ",".join(inverted_object[word])
        posting_list = posting_list + "\n"
        if word not in document_word:
            document_word[word] = {}
        document_word[word][flag] = pointer
        fileptr.write(posting_list)
        pointer += len(posting_list)
    fileptr.close()

def write_pickle_file(filename, pickleobj):
    file = open(filename, "wb")
    pickle.dump(pickleobj, file)
    file.close()

for event,context in content:
    tag = re.sub(r"{.*}", "", context.tag)
    
    if event == "end":
        
        if tag == "title":
            
            title_text = context.text
            document_title[document_no]=title_text
            title_text = title_text.lower()
            try:
                words = re.split(pattern, title_text)
                for word in words:
#                     word=word.strip()
                    word = stemmer.stem(word)
                    if len(word) <= 2:
                    	continue
                    if word and word not in stop_words:
                        if word not in title_freq:
                            title_freq[word] = 1
                        else:
                            title_freq[word] += 1
            except:
                pass
        
        elif tag == "text":
            
            body_text = context.text
            body_text = linkExp.sub('',str(body_text))
            body_text = cssExp.sub('',str(body_text))
            try:
                category_words = re.findall("\[\[Category:(.*?)\]\]", body_text);
                if category_words != "":
                    for category_word in category_words:
                        words = re.split(pattern, category_word)
                        for word in words:
#                             word=word.strip()
                            word = stemmer.stem(word.lower())
                            if len(word) <= 2:
                                continue
                            if  word and word not in stop_words:
                                if word not in category_freq:
                                    category_freq[word] = 1
                                else:
                                    category_freq[word] += 1
            except:
                pass
            
            try:

                info_words = re.findall("{{Infobox((.|\n)*?)}}", body_text)
                if info_words != "":
                    for info_word in info_words:
                        for i_word in info_word:
                            words = re.split(pattern, i_word)
                            for word in words:
#                                 word=word.strip()
                                word = stemmer.stem(word.lower())
                                if len(word) <= 2:
                                	continue
                                if word and word not in stop_words:
                                    if word not in infobox_freq:
                                        infobox_freq[word] = 1
                                    else:
                                        infobox_freq[word] += 1
            except:
                pass
                                    
            try:
                words = re.split(pattern, body_text)

                for word in words:
                    word = stemmer.stem(word.lower())
                    if len(word) <= 2:
                    	continue
                    if word and word not in stop_words:
                        if word not in body_freq:
                            body_freq[word] = 1
                        else:
                            body_freq[word] += 1
            except:
                pass
            
        elif tag == "page":
            d_no = str(document_no)
            for word in body_freq:
                if word not in body_inverted_index:
                    body_inverted_index[word]=[]
                body_inverted_index[word].append(d_no + ":" + str(body_freq[word]))
            
            body_freq = {}

            for word in title_freq:
                if word not in title_inverted_index:
                    title_inverted_index[word]=[]
                title_inverted_index[word].append(d_no + ":" + str(title_freq[word]))
            
            title_freq = {}

            for word in category_freq:
                if word not in category_inverted_index:
                    category_inverted_index[word]=[]
                category_inverted_index[word].append(d_no + ":" + str(category_freq[word]))
            
            category_freq = {}

            for word in infobox_freq:
                if word not in infobox_inverted_index:
                    infobox_inverted_index[word]=[]
                infobox_inverted_index[word].append(d_no + ":" + str(infobox_freq[word]))
            
            infobox_freq = {}
                
            document_no += 1


# In[ ]:
filename = index_path+"/title.txt"
write_into_file(filename,title_inverted_index,'t')
filename = index_path+"/category.txt"
write_into_file(filename,category_inverted_index,'c')
filename = index_path+"/infobox.txt"
write_into_file(filename,infobox_inverted_index,'i')
filename = index_path+"/body_text.txt"
write_into_file(filename,body_inverted_index,'b')

filename = index_path+"/word_position.pickle"
write_pickle_file(filename, document_word)
filename = index_path+"/title_doc_no.pickle"
write_pickle_file(filename, document_title)


# In[ ]:


end = time.time()
# print("Time Taken :- ",(end-start))

