# Rose Luttmer

'''
This file encrypts and decrypts playfair messages (key must be entered)

Rules being used:
1. If digraph is same letter, replace second one with X, then encrypt
2. If in same row, move down by one
3. If in same col, move right by one
4. If in rectangle, stay in same row, switching col
5. Pad end with an X
6. Remove all non-alpha characters (instead of keeping as is
because this makes it more secure)

Still need to make this more user proof
'''

import string
import classes




# Takes a message, key, and mode (encrypt or decrypt) and returns newMessage
def encDecPlayfair(plaintext, key, mode='encrypt'):
    
    # Make the required table using the keyword
    keyTable = makeKeyTable(key)
    
    # Process plaintext so that it is ready for encoding
    digraphList = makeDigraphL(plaintext)
    
    newText = ''

    # Encode/decode one digraph at a time
    for digraph in digraphList:
        newDigraph = findNewDigraph(digraph, keyTable, mode)
        newLetter1, newLetter2 = newDigraph.let1, newDigraph.let2
        newText += newLetter1 + newLetter2

    return newText


# Uses keyword to create table for encryption / decryption
def makeKeyTable(key):
    tableDim = 5
    # Start with blank table
    keyTable = [[0]*tableDim for _ in range(tableDim)]

    # This is all letters that will need to go in table
    toPlace = removeNonAlphas(key.upper()) + string.ascii_uppercase
    
    # Since j's and i's are interchangable, only want i's
    toPlace = toPlace.replace('J', 'I')
    
    # Remove all but first occurance of letter to get string of len 25
    toPlace = removeStringDuplicates(toPlace)

    # actually place the letters in the board
    for row in range(tableDim):
        for col in range(tableDim):
            keyTable[row][col] = toPlace[0]
            toPlace = toPlace[1:]
    
    
    return keyTable


# Removes all but the first instance of a letter in a string
# Helper function for makeKeyTable
def removeStringDuplicates(s):
    i = 0

    while i < len(s):
        char = s[i]
        # Checks if character occured earlier in list
        if char in s[:i]:
            # Removes that character and all subsequent instances of it
            s = s[:i] + s[i+1:].replace(char, '')
        else:
            # Only increment i if character wasn't removed
            i += 1
    
    return s


# Makes string upper, removes non-alpha characters, add's necessary X's,
# and replaces J's with I's, then turns string into list of digraphs
def makeDigraphL(text):
    # Make uppercase and remove all non-alphabetic characters
    # and replace all J's with I's
    text = removeNonAlphas(text.upper()).replace('J', 'I')

    digraphList = []

    for i in range(0, len(text), 2):
        if i+1 >= len(text) or text[i] == text[i+1]:
            digraph = classes.Digraph(text[i], 'X')
        else:
            digraph = classes.Digraph(text[i], text[i+1])
        digraphList.append(digraph)
    
    return digraphList


# Takes non-alphabetic characters out of plaintext since those aren't 
# included in playfair
def removeNonAlphas(text):
    i = 0
    while i < len(text):
        if not text[i].isalpha():
            text = text[:i] + text[i+1:]
        else:
            i += 1
    
    return text


# Take digraph, keyTable, and mode (encrypt or decrypt)
# Returns the encrypted or decrypted digraph
# Helper to main encrypt/decrypt function
def findNewDigraph(digraph, keyTable, mode='encrypt'):
    boardDim = len(keyTable)

    (letter1, letter2) = digraph.let1, digraph.let2

    (row1, col1) = findRowCol(letter1, keyTable)
    #print(row1, col1)
    (row2, col2) = findRowCol(letter2, keyTable)
    #print(row2, col2)

    if row1 == row2:
        if mode == 'encrypt':
            newCol1 = (col1 + 1) % boardDim
            newCol2 = (col2 + 1) % boardDim
        else:
            newCol1 = (col1 - 1) % boardDim
            newCol2 = (col2 - 1) % boardDim

        newLetter1 = keyTable[row1][newCol1]
        newLetter2 = keyTable[row2][newCol2]
    
    elif col1 == col2:
        if mode == 'encrypt':
            newRow1 = (row1 + 1) % boardDim
            newRow2 = (row2 + 1) % boardDim
        else:
            newRow1 = (row1 - 1) % boardDim
            newRow2 = (row2 - 1) % boardDim
        
        newLetter1 = keyTable[newRow1][col1]
        newLetter2 = keyTable[newRow2][col2]
    else:
        newLetter1 = keyTable[row1][col2]
        newLetter2 = keyTable[row2][col1]
    
    return classes.Digraph(newLetter1, newLetter2)


# Finds row and col index of letter (uses fact that only once in list)
# Helper for findNewDigraph
def findRowCol(letter, keyTable):

    for row in range(len(keyTable)):
        for col in range(len(keyTable[0])):
            if keyTable[row][col] == letter:
                return row, col
    
    return None, None





