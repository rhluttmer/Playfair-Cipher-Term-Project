import helpers
import digraphClass


def crackKeyTable(plaintext, ciphertext):
    # Makes dictionary of what each digraph encrypts to
    digraphMap = makeDigraphMap(plaintext, ciphertext)
    
    # Finds letters that either must be in a row or col and letters that
    # must be in a rect
    rowsAndCols, rectanlgesSet = findRectOrRowPairs(digraphMap)

    print(rowsAndCols, rectanlgesSet)
    
   
    
    
    return 42


# Makes a dictionary of which ciphertect digraph each plaintext digraph maps to
def makeDigraphMap(plaintext, ciphertext):
    digraphMap = {}

    # Make upper, take away non-alpha chars, make all J's into I's
    plaintext = helpers.removeNonAlphas(plaintext.upper()).replace('J', 'I')
    ciphertext = helpers.removeNonAlphas(ciphertext.upper())

    # Remove later, this is temporary
    if len(plaintext) > len(ciphertext):
        print('Error, plaintext and ciphertext not compatible')
        return None


    for i in range(0, len(plaintext), 2):
        plainChar1 = plaintext[i]
        if i + 1 >= len(plaintext) or plaintext[i+1] == plainChar1:
            plainChar2 = 'X'
        else:
            plainChar2 = plaintext[i+1]
        plainDigraph = digraphClass.Digraph(plainChar1, plainChar2)

        cipherChar1 = ciphertext[i]
        cipherChar2 = 'X' if (i+1 >= len(ciphertext)) else ciphertext[i+1]
        cipherDigraph = digraphClass.Digraph(cipherChar1, cipherChar2)

        digraphMap[plainDigraph] = cipherDigraph
    
    return digraphMap
    
# Finds digraph pairs that must be consecutive in a row or column 
# Example if AB -> BC then have row ABC
# Helper for findRectOrRowPairs
def findRowsAndCols(digraphMap):
    # Initialized as list to make looping through easier, will become set
    rowsAndCols = []

    # Look for plain-cipher pairs that must encrypt in row or col
    for plain in digraphMap:
        cipher = digraphMap[plain]
        
        # IF AB -> BC then row or col is ABC
        if cipher.let1 == plain.let2:
            rowsAndCols.append(plain.let1 + plain.let2 + cipher.let2)
        # Else if BA -> CB then row or col is ABC
        elif cipher.let2 == plain.let1:
            rowsAndCols.append(plain.let2 + plain.let1 + cipher.let1)

    # Combine all strings that are in the same row
    # For example ABC and BCD must be in same row, so becomes ABCD
    rowsAndCols = set(combineRowsCols(rowsAndCols))
    
    return rowsAndCols


# Combine all sequences in the same row
# For example ABC and BCD can combine into ABCD 
# Helper for findRowsAndCols
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


# Finds pairs that must be in rectangles or in rows
def findRectOrRowPairs(digraphMap):
    rowsAndCols = findRowsAndCols(digraphMap)
    rectangles = set()
    unorderedRowsAndCols = set()

    for key in digraphMap:
        value, revdValue = digraphMap[key], value.reverse()
        
        if value in digraphMap or revdValue in digraphMap:
            digraph1, digraph2 = key, value
            if value in digraphMap:
                digraph3 = digraphMap[value]
            else: # So revdValue in digraphMap
                # Using fact that if BA -> DC then AB -> CD no matter what
                revdDigraph3 = digraphMap[revdValue]
                digraph3 = revdDigraph3.reverse()
    
            # Check for digraphs in rectanlge (AB -> CD -> AB)
            if digraph1 == digraph3:
                rectangles.add((digraph1, digraph2))
                
                #TO DO: right now every pair added twice, fix
            
            # Check for letters in same row (AB -> CD -> EA) then row BDACE
            # or (AB -> CD -> BE) then row ACBDE
            elif digraph3.let2 == digraph1.let1:
                rowsAndCols.add(digraph1.let2 + digraph2.let2 + 
                                digraph1.let1 + digraph2.let1 + digraph3.let1)
            elif digraph3.let1 == digraph1.let2:
                rowsAndCols.add(digraph1.let1 + digraph2.let1 + digraph3.let1 +
                                digraph2.let2 + digraph3.let2)
            
            else:
                pass
                # TO DO: everything that makes it here can't be a rectangle
                # so it must be in a row or column, just we don't have order
                #unorderedRows.append

    deleteUnneededRowsAndCols(rowsAndCols)
    return rectangles, rowsAndCols

# Rows is stronger than rowsAndCols because we specifically know it
# is in a row (can't be in col), so if an entry rowOrCol brings no
# new information compared to what's in rows, then delete rowOrCol.
# Mutating method
def deleteUnneededRowsAndCols(rowsAndCols):
    toRemove = set()
    
    for rowOrCol1 in rowsAndCols:
        for rowOrCol2 in rowsAndCols:
            if isSubsetOf(rowOrCol1, rowOrCol2):
                print('here', rowOrCol1, rowOrCol2)
                toRemove.add(rowOrCol1)
                
    rowsAndCols -= toRemove
    

# Says whether smallRow is contained in bigRow with wrapparound allowed
# Example isSubsetOf('DEA', 'ABCDE') returns True
# Helper to deleteUnneededRows
def isSubsetOf(smallRow, bigRow):
    if len(smallRow) > len(bigRow) or smallRow == bigRow:
        return False
    for i in range(len(bigRow)):
        if bigRow.find(smallRow) != -1:
            return True
        bigRow = bigRow[1:] + bigRow[0]
    
    return False

def makeLetterMap(digraphMap):
    letterMap = {}

    for digraph in digraphMap:
        letter1Set = letterMap.get(digraph.let1, set()) 
        letterMap[digraph.let1] = letter1Set | {digraphMap[digraph].let1}

        letter2Set = letterMap.get(digraph.let2, set()) 
        letterMap[digraph.let2] = letter2Set | {digraphMap[digraph].let2}
    
    return letterMap



def main():
    
    plaintext = 'EX AM PL EA QU IC KB RO WN FO XI UM PS OV ER TH EL AZ YD OG AB MX AC DB'
    ciphertext = 'CZ BL LM AB RQ HD GE TM XM IL YH RP NU LY BU SI AP EV DI MI BC NW BD EC'
    digraphMap = makeDigraphMap(plaintext, ciphertext)
    print(makeLetterMap(digraphMap))
    
    

main()

