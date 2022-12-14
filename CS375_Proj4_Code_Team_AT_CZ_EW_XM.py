'''
CS375 Project 4
Aidan Tokarski, Cynthia Zafris,
Eda Wright, Xavier Markowitz

This program explores different edit distance algorithms
and a spell spell checker. 

Usage:
Provide a command line argument for which function you want to run.
Below are all the possible arguments:

spellChecker_test
Run the tests on the spell checker (see function below with same name)

documentCheck_test
Run tests on documentCheck function

editDistance_test
Runs test on the edit distance functions

ex. Usage: CS375_Proj4_Code_Team_AT_CZ_EW_XM.py editDistance_test

Layout of File:
editDistance_rec
editDistance_iter
spellCheck
findSuggestions (helper function for spellCheck)
documentCheck (Opens a txt document and spell checks it)
spellCheckImproved 
make_word_dict (Opens a txt dictionary file and converts to list of words)
3 test functions for each of the main algorithms
main function which handles command line arguments and runs desired functions
'''

import sys
import re
import time

def editDistance_rec(S,T):
    '''
    Input: Two strings, S and T, that represent two words
    
    Output: Returns the minimum number of operations that need to be conducted on string S to transform it into string T
    
    Note: This algorthm is case sensitive, changing from lower to upper case will count as 1 edit

    Complexity:
    '''
    if S == '': # if S is an empty string
        return len(T) 
    if T == '': # if T is an empty string
        return len(S)
    if S[-1] == T[-1]: # if the last letter in S and T is the same
        return editDistance_rec(S[:-1],T[:-1]) 
    return 1 + min( editDistance_rec(S[:-1],T[:-1]), # if the last letter in S and T is not the same
                    editDistance_rec(S[:-1],T),
                    editDistance_rec(S,T[:-1]) ) 

def editDistance_iter(S,T):
    '''
    Input: Two strings, S and T, that represent two words
    
    Output: Returns the minimum number of operations that need to be conducted on string S to transform it into string T

    Note: This algorthm is case sensitive, changing from lower to upper case will count as 1 edit

    Complexity:
    '''
    m = len(S)
    n = len(T)

    grid = []
    for i in range(m + 1): # rows: S, using m
        grid.append([])
        for j in range(n + 1): # columns: T, using n
            grid[i].append(0)  

    for i in range(1,m + 1): # base case for rows
        grid[i][0] = i  
    
    for j in range(1,n + 1): # base case for columns
        grid[0][j] = j

    for i in range(1, m + 1): # all but the first row / first column
        for j in range(1, n + 1): 
            if S[i - 1] == T[j - 1]: # if specified letters in S and T are the same
                grid[i][j] = grid[i - 1][j - 1] 
            else: # if specified letters in S and T are not the same
                grid[i][j] = 1 + min( 
                                grid[i - 1][j - 1],
                                grid[i - 1][j],
                                grid[i][j - 1]
                            ) 

    return grid[m][n]

def spellCheck(T, D):
    '''
    Input: A sting of text T to be spell checked (length n words). A python list D of correctly spelled words (length m words).

    Output: For every word w in T that does not occour in D, 5 words in D with minimal edit distance.
    These will be returned as a dictionary with the w as the key and the value a list of spelling suggestions.

    Words are defined as strings seperated by whitespace (spaces or \n). No other preprocessing is done, so the spell checker
    is case sensitive. Whitespace will be striped from words in T, but not in D.

    Complexity:
    '''
    out = {} #Output dictionary
    words = T.split() #split by whitespace, strips any remaining white space
    for word in words:
        if word not in D: #linear search, O(M)
            out[word] = findSuggestions(word, D)
    return out

