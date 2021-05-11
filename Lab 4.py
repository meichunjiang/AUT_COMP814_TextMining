# Comp814 Text Mining Vectorizing Documents Lab
# Author : Chunjiang Mei 20100106
# Date   : 1/5/2021

# Task
# 1.	You will need the sample code snippets from lectures for the following tasks.
# 2.	Download and unzip the terrorism data.7z file into your working directory.
# 3.	Task description:
#       a.	Find bigrams of tokens for the all the articles in the dataset.
#       b.	Determine the most common bigram.
#       c.	Output 4 grams consisting of previous and next token around the most common bigram from step b above.
#       d.	See if you can figure out what if any useful information this gives you. How can you modify the strategy to extract the “most common topic” in the corpus

import nltk
import os
from nltk.corpus import stopwords
import collections
articleSet_path = '/Users/chunjiangmei/PycharmProjects/AUT COMP814 – Text Mining/Lab 4 ArticleSets/'


def remove_stop_words(sentence_list):
    stop_words = set(stopwords.words('english'))
    filtered_sentence = [w for w in sentence_list if not w in stop_words]
    return filtered_sentence

def find_bigrams(input_list):
    bigram_list = []
    for i in range(len(input_list) - 1):
        bigram_list.append((input_list[i], input_list[i + 1]))
    return bigram_list

#for num_txt in range(1,2):
for num_txt in range(1,len(os.listdir(articleSet_path))+1):
    filename = 'ArticleSet_'+str(num_txt)+'.txt'
    f = open(articleSet_path+filename)
    print("[Open File]: "+filename)
    lines = f.read()

    # task a : Find bigrams of tokens for the all the articles in the dataset.
    #lines = remove_stop_words(lines)
    lines = nltk.word_tokenize(lines)
    bigrams = find_bigrams(lines)
    print("The bigrams of " + filename+" is as followed : ")
    print(bigrams,"\n")

    # task b : Determine the most common bigram.
    count_bigrams = collections.Counter(bigrams)
    most_common_bigram = count_bigrams.most_common(1)
    print("The most common bigram of "+ filename+ " is :" , most_common_bigram[0],"\n")

    # task c : Output 4 grams consisting of previous and next token around the most common bigram from step b above.
    tokens_to_print = ""
    for i in range(len(bigrams)-1):
        if ( i> 0 and bigrams[i] == most_common_bigram[0].__getitem__(0)):
            tokens_to_print += bigrams[i-1].__getitem__(0) + " "
            tokens_to_print += most_common_bigram[0].__getitem__(0).__getitem__(0) + " "
            tokens_to_print += most_common_bigram[0].__getitem__(0).__getitem__(1) + " "
            tokens_to_print += bigrams[i+1].__getitem__(1) + "\n "
        #the previous token
    print("4 grams consisting of previous and next token around the most common bigram from step b above is :","\n",tokens_to_print)

    f.close()
    print("[Close File]: " + filename)\



