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

    # Combine all strings that are in the same row
    # For example ABC and BCD must be in same row, so becomes ABCD
    rowsAndCols = combineRowsCols(rowsAndCols)
    
    return rowsAndCols

# Combine all sequences in the same row
# For example ABC and BCD can combine into ABCD 
def combineRowsCols(rowsAndCols):
   
    # Loop through pairs in list (done with 'while' because list mutates)
    i = 0
    while i < len(rowsAndCols):
        rowOrCol1 = rowsAndCols[i]
        # Keeps tracks of whether rowOrCol1 was put into bigger string
        combined = False
        
        j = i+1
        while j < len(rowsAndCols):
            rowOrCol2 = rowsAndCols[j]

            # In form rowOrCol = CD... and rowOrCol2 = ...CD. 
            # Puts ...CD... at end of list and removes CD...
            if rowOrCol1[:2] == rowOrCol2[-2:]:
                rowsAndCols.append(rowOrCol2 + rowOrCol1[2:])
                rowsAndCols.pop(j)
                combined = True
                
            # In form rowOrCol = ...CD and rowOrCol2 = CD... Makes ...CD...
            elif rowOrCol1[-2:] == rowOrCol2[:2]:
                rowsAndCols.append(rowOrCol1 + rowOrCol2[2:])
                rowsAndCols.pop(j)
                combined = True
           
            else:  # Only increment if nothing was popped   
                j += 1
        
        if combined == True:
            rowsAndCols.pop(i)
        else: # Once again, only increment if not popped
            i += 1
            
    return rowsAndCols


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