def spellCheckImproved(T, D):
    '''
    Input: A sting of text T to be spell checked (length n words). A python list D of correctly spelled words (length m words).

    Output: For every word w in T that does not occour in D, 5 words in D with minimal edit distance.
    These will be returned as a dictionary with the w as the key and the value a list of spelling suggestions.

    Words are defined as strings seperated by whitespace (spaces or \n). No other preprocessing is done, so the spell checker
    is case sensitive. Whitespace will be striped from words in T, but not in D.

    Complexity:
    '''
    out = {} #Output dictionary
    
    words = set(T.split()) 
    D = set(D)
    for word in words:
        if word not in D: #constant time search, O(1)
            out[word] = findSuggestions(word, D)
    return out

def findSuggestions(word, D):
    '''
    Input: A mispelled word, a dictionary of correctly spelled words D

    Output: Returns a list of 5 words from D with the closest edit distance to word. If there is a tie, the word
    that appears in D first is valued closer to the word.

    Complexity:
    '''
    out = [] #Output list
    editDistances = [1e10, 1e10, 1e10, 1e10, 1e10] #keeps track of the 5 smallest edit distances so far
    for d in D: #For each word in the dictionary
        editDistance =  editDistance_iter(d, word) #Edit distance of currend dictionary word
        k = 5 #index where new word should be inserted
        while k > 0: #Determining where d should be inserted
            # print(editDistance[k])
            # print(editDistances[k-1])
            if editDistance < editDistances[k-1]:
                k -= 1 #d belongs higher in the list
            else:
                #the editDistance[k-1] could not be in the while loop (causes index error)
                #this gets around that, but unfortunatly uses a break
                break 
        #Inserting d and edit distance into their respective lists
        out.insert(k, d)
        editDistances.insert(k, editDistance)
        #Trimming list to sill be 5 long
        out = out[:5]
        editDistances = editDistances[:5]
    return out

def documentCheck(textfile, dictfile):
    '''
    Input: A text file to be spellchecked, and a text file dictionary of valid words.

    Output: Returns a list of invalid words, and 5 suggestions for replacement.
    '''
    with open(textfile, encoding='utf-8') as f:
        text = f.read()
        # Replacement order is very important!
        text = text.replace("\n", " ") # All newlines converted to spaces
        text = text.replace("—", " ") # All dashes converted to spaces
        # Attempt to remove as many invalid "words" as possible
        text = re.sub(r'[a-zA-Z1-9]*[\.<>\[\]@]+[a-zA-Z1-9]+[^\.]', '', text)
        text = text.replace("’", "'") # Apostrophe encoding correction
        text = text.replace("-", " ") # All hyphens converted to spaces
        # Hyphens to spaces treats compound words as two separate words
        text = text.replace(".", " ") # All periods converted to spaces
        text = re.sub(r'[^a-zA-Z\' ]', '', text) # Remove all characters that cannot be in a valid word
        text = re.sub(r' [a-zA-Z] ', ' ', text) # Remove all single character words
        text = re.sub(r' [a-zA-Z\'][a-zA-Z\'] ', ' ', text) # Remove all two character words
        text = text.lower() # Spell-checker is case-sensitive, so we use only lowercase checking
    
    with open(dictfile) as f:
        dict_text = f.read()
        dict_text = dict_text.lower() # Same as above, dictionary is made all lowercase
        dict = dict_text.split("\n")
            
    check_out = spellCheck(text, dict)
    return check_out

def make_word_list(filename):
    #looping through the text file and 
    d = []
    with open(filename) as f:
        for line in f:
            words = line.split()
            d.append(words[0])
    return d

def make_word_dict(filename):
    #looping through the text file and 
    d = set()
    with open(filename) as f:
        for line in f:
            words = line.split()
            d.add(words[0])
    return d

