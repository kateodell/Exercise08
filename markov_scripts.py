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

    # initialize first words to use to create chain
    for i in range(0,len(words)-ngram):
        for n in range(0,ngram+1):
            temp_words[n] = words[i+n]

        #store ngram tuples in dict, with list of next words as value
        if(chain_dict.get(tuple(temp_words[0:-1]))):
            chain_dict[tuple(temp_words[0:-1])].append(temp_words[-1])
        else:
            chain_dict[tuple(temp_words[0:-1])] = [temp_words[-1]]

    # used for testing: print out dict after generation
    # for t in chain_dict.keys():
    #     print t, chain_dict[t]

    return chain_dict

#check if the given string is all upper case 
#  (ie. specifies a new character is speaking)
def is_all_upper(word): 
    return bool(re.search("^[A-Z,][A-Z,]+$",word))

def get_first_tuple(chains):
    #loop until a valid first tuple is returned (starts w/ a capital letter)
    while True:
        num_tuples = len(chains.keys())
        #generate random index in keys and set first_tuple to that key
        num = randint(0,num_tuples-1)
        first_tuple = chains.keys()[num]

        #return only if the first tuple is valid to start script line (word in all caps)
        if is_all_upper(first_tuple[0]):
            return first_tuple

def make_text(chains, limit_length):
    """Takes a dictionary of markov chains and returns random text
    based off an original text. Limits result to 140 chars if limit_length"""
    
    #initialize result and first set of words to start markov chain with
    result = ""
    temp_words = get_first_tuple(chains)

    result = " ".join(temp_words)
    
    # keep adding a word until the result is > 140 chars or 
    #   if the word ends w/ sentence-ending punctuation
    while True :
        # check if the chain is in the dict (edge case for end of file)
        if not chains.get(temp_words):
            break

        words = chains[temp_words]
        # generate random int to choose next word
        num = randint(0,len(words)-1)
        next_word = words[num]
        # END CONDITION: If limit_length True AND next_word will put us over 140 chars
        if limit_length and len(result)+len(next_word) > 140:
            break

        #END CONDITION: If limit_length AND end of sentence
        # if limit_length and bool(re.search("[\.\?!\"]", result[-1])):
        #     break

        # END CONDITION: check if at end of sentence AND next word is a name.
        if bool(re.search("[\.\?!\"]", result[-1])) and is_all_upper(next_word):
            break

        # add next word to result
        result += " " + next_word
        # splice words being processed to remove the first one and append the newly added word
        temp_words = temp_words[1:]
        temp_words = temp_words + tuple((next_word,))

    # if result doesn't end with end-punctuation, try again.
    if not re.search("[\.\?!\"]", result[-1]):
        result = make_text(chains, limit_length)
    
    return result

def post_on_twitter(text):
        print "Do you want to post that to Twitter? (y or n)"
        answer = raw_input()
        if answer == "y":
            #set up the twitter stuff  
            api = twitter.Api(consumer_key = 'agyxIKT7LNhC0QmAmgawA',consumer_secret = 'Hpf2VVWpYYabAthvZCFX9CYZHKchamhv8GVGIuuU',
                access_token_key = '1553835870-99vXUx6EDeA2cOPHi3mgOWGtdHNg8pcAf5ubmkr', access_token_secret = 'ehpTUPRKe7ebjjJKD0frI9WjZ18Le7jZm8cb5UvTgk')
            #print api.VerifyCredentials()
            status = api.PostUpdate(text)
            print "It is now on the interwebz!"

def format_as_script(text):
    result = ""
    words = text.split()
    i = 0
    while (i < len(words) and is_all_upper(words[i])):
        result = result + words[i]
        i += 1
    result += ": "
    result += " ".join(words[i:])
    return result

def main():
    args = sys.argv

    script, filename, ngram = args

    input_text = open(filename)
    text = input_text.read()

    chain_dict = make_chains(text, int(ngram))

    #ask if should limit to 140 chars for twitter posting
    print "Do you want to limit lines to 140 characters for Twitter posting? (y or n)"
    ans = raw_input("> ")
    if ans == "y":
        limit_length = True
    else:
        limit_length = False


    while True:
        print "How many lines do you want to generate? (or q to quit) "
        n = raw_input("> ")
        if n == "q":
            break
        try:
            n = int(n)
        except:
            print "that wasn't a frakking number!"

        #generate n lines
        for i in range(n):
            random_text = make_text(chain_dict, limit_length)
            random_text = format_as_script(random_text)
            print random_text
            if limit_length:
                post_on_twitter(random_text)


        #post_on_twitter(random_text)





if __name__ == "__main__":
    main()
