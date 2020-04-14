import random as rm
import numpy as np
import pandas as pd
from exclude import bad_ends
import tweepy
from os import environ
from markov_functions import set_up, make_pairs, make_dict, generate, author_gen, book_gen

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

# Create API object
api = tweepy.API(auth)

#Open and read book title doc and make unspilt corpus
books = open('book_titles.txt','r')
unsplit_book_corpus = books.readlines()
books.close()

#open and read author doc and make unspilt corpus
names = open('authors.txt','r')
unsplit_author_corpus = names.readlines()
names.close()

#Open and read noun list and make a list of entries
nouns = open('nouns.txt','r')
noun_list = nouns.readlines()
nouns.close()

#format unsplit corpus's with set_up()
book_corpus = set_up(unsplit_book_corpus)
author_corpus = set_up(unsplit_author_corpus)

#Generate pairs
book_pairs = make_pairs(book_corpus)
author_pairs = make_pairs(author_corpus)

#Generate dictionaries 
book_word_dict = make_dict(book_pairs)
author_word_dict = make_dict(author_pairs)

#Generate markov list model for authors
author = generate(author_corpus, author_word_dict, 2)

#format author list model into final string
final_author = author_gen(author)

#generate final book title
final_book = book_gen(book_corpus, book_word_dict)

tweet = (final_book + '\nBy ' + final_author)

print(tweet)

try:
	api.update_status(tweet)
	print('Tweet Sent')
except TweepyError:
	print('Could not Tweet')