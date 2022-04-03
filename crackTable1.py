import helpers


def crackKeyTable(plaintext, ciphertext):
    digraphMap = makeDigraphMap(plaintext, ciphertext)
    
    rowsAndCols = findRowsAndCols(digraphMap)
    return 42

def findRowsAndCols(digraphMap):
    rowsAndCols = []

    # Look for plain-cipher pairs that must encrypt in row or col
    for plain in digraphMap:
        cipher = digraphMap[plain]
        
        # IF AB -> BC then row or col is ABC
        if cipher[0] == plain[1]:
            rowsAndCols.append(plain + cipher[1])
        # Else if BA -> CB then row or col is ABC
        elif cipher[1] == plain[0]:
            rowsAndCols.append(plain[1] + plain[0] + cipher[0])


    print(rowsAndCols)

 
    
    return rowsAndCols

def combineRowsCols(rowsAndCols):
    newRowsAndCols = set()

    # Combine all sequences in the same row
    # For example ABC and BCD can combine into ABCD 
    i = 0
    while i < len(rowsAndCols):
        rowOrCol1 = rowsAndCols[i]
        
        j = i+1
        while j < len(rowsAndCols):
            rowOrCol2 = rowsAndCols[j]

            # In form rowOrCol = CD... and rowOrCol2 = ...CD. Makes ...CD...
            if rowOrCol1[:2] == rowOrCol2[-2:]:
                rowsAndCols.append(rowOrCol2 + rowOrCol1[2:])
                
                
            # In form rowOrCol = ...CD and rowOrCol2 = CD... Makes ...CD...
            elif rowOrCol1[-2:] == rowOrCol2[:2]:
                rowsAndCols.append(rowOrCol1 + rowOrCol2[2:])
                
            else:
                newRowOrCol = rowOrCol2
            
            rowsAndCols[j] = newRowOrCol
        
        i += 1


# Makes a dictionary of which ciphertect digraph each plaintext digraph maps to
def makeDigraphMap(plaintext, ciphertext):
    digraphMap = {}

    # Make upper, take away non-alpha chars, make all J's into I's
    plaintext = helpers.removeNonAlphas(plaintext.upper()).replace('J', 'I')
    ciphertext = helpers.removeNonAlphas(ciphertext.upper())

    if len(plaintext) > len(ciphertext):
        print('Error, plaintext and ciphertext not compatible')
        return None


    for i in range(0, len(plaintext), 2):
        plainChar1 = plaintext[i]
        if i + 1 >= len(plaintext) or plaintext[i+1] == plainChar1:
            plainChar2 = 'X'
        else:
            plainChar2 = plaintext[i+1]

        cipherChar1 = ciphertext[i]
        cipherChar2 = 'X' if (i+1 >= len(ciphertext)) else ciphertext[i+1]

        digraphMap[plainChar1 + plainChar2] = cipherChar1 + cipherChar2
    
    return digraphMap
    

def main():
    plaintext = 'EX AM PL EA QU IC KB RO WN FO XI UM PS OV ER TH EL AZ YD OG AB'
    ciphertext = 'CZ BL LM AB RQ HD GE TM XM IL YH RP NU LY BU SI AP EV DI MI BC'
    digraphMap = makeDigraphMap(plaintext, ciphertext)
    print(findRowsAndCols(digraphMap))

main()





'''
Loop through texts, make dictionary of which diagraphs go to which
Then find the ones that go to the same row or same column
From there place rectangles of already placed letters
And then place everything else

'''



