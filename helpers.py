# Rose Luttmer

'''
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

# Takes a plaintext and a key and returns the ciphertext using playfair
def encryptPlayfair(plaintext, key):
    # Make the required table using the keyword
    keyTable = makeKeyTable(key)

    # Process plaintext so that it is ready for encoding
    digraphList = makeDigraphL(plaintext)

    cipherText = ''

    # Encode one digraph at a time
    for digraph in digraphList:
        cipherLetter1, cipherLetter2 = encryptDigraph(digraph, keyTable)
        cipherText += cipherLetter1 + cipherLetter2

    return cipherText


# Uses keyword to create table for encryption / decryption
def makeKeyTable(key):
    tableDim = 5
    # Start with blank table
    keyTable = [[0]*tableDim for _ in range(tableDim)]

    # This is all letters that will need to go in table
    toPlace = key.upper() + string.ascii_uppercase
    
    # Since j's and i's are interchangable, only want i's
    toPlace = toPlace.replace('J', '')
    
    # Remove all but first occurance of letter to get string of len 25
    toPlace = removeStringDuplicates(toPlace)
    
    # This should be removed, just in case something goes wrong
    if len(toPlace) != 25:
        print('Error', len(toPlace))
        return None

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

# Makes string upper, removes non-alpha characters, add's necessary X's
# then turns string into list of digraphs
def makeDigraphL(text):
    text = text.upper()
    
    # Remove all non-alphabetic characters
    i = 0
    while i < len(text):
        if not text[i].isalpha():
            text = text[:i] + text[i+1:]
        else:
            i += 1


    digraphList = []

    for i in range(0, len(text), 2):
        if i+1 >= len(text) or text[i] == text[i+1]:
            digraph = (text[i], 'X')
        else:
            digraph = (text[i], text[i+1])
        digraphList.append(digraph)
    
    return digraphList

# Take digraph, keyTable, and mode (encrypt or decrypt)
# Returns the encrypted or decrypted digraph
# Helper to main encrypt/decrypt function
def findNewDigraph(digraph, keyTable, mode='encrypt'):
    boardDim = len(keyTable)

    (letter1, letter2) = digraph

    (row1, col1) = findRowCol(letter1, keyTable)
    (row2, col2) = findRowCol(letter2, keyTable)

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
    
    return (newLetter1, newLetter2)

# Finds row and col index of letter (uses fact that only once in list)
# Helper for encryptDigraph
def findRowCol(letter, keyTable):
    # Treat all J's as I's
    if letter == 'J': letter = 'I'

    for row in range(len(keyTable)):
        for col in range(len(keyTable[0])):
            if keyTable[row][col] == letter:
                return row, col
    print(letter, keyTable)
    return None, None





