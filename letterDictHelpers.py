# Rose Luttmer

'''
Helper functions to the "createAndPopulateLetterDict" function
(These are in their own file because they take up a lot of space
but are only used to set up the backtracking, not actually during it)

Info found with these functions:
For each letter, we know what it shares a row or column with (but not in
which order this happens)
Then we also have a list of things that are ordered bits of rows or columns
And we also have a set of some ordered bits that must be in rows

'''


import classes

# Makes a dict mapping letter names to 'Letter' instances
def makeEmptyLetterDict():
    letterDict = {}
    
    for i in range(26):
        char = chr(ord('A') + i)
        letterDict[char] = classes.Letter(char)
    
    return letterDict

# Updates letter dict to reflect which letters each letter encrypts to
# Mutating
def addEncryptsTo(digraphMap, letterDict):
    for digraph in digraphMap:
        encodedDigraph = digraphMap[digraph]
        letterDict[digraph.let1].encryptsTo.add(encodedDigraph.let1)
        letterDict[digraph.let2].encryptsTo.add(encodedDigraph.let2)
    
# Adds row partners into letterDict
# Mutating function (changes letterDict)
def makeRowPartners(letterDict):
    # Motivation: If A -> B and B -> A they must be in rows (from rectangles)
    for letter1 in letterDict:
        for letter2 in letterDict[letter1].encryptsTo:
            if  letter1 in letterDict[letter2].encryptsTo:
                letterDict[letter1].inSameRow.add(letter2)
                letterDict[letter2].inSameRow.add(letter1)


   

    
       

# Make it so that all letters in a row have all other letters listed
# For example, input could have A.inSameRow = {B}, B.inSameRow = {C,D}
# and D.inSameRow = {A,E}, this would make it so that
# A.inSameRow = {B, C, D, E}, B.inSameRow = {A, C, D, E}, etc
def consolidateRowColPartners(letterDict):
    consolidateRowPartners(letterDict)
    consolidateColPartners(letterDict)
    
# Mutatingly changes letterDic so that all letters in same row are listed
# (See consolidateRowColParners for more in-depth explanation)
def consolidateRowPartners(letterDict):
    # This will hold all known rows temporarily
    rows = []
    
    # Update rows list
    for letter in letterDict:
        # We know that letter and letter.inSameRow are all in a row
        currentRow = {letter} | letterDict[letter].inSameRow
        
        # We see if currentRow has any common letters with any entry of rows
        placed = False
        for row in rows:
            # If so, then 'currentRow' is in row with 'row' so update 'row'
            if len(currentRow & row) > 0:
                row |= currentRow
                placed = True
        # Otherwise currentRow becomes its own new row
        if placed == False:
            rows.append(currentRow)

    # Now that rows is complete, fix letterDict
    for letter in letterDict:
        for row in rows:
            if letter in row:
                letterDict[letter].inSameRow = row - {letter}
    
# Mutatingly changes letterDic so that all letters in same col are listed
# (See consolidateRowColParners for more in-depth explanation)
def consolidateColPartners(letterDict):
    # This will hold all known cols temporarily
    cols = []
    
    # Update cols list
    for letter in letterDict:
        # We know that letter and letter.inSameCol are all in a col
        currentCol = {letter} | letterDict[letter].inSameCol
        
        # We see if currentCol has any common letters with any entry of cols
        placed = False
        for col in cols:
            # If so, then 'currentCol' is in column with 'col' so update 'col'
            if len(currentCol & col) > 0:
                col |= currentCol
                placed = True
        # Otherwise currentCol becomes its own new col
        if placed == False:
            cols.append(currentCol)

    # Now that cols is complete, fix letterDict
    for letter in letterDict:
        for col in cols:
            if letter in col:
                letterDict[letter].inSameCol = col - {letter}
    
    










# Finds pairs that must be in rectangles or in rows / columns
# Adds row and column partners to letterDict (mutates letterDict)
# Returns rowsOrCols, a set of strings that appear either in rows or cols
def findOrderedRowsCols(digraphMap, letterDict):
    rowsOrCols = findSimpleRowsOrCols(digraphMap)
    
    for key in digraphMap:
        value = digraphMap[key]
        revdValue = value.reverse()

        # Look for digraphs of which we know encryption and decryption
        if value in digraphMap or revdValue in digraphMap:
            digraph1, digraph2 = key, value
            if value in digraphMap:
                digraph3 = digraphMap[value]
            else: # So revdValue in digraphMap
                # Using fact that if BA -> DC then AB -> CD no matter what
                revdDigraph3 = digraphMap[revdValue]
                digraph3 = revdDigraph3.reverse()
                
            dealWithRectangles(digraph1, digraph2, digraph3, letterDict)

            # Check for letters in same row/col (AB -> CD -> EA) then row/col 
            # BDACE or (AB -> CD -> BE) then row/col ACBDE
            if digraph3.let2 == digraph1.let1:
                rowsOrCols.add(digraph1.let2 + digraph2.let2 + 
                                digraph1.let1 + digraph2.let1 + digraph3.let1)
            elif digraph3.let1 == digraph1.let2:
                rowsOrCols.add(digraph1.let1 + digraph2.let1 + digraph3.let1 +
                                digraph2.let2 + digraph3.let2)
            
    # Removes rows or cols with no information       
    delUnneededRowsOrCols(rowsOrCols)
    return rowsOrCols


