import helpers

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

# Takes a message, key, and mode (encrypt or decrypt) and returns newMessage
def encryptPlayfair(plaintext, key, mode='encrypt'):
    # Make the required table using the keyword
    keyTable = helpers.makeKeyTable(key)
    
    # Process plaintext so that it is ready for encoding
    digraphList = helpers.makeDigraphL(plaintext)

    newText = ''

    # Encode/decode one digraph at a time
    for digraph in digraphList:
        newLetter1, newLetter2 = helpers.findNewDigraph(digraph, keyTable, mode)
        newText += newLetter1 + newLetter2

    return newText

def main():
    print(encryptPlayfair('FCBLADSZOETN', 'computer', 'decrypt'))

main()