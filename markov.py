#!/usr/bin/env python

import sys
from random import randint
import string
import re

def make_chains(corpus):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    chain_dict = {}

    words = corpus.split() 

    for i in range(0,len(words)-2):
        #set up words to be processed
        w1 = words[i]
        w2 = words[i+1]
        w3 = words[i+2]

        #store w1+w2 in dict, with w3 as chain
        if(chain_dict.get((w1,w2))):
            chain_dict[(w1,w2)].append(w3)
        else:
            chain_dict[(w1,w2)] = [w3]

    # for t in chain_dict.keys():
    #     print t, chain_dict[t]
    return chain_dict


def get_first_pair(chains):

    while True:
        num_pairs = len(chains.keys())
        #generate random index for keys and set w1 and w2 equal to each value of the tuple
        w1, w2 = chains.keys()[randint(0,num_pairs-1)]

        if w1[0] in string.ascii_uppercase:
            return (w1,w2)

def end_on_punctuation(result):



    truncate=result.rfind(".")
    if truncate == -1:
        return result

    return result[0:truncate+1]

def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""
    
    result = ""

    w1, w2 = get_first_pair(chains)
    result = w1 + " " + w2
    
    while len(result) < 140 and not re.search("[\.\?!\"]", result[-1]) :
        # print "w1 and w2 are:",w1,w2
        if not chains.get((w1,w2)):
            break
        words = chains[(w1,w2)]
        # print "words is: ",words
        num = randint(0,len(words)-1)
        # print "num is", num
        w3 = words[num]
        if len(result)+len(w3) > 140:
            break
        result += " " + w3
        w1 = w2
        w2 = w3

    #result = end_on_punctuation(result)

    return result



def main():
    args = sys.argv

    script, filename = args

    # Change this to read input_text from a file
    input_text = open(filename)
    text = input_text.read()

    chain_dict = make_chains(text)
    random_text = make_text(chain_dict)
    print random_text

if __name__ == "__main__":
    main()
