# Wikipedia_Search_Engine

# Description

* Implemented a search engine on the wikipedia dump of size 73.4 GB. In order to retrieve result faster and relevant, indexing and ranking is implemented. Relevance ranking algorithm is implemented using TF-IDF score to rank documents. Creating index takes around 14 hr on a given wikipedia dump. Result is retrieved in less than 1 second.

# Prerequisites

* python3
* For preprocessing and Stemming, I have used nltk library.
* To install nltk `pip3 install nltk`
* Install etree to parse wikipedia dump xml file
* To install etree `pip3 install elementpath`
* stop_words.txt file must be present in the same directory to remove stop words

# To run the project 

* Change wikipedia dump filepath in create_index.py file
* Change index file path to store index in create_index.py file
* Command to run create_index file
* `python3 create_index.py`
* Change filepath of a index file to load index in the memory in search file.
* Command to run search file
* `python3 search.py`

# Format of the query

* It supports two types of query.
* Normal query e.g. `new york` , `gandhi` , `1981 world cup`
* Field query e.g. `title:gandhi body:arjun infobox:gandhi category:gandhi ref:gandhi`
* Top 10 results will be printed.