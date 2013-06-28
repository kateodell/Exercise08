#!/usr/bin/env python

import sys
from random import randint
import string
import re

def make_chains(corpus, ngram):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    chain_dict = {}
    temp_words = [0]*(ngram+1)

    words = corpus.split() 

    for i in range(0,len(words)-ngram):
        #set up words to be processed
        # w1 = words[i]
        # w2 = words[i+1]
        # w3 = words[i+2]
        for n in range(0,ngram+1):
            temp_words[n] = words[i+n]


        #store w1+w2 in dict, with w3 as chain
        if(chain_dict.get(tuple(temp_words[0:-1]))):
            chain_dict[tuple(temp_words[0:-1])].append(temp_words[-1])
        else:
            chain_dict[tuple(temp_words[0:-1])] = [temp_words[-1]]

    # for t in chain_dict.keys():
    #     print t, chain_dict[t]
    return chain_dict


def get_first_tuple(chains):

    while True:
        num_tuples = len(chains.keys())
        #generate random index for keys and set w1 and w2 equal to each value of the tuple
        num = randint(0,num_tuples-1)
        first_tuple = chains.keys()[num]

        if first_tuple[0][0] in string.ascii_uppercase:
            return first_tuple

def end_on_punctuation(result):

    truncate=result.rfind(".")
    if truncate == -1:
        return result

    return result[0:truncate+1]

def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""
    
    result = ""
    temp_words = get_first_tuple(chains)

    result = " ".join(temp_words)

    # print "result before loop is:",result
    
    while len(result) < 140 and not re.search("[\.\?!\"]", result[-1]) :
        # check if the chain is in the dict (edge case for end of file)
        if not chains.get(temp_words):
            # print "breaking because get failed"
            break
        words = chains[temp_words]
        # generate random int to choose next word
        num = randint(0,len(words)-1)
        # get the next word
        next_word = words[num]
        #check if next_word is going to put us over 140 chars
        if len(result)+len(next_word) > 140:
            # print "breaking because next word goes over 140. next word is:",next_word
            break
        # add next word to result
        result += " " + next_word
        # splice words being processed to remove the first one and append the newly added word
        temp_words = temp_words[1:]
        temp_words = temp_words + tuple((next_word,))

        # print "at end of loop, temp_words is:", temp_words

    #result = end_on_punctuation(result)
    # print "result after loop is",result
    if not re.search("[\.\?!\"]", result[-1]):
        result = make_text(chains)
    
    return result



def main():
    args = sys.argv

    script, filename, ngram = args

    # Change this to read input_text from a file
    input_text = open(filename)
    text = input_text.read()

    chain_dict = make_chains(text, int(ngram))
    random_text = make_text(chain_dict)
    print random_text

if __name__ == "__main__":
    main()