def editDistance_test():
    print("Testing Edit Distance")
    print("---------")
    print("Input: ")
    print("'car' 'cat' - should output 1")
    print("Output: ")
    print("Iterative: " + str(editDistance_iter("car","cat")) + " / Recursive: " + str(editDistance_rec("car","cat"))) 
    print("Input: ")
    print("'cars' 'cat' - should output 2")
    print("Output: ")
    print("Iterative: " + str(editDistance_iter("cars","cat")) + " / Recursive: " + str(editDistance_rec("cars","cat"))) 
    print("Input: ")
    print("'analysis' 'algorithms' - should output 8")
    print("Output: ")
    print("Iterative: " + str(editDistance_iter("analysis","algorithms")) + " / Recursive: " + str(editDistance_rec("analysis","algorithms"))) 
    print("Input: ")
    print("'' 'reach' - should output 5")
    print("Output: ")
    print("Iterative: " + str(editDistance_iter("","reach")) + " / Recursive: " + str(editDistance_rec("","reach"))) 
    print("Input: ")
    print("'creative' '' - should output 8")
    print("Output: ")
    print("Iterative: " + str(editDistance_iter("creative","")) + " / Recursive: " + str(editDistance_rec("creative",""))) 
    print("Input: ")
    print("'rock' 'rock' - should output 0")
    print("Output: ")
    print("Iterative: " + str(editDistance_iter("rock","rock")) + " / Recursive: " + str(editDistance_rec("rock","rock")))

    print("\nTesting Runtime")
    print("---------")
    print("Input: ")
    print("'abcdefghijklmn' 'zyxvutsrqponm'")
    print("Recursive:")
    start = time.monotonic()
    editDistance_rec("abcdefghijklmn","zyxvutsrqponm")
    end = time.monotonic()
    print("Time elapsed: {}".format(end - start))
    print("Iterative:")
    start = time.monotonic()
    editDistance_iter("abcdefghijklmn","zyxvutsrqponm")
    end = time.monotonic()
    print("Time elapsed: {}".format(end - start))

def spellCheck_test():
    st = time.time()
    print("Testing Spell Checker")
    print("---------")
    print("Test 1: Small dictionary and storing")
    print("Input: ths is a tst of spel check, [this, is, a, test, of, spell, check]")
    print("Output:")
    print(spellCheck("ths is a tst of spel check", ["this", "is", "a", "test", "of", "spell", "check"]))
    print("---------")
    print("Tesst 2: Order of suggestions")
    print('Input: ("Aalsis", ["Analysis", "Analys", "hello", "HappY", "Algorithm", "Hopper"]')
    dict = ["Analysis", "Analys", "hello", "HappY", "Algorithm", "Hopper"]
    test2_out = spellCheck("Aalsis", dict)
    print(f"Output: {test2_out}")
    print("Edit Distance for all words in dictionary:")
    for word in dict:
        print(f"{word}: {editDistance_iter(word.lower(), 'AaLsIs'.lower())}")
    print("---------")

    st = time.time()
    print("Test 3: Using SCOWL Dictionary")
    # with open('en_US-large.txt') as f:
    #     SCOWL = f.readlines()
    #     for i in range(len(SCOWL)):
    #         SCOWL[i] = SCOWL[i].strip()
    SCOWL = make_word_list('en_US-large.txt')
    SCOWL = make_word_dict('en_US-large.txt')
    print("Input: 'this is a tst of teh spell chekr with SCOWL', SCOWL dictionary")
    res = spellCheck('this is a tst of teh spell chekr with SCOWL', SCOWL)
    for word in res:
        print(f"{word} : {res[word]}")
    print("Note for 'teh', 'the' was not suggested. With short words, the edit distance to other short words is very small, thus the correct word may not make it on the suggestions ")
    print("---------")
    ed = time.time()
    print(ed - st)

    st = time.time()
    print("Test 4: Adding Punctuation and Capitals")
    print("Our spell checker is case sensitive and does not strip punctuation")
    print("Input: 'This sentence has no spelling mistakes. It's color is beautiful? 1/2 of all things are red/green some OF the time!', SCOWL dictionary")
    print("Output:")
    print(spellCheck("This sentence has no spelling mistakes. It's color is beautiful? 1/2 of all things are red/green some OF the time.", SCOWL))
    ed = time.time()
    print(ed - st)

