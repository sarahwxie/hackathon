'''
Let's outline it:
* Place
* 
'''
import numpy as np
import pandas as pd
import time
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import pickle
# from nltk.probability import ProbabilisticMixIn


THRESHOLD = 0.2

def analyse_journal(entry, lower = True):
    '''
    Pulls out words
    '''
    stop_words = set(stopwords.words('english'))  # Common stop words
    other_words = set(['.', ","])
    if lower:
        word_tokens = word_tokenize(entry.lower())  # Tokenise
        filtered_sentence = [
            w for w in word_tokens if not (w in stop_words or w in other_words)]  # Filters
    else: 
        word_tokens2 = word_tokenize(entry)
        word_tokens = word_tokenize(entry.lower())
        filtered_sentence = []
        for w in range(len(word_tokens)):
            if not (word_tokens[w] in stop_words or word_tokens[w] in other_words):
                filtered_sentence.append(word_tokens2[w])
        

    # ps = PorterStemmer()
    # stems = [ps.stem(i) for i in filtered_sentence]
    tagged = nltk.pos_tag(filtered_sentence)
    # print(tagged)
    return filtered_sentence


def add_user(username, password):
    # ti = str(time.time())
    filename = "users/"+username+".csv"
    with open('data.csv', 'a') as f:
        if username in pd.read_csv('data.csv').iloc[:, 0].values:
            print("ERROR")
        else:
            f.write(username+ ","+ password+","+ filename + "\n")
            with open(filename, "a") as f:
                f.write("WORD, SENTIMENT, TIMES\n")

# Queries the database
def get_information(user):
    arr = pd.read_csv('data.csv')
    print(arr.iloc[:, 0].values)


def sentiment(text):
    '''
    Really rough Sentimental Analysis.
    '''
    text = analyse_journal(text)
    print(text)
    posnum = 0
    negnum = 0
    neunum = 0
    with open("negative-words.txt", "r") as f: neg = set(f.read().split("\n"))
    with open("positive-words.txt", "r") as f: pos = set(f.read().split("\n"))
    for i in text:
        if i in neg: negnum += 1
        elif i in pos: posnum += 1
        else: neunum += 1
    print(posnum, negnum, neunum)
    print(posnum/(negnum+posnum) * 2 - 1)
    return posnum/(negnum+posnum) * 2 - 1 
    
def get_key_words(text):
    words = analyse_journal(text, False)
    tagged = nltk.pos_tag(words)
    print(tagged)
    word_types_wanted = set(
        ["NN", "NNS", "NNP", "NNPS", "VB", "VBP", "VBD", "VBN"])
    # words = []
    val = sentiment(text) / len(words) # Sentiment divided by the number of major words
    new_words_and_val = []
    for word, wt in tagged:
        if wt in word_types_wanted:
            new_words_and_val.append([word, val])
    return new_words_and_val

def update_words(user, text):
    new_set = get_key_words(text)
    print(new_set)
    data = pd.read_csv("users/" + user + ".csv")
    old_words = list(data.iloc[:, 0])
    old_vals = list(data.iloc[:, 1])
    old_num = list(data.iloc[:, 2])
    for new_word in new_set:
        found = False
        for j in range(len(old_words)):
            print(new_word)
            if old_words[j] == new_word[0]:
                old_vals[j]+=new_word[1]
                old_num[j]+=1
                found = True
                break 
        if not found:
            old_words.append(new_word[0])
            old_vals.append(new_word[1])
            old_num.append(1)
    dct = {'WORD': old_words, 'SENTIMENT': old_vals, 'TIMES': old_num}
    df = pd.DataFrame(dct)
    df.to_csv('users/'+user+'.csv', index=False)


add_user("Hello", "abc")
update_words("Hello", "I hate life.")
