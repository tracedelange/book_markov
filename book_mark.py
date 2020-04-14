import random as rm
import numpy as np
import pandas as pd
from exclude import bad_ends
import tweepy
from os import environ


from os import environ
ACCESS_KEY = environ['ACCESS_KEY']
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']

ACCESS_SECRET = environ['ACCESS_SECRET']



print(CONSUMER_KEY)
print(ACCESS_KEY)

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

# Create API object
api = tweepy.API(auth)

#Open and read corpus
books = open('book_titles.txt','r')
unsplit_corpus = books.readlines()
books.close()

#Process corpus from 'book_titles.txt'
def set_up(unsplit_corpus):
    corpus = []
    for entry in unsplit_corpus:
        corpus.append(entry.split(' '))
    final_corpus = []
    for entry in corpus:
        for item in entry:
            final_corpus.append(item.strip('(').strip(')'))
    return final_corpus

def make_pairs(corpus):
    
    for i in range(len(corpus) -1):
        yield (corpus[i], corpus[i + 1])

def generate(corpus, dic, words):
    first_word = np.random.choice(corpus)
    
    while first_word.islower() or first_word[-1][-1] == '\n' or first_word[-1][-1] == '?' or first_word == ':' or first_word == ' ':
        first_word = np.random.choice(corpus)

    chain = [first_word]
    
    ending_word = False
    
    while ending_word == False:
        word = np.random.choice(word_dict[chain[-1]])
        if len(chain) > words:
            ending_word = True
        else:
            chain.append(word)
            
    return chain

def book_gen(final_corpus, word_dict):
    
    title = generate(final_corpus, word_dict, 7)
    
    if title[-1] in bad_ends:
        del title[-1]
    b = ' '.join(title)
    book = b.replace('\n','').replace(')','')
    if book[-1] == ':' or book[-1] == ',':
        book = book[:-1]
    return book

corpus = set_up(unsplit_corpus)

pairs = make_pairs(set_up(unsplit_corpus))

word_dict = {}

for word_1, word_2 in pairs:
    if word_1 in word_dict.keys():
        word_dict[word_1].append(word_2)
    else:
        word_dict[word_1] = [word_2]
        

print(book_gen(corpus, word_dict))

tweet = str(book_gen(corpus, word_dict))

api.update_status(tweet)
