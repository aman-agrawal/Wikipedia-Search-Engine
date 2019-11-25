import sys
import re
import os
import sys
import nltk
import pickle
import base64
import copy
import time


def read_file(testfile):
    with open(testfile, 'r') as file:
        queries = file.readlines()
    return queries


def write_file(outputs, path_to_output):
    '''outputs should be a list of lists.
        len(outputs) = number of queries
        Each element in outputs should be a list of titles corresponding to a particular query.'''
    with open(path_to_output, 'w') as file:
        for output in outputs:
            for line in output:
                file.write(line.strip() + '\n')
            file.write('\n')


def search(path_to_index, queries):
    stemmer = nltk.stem.SnowballStemmer('english')
    stop_words = {}
    stop_file = open("stop_words.txt", "r")
    words = stop_file.read()
    words = words.split(",")
    for word in words:
        word = word.strip()
        if word:
            stop_words[word[1:-1]] = 1
    fields = {}
    fields["t"] = open(path_to_index+"/title.txt","r")
    fields["c"] = open(path_to_index+"/category.txt","r")
    fields["i"] = open(path_to_index+"/infobox.txt","r")
    fields["b"] = open(path_to_index+"/body_text.txt","r")

    words_position = pickle.load(open(path_to_index+"/word_position.pickle", "rb"))
    title_position = pickle.load(open(path_to_index+"/title_doc_no.pickle", "rb"))

    final_query_result = []
    for query in queries:
        query_result = []
        if (query == "quit") :
            break
        start = time.time()
        query = query.lower().strip()
        if ":" in query:
            tmp_result = []
            flag = 0
            query_fields = query.split(" ")
            for queries in query_fields:
                field,query = queries.split(":")
                if field == "ref" or field == "ext" or field == "body":
                    field = "b"
                elif field == "title":
                    field = "t"
                elif field == "category":
                    field = "c"
                elif field == "infobox":
                    field = "i"
                for word in words:
                    word = word.strip()
                    word = stemmer.stem(word)
                    if word and word not in stop_words:
                        if word in words_position and field in words_position[word]:
                            docs = []
                            pointer = words_position[word][field]
                            fields[field].seek(pointer)
                            posting_list = fields[field].readline()[: -1]
                            posting_list = posting_list.split(",")
                            for doc in posting_list:
                                docs.append(doc.split(":")[0])

                            if flag == 0:
                                tmp_result = copy.deepcopy(docs)
                                flag = 1
                            else:
                                tmp_result = copy.deepcopy(list(set(tmp_result) & set(docs)))
                
            for doc_id in tmp_result:
                query_result.append(title_position[int(doc_id)])
        else:
            flag = 0
            tmp_result = []
            query_words = query.split(" ")
            for word in query_words:
                word = word.strip()
                word = stemmer.stem(word)
                if word not in stop_words:
                    if word in words_position:
                        docs = []
                        for field in words_position[word].keys():
                            pointer = words_position[word][field]
                            fields[field].seek(pointer)
                            posting_list = fields[field].readline()[: -1]
                            posting_list = posting_list.split(",")
                            for doc in posting_list:
                                docs.append(doc.split(":")[0])
                        if flag == 0:
                            tmp_result = copy.deepcopy(docs)
                            flag = 1
                        else:
                            tmp_result = copy.deepcopy(list(set(tmp_result) & set(docs)))
            
            for doc_id in tmp_result:
                query_result.append(title_position[int(doc_id)])
        
        end = time.time()
        print("Time Taken :- ",(end-start))
        if len(query_result) == 0:
            query_result = []
        else:
            query_result = set(query_result)
            query_result = list(query_result)

        if len(query_result) > 10:
        	query_result = query_result[0:10]
        final_query_result.append(query_result)

    return final_query_result



def main():
    path_to_index = sys.argv[1]
    testfile = sys.argv[2]
    path_to_output = sys.argv[3]

    queries = read_file(testfile)
    outputs = search(path_to_index, queries)
    write_file(outputs, path_to_output)


if __name__ == '__main__':
    main()