# Finds digraph pairs that must be consecutive in a row or column 
# Example if AB -> BC then have row ABC
# Helper for findRectOrRowPairs
def findSimpleRowsOrCols(digraphMap):
    # Initialized as list to make looping through easier, will become set
    rowsOrCols = []

    # Look for plain-cipher pairs that must encrypt in row or col
    for plain in digraphMap:
        cipher = digraphMap[plain]
        
        # IF AB -> BC then row or col is ABC
        if cipher.let1 == plain.let2:
            rowsOrCols.append(plain.let1 + plain.let2 + cipher.let2)
        # Else if BA -> CB then row or col is ABC
        elif cipher.let2 == plain.let1:
            rowsOrCols.append(plain.let2 + plain.let1 + cipher.let1)

    # Combine all strings that are in the same row
    # For example ABC and BCD must be in same row, so becomes ABCD
    rowsOrCols = set(combineRowsCols(rowsOrCols))
    
    return rowsOrCols

# If digraphs are in rectangle, updates row and column partners
def dealWithRectangles(digraph1, digraph2, digraph3, letterDict):
    # Check for digraphs in rectanlge (AB -> CD -> AB)
    if digraph1 == digraph3:   
        # Then A and D are in column, and B and C are in column
        # (Also have row A/C and B/D but this has already been added)
        letterDict[digraph1.let1].inSameCol.add(digraph2.let2)
        letterDict[digraph2.let2].inSameCol.add(digraph1.let1)
        letterDict[digraph1.let2].inSameCol.add(digraph2.let1)
        letterDict[digraph2.let1].inSameCol.add(digraph1.let2)


# Combine all sequences in the same row
# For example ABC and BCD can combine into ABCD 
# Helper for findSimpleRowsOrCols
def combineRowsCols(rowsOrCols):
   
    # Loop through pairs in list (done with 'while' because list mutates)
    i = 0
    while i < len(rowsOrCols):
        rowOrCol1 = rowsOrCols[i]
        # Keeps tracks of whether rowOrCol1 was put into bigger string
        combined = False
        
        j = i+1
        while j < len(rowsOrCols):
            rowOrCol2 = rowsOrCols[j]

            # In form rowOrCol = CD... and rowOrCol2 = ...CD. 
            # Puts ...CD... at end of list and removes CD...
            if rowOrCol1[:2] == rowOrCol2[-2:]:
                rowsOrCols.append(rowOrCol2 + rowOrCol1[2:])
                rowsOrCols.pop(j)
                combined = True
                
            # In form rowOrCol = ...CD and rowOrCol2 = CD... Makes ...CD...
            elif rowOrCol1[-2:] == rowOrCol2[:2]:
                rowsOrCols.append(rowOrCol1 + rowOrCol2[2:])
                rowsOrCols.pop(j)
                combined = True
           
            else:  # Only increment if nothing was popped   
                j += 1
        
        if combined == True:
            rowsOrCols.pop(i)
        else: # Once again, only increment if not popped
            i += 1
            
    return rowsOrCols



# Removes rows/cols that are subsets of longer known row/col segments
# Mutating method
def delUnneededRowsOrCols(rowsOrCols):
    toRemove = set()
    
    for rowOrCol1 in rowsOrCols:
        for rowOrCol2 in rowsOrCols:
            if isSubsetOf(rowOrCol1, rowOrCol2):
                toRemove.add(rowOrCol1)
                
    rowsOrCols -= toRemove
    



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



# Updates letterDict to say which letter each letter precedes and succeeds
# in either a row or a column (eg if column is ABCDE then B.succeeds={A})
# Mutating
def updatePrecSuccLetters(letterDict, rowsOrCols):
    boardDim = 5
    
    # Go through each letter, see if we have data on its row or col
    for letter in letterDict:
        for rowOrCol in rowsOrCols:
            letterLoc = rowOrCol.find(letter)
            if letterLoc == -1:
                continue

            # If the letter is in a row or col, add what it succeeds and precedes
            if letterLoc - 1 in range(len(rowOrCol)):
                letterDict[letter].succeeds.add(rowOrCol[letterLoc-1])
            if letterLoc + 1 in range(len(rowOrCol)):
                letterDict[letter].precedes.add(rowOrCol[letterLoc+1])

            # If have full row or column, can wrap around
            if len(rowOrCol) == boardDim:
                if letterLoc == 0:
                    letterDict[letter].succeeds.add(rowOrCol[-1])
                if letterLoc == boardDim - 1:
                    letterDict[letter].precedes.add(rowOrCol[0])
            



