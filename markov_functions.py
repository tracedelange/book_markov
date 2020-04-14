import numpy as np
import random as rm
from exclude import bad_ends

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

def make_dict(pairs):
	word_dict = {}
	for word_1, word_2 in pairs:
		if word_1 in word_dict.keys():
			word_dict[word_1].append(word_2)
		else:
			word_dict[word_1] = [word_2]
	return word_dict

        
def generate(corpus, word_dict, words):
    first_word = np.random.choice(corpus)
    
    while first_word.islower() or first_word[-1][-1] == '\n' or first_word[-1][-1] == '?' or first_word == ':' or first_word == ' ':
        first_word = np.random.choice(corpus)

    chain = [first_word]
    print('starting word is ' + str(chain[0]))
    
    ending_word = False
    
    while ending_word == False:
        word = np.random.choice(word_dict[chain[-1]])
        if len(chain) > words:
            ending_word = True
        else:
            chain.append(word)
            
    return chain
    
def book_gen(final_corpus, word_dict):
    
    title = generate(final_corpus, word_dict, 6)
    
    if title[-1] in bad_ends:
        del title[-1]
    b = ' '.join(title)
    book = b.replace('\n','').replace(')','')
    if book[-1] == ':' or book[-1] == ',':
        book = book[:-1]
    return book
    
def author_gen(name):
	#Open and read noun list and make a list of entries
	nouns = open('nouns.txt','r')
	noun_list = nouns.readlines()
	nouns.close()
	
	#Replace a random word out of the author name 80% of the time
	rand = rm.randint(0,10)
	if rand > 2:
		remove = name[rm.randint(0,2)]
		sub = np.random.choice(noun_list)
		n = ' '.join(name)
		final = n.replace(remove, sub.capitalize())

	else:
		final = ' '.join(name)

	return final.replace('\n','')    