def spellCheckImproved_test():
    st = time.time()
    print("Testing Improved Spell Checker")
    print("---------")
    print("Test 1: Small dictionary and storing")
    print("Input: ths is a tst of spel check, [this, is, a, test, of, spell, check]")
    print("Output:")
    print(spellCheckImproved("ths is a tst of spel check", ["this", "is", "a", "test", "of", "spell", "check"]))
    print("---------")

    print("Tesst 2: Order of sugestions")
    print('Input: ("Aalsis", ["Analysis", "Analys", "hello", "HappY", "Algorithm", "Hopper"]')
    dict = ["Analysis", "Analys", "hello", "HappY", "Algorithm", "Hopper"]
    test2_out = spellCheckImproved("Aalsis", dict)
    print(f"Output: {test2_out}")
    print("Edit Distance for all words in dictionary:")
    for word in dict:
        print(f"{word}: {editDistance_iter(word.lower(), 'AaLsIs'.lower())}")
    print("---------")

    st = time.time()
    print("Test 3: Using SCOWL Dictionary")
    # with open('en_US-large.txt') as f:
    #     SCOWL = f.readlines()
    #     for i in range(len(SCOWL)):
    #         SCOWL[i] = SCOWL[i].strip()
    SCOWL = make_word_list('en_US-large.txt')
    print("Input: 'this is a tst of teh spell chekr with SCOWL', SCOWL dictionary")
    print(spellCheckImproved('this is a tst of teh spell chekr with SCOWL', SCOWL))
    print("Note for 'teh', 'the' was not suggested. With short words, the edit distance to other short words is very small, thus the correct word may not make it on the suggestions ")
    print("---------")
    ed = time.time()
    print(ed - st)

    st = time.time()
    print("Test 4: Adding Punctuation and Capitals")
    print("Our spell checker is case sensitive and does not strip punctuation")
    print("Input: 'This sentence has no spelling mistakes. It's color is beautiful? 1/2 of all things are red/green some OF the time!', SCOWL dictionary")
    print("Output:")
    print(spellCheckImproved("This sentence has no spelling mistakes. It's color is beautiful? 1/2 of all things are red/green some OF the time.", SCOWL))
    ed = time.time()
    print(ed - st)
    res = spellCheck("This sentence has no spelling mistakes. It's color is beautiful? 1/2 of all things are red/green some OF the time.", SCOWL)
    for word in res:
        print(f"{word} : {res[word]}")
    
def documentCheck_test():
    print("Testing Document Spell Check")
    print("---------")
    print("Test 1: Using SCOWL wordlist on project assignment")
    start = time.monotonic()
    print(documentCheck("CS375f22_proj4_DynamicProgramming.txt", "en_US-large.txt"))
    end = time.monotonic()
    print("Time elapsed: {}".format(end - start))
    print("---------")
    print("Test 2: Using CS375-specific wordlist on project assignment")
    start = time.monotonic()
    print(documentCheck("CS375f22_proj4_DynamicProgramming.txt", "CS375_dict.txt"))
    end = time.monotonic()
    print("Time elapsed: {}".format(end - start))
    print("---------")
    print("Test 3: Using SCOWL wordlist on PS5")
    start = time.monotonic()
    print(documentCheck("cs375f22_PS5.txt", "en_US-large.txt"))
    end = time.monotonic()
    print("Time elapsed: {}".format(end - start))
    print("---------")
    print("Test 4: Using CS375-specific wordlist on PS5")
    start = time.monotonic()
    print(documentCheck("cs375f22_PS5.txt", "CS375_dict.txt"))
    end = time.monotonic()
    print("Time elapsed: {}".format(end - start))

def main():
    '''
    Handles command line arguments to run the proper function.
    See usage statement above for all the possible arguments
    '''
    if len(sys.argv) < 2:
        print("Please provide command line arguments")
        return
    
    if sys.argv[1] == "spellCheck_test":
        spellCheck_test()
        return
    
    if sys.argv[1] == "spellCheckImproved_test":
        spellCheckImproved_test()
        return

    if sys.argv[1] == "documentCheck_test":
        documentCheck_test()
        return
    
    if sys.argv[1] == "editDistance_test":
        editDistance_test()
        return
    
    print("Could not identify command line arguments")

if __name__ == "__main__":
    main()


