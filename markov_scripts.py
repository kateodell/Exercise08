#version of markov specific for processing scripts

#!/usr/bin/env python

import sys
from random import randint
import string
import re
import twitter

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


        #store ngram tuples in dict, with list of next words as value
        if(chain_dict.get(tuple(temp_words[0:-1]))):
            chain_dict[tuple(temp_words[0:-1])].append(temp_words[-1])
        else:
            chain_dict[tuple(temp_words[0:-1])] = [temp_words[-1]]

    # testing: print out dict after generation
    # for t in chain_dict.keys():
    #     print t, chain_dict[t]
    return chain_dict

#check if the given string is all upper case (ie. specifies a new character is speaking)
def is_all_upper(word): 
    return bool(re.search("^[A-Z,][A-Z,]+$",word))

def get_first_tuple(chains):
    #keep looping until a valid first tuple is returned (starts w/ a capital letter)
    while True:
        num_tuples = len(chains.keys())
        #generate random index for keys and set w1 and w2 equal to each value of the tuple
        num = randint(0,num_tuples-1)
        first_tuple = chains.keys()[num]

        if is_all_upper(first_tuple[0]):
            return first_tuple

def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""
    
    #initialize result and first set of words to start markov chain with
    result = ""
    temp_words = get_first_tuple(chains)

    result = " ".join(temp_words)
    
    # keep adding a word until the result is > 140 chars or 
    #   if the word ends w/ sentence-ending punctuation
    while not re.search("[\.\?!\"]", result[-1]) :
        # check if the chain is in the dict (edge case for end of file)
        if not chains.get(temp_words):
            break
        words = chains[temp_words]
        # generate random int to choose next word
        num = randint(0,len(words)-1)
        # get the next word
        next_word = words[num]
        #check if next_word is going to put us sover 140 chars
        if is_all_upper(next_word):
            break
        # add next word to result
        result += " " + next_word
        # splice words being processed to remove the first one and append the newly added word
        temp_words = temp_words[1:]
        temp_words = temp_words + tuple((next_word,))

    if not re.search("[\.\?!\"]", result[-1]):
        result = make_text(chains)
    
    return result

def post_on_twitter(text):
        print "Do you want to post that to Twitter? (y or n)"
        answer = raw_input()
        if answer == "y":
            #set up the twitter stuff  
            api = twitter.Api(consumer_key = 'asdf',consumer_secret = 'asdf',
                access_token_key = 'asdf', access_token_secret = 'asdf')
            #print api.VerifyCredentials()
            status = api.PostUpdate(text)
            print "It is now on the interwebz!"

def print_as_script(text):
    words = text.split()
    i = 0
    while (i < len(words) and is_all_upper(words[i])):
        print words[i],
        i += 1
    print ":"
    print " ".join(words[i:])
    print ""

def main():
    args = sys.argv

    script, filename, ngram = args

    input_text = open(filename)
    text = input_text.read()

    chain_dict = make_chains(text, int(ngram))

    while True:
        print "How many lines do you want to generate? (or q to quit) "
        n = raw_input("> ")
        if n == "q":
            break
        try:
            n = int(n)
        except:
            print "that wasn't a frakking number"
        #generate n lines
        for i in range(n):
            random_text = make_text(chain_dict)
            print_as_script(random_text)


        #post_on_twitter(random_text)





if __name__ == "__main__":
    main()
