# Rose Luttmer

'''
Uses backtracking to find keytable when given plaintext and ciphertext.
First places all rows and columns in an outer backtracking loop,
then places all remaining letters

Has potential to work well (hopefully?), several issues must be fixed:
1) With current settings, it is spitting out cols of length 1. That shouldn't happen.
Figure out why we are getting that, how to fix
2) Needs to be updated so that board only has one of each letter,
right now if there's a letter in a row and a col, it can be placed twice, which is bad

'''

import encryptDecrypt
import classes
import letterDictHelpers
import string
import copy

# Given plaintext and ciphertext, returns the key table used for the encoding
def crackKeyTable(plaintext, ciphertext):
    boardDim = 5 # to avoid magic number

    # Makes dictionary of what each digraph encrypts to
    digraphMap = makeDigraphMap(plaintext, ciphertext)
    
    # Make a dictionary that maps letters to letter instances that store
    # all the information about how the letter encrypts / decrypts
    letterDict, rowSet, colSet, rowOrColSet = createAndPopulateLetterDict(digraphMap)
    
    print(rowSet, colSet, rowOrColSet)

    board = [[0]*5 for _ in range(boardDim)]
    
    longestRow = findLongestRow(rowSet)
    if longestRow != None:
        board = putInRow(board, longestRow, 0, 0)
        rowSet.remove(longestRow)
        lettersPlaced = set(longestRow)
    
    return outerBacktrack(board, rowSet, colSet, rowOrColSet, digraphMap, 
                          letterDict, lettersPlaced)

    
###########################################################################
#                       Pre back-tracking Setup
###########################################################################

# Makes a dictionary of which ciphertext digraph each plaintext digraph maps to
def makeDigraphMap(plaintext, ciphertext):
    digraphMap = {}

    # Make upper, take away non-alpha chars, make all J's into I's
    plaintext = encryptDecrypt.removeNonAlphas(plaintext.upper()).replace('J', 'I')
    ciphertext = encryptDecrypt.removeNonAlphas(ciphertext.upper())

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
        plainDigraph = classes.Digraph(plainChar1, plainChar2)

        cipherChar1 = ciphertext[i]
        cipherChar2 = 'X' if (i+1 >= len(ciphertext)) else ciphertext[i+1]
        cipherDigraph = classes.Digraph(cipherChar1, cipherChar2)

        digraphMap[plainDigraph] = cipherDigraph
    
    return digraphMap

# Creates a letter dictionary which maps letters to Letter instances
# These instances have letters that are encrypted to, letters in same row as
# and more info
def createAndPopulateLetterDict(digraphMap):
    letterDict = letterDictHelpers.makeEmptyLetterDict()

    letterDictHelpers.addEncryptsTo(digraphMap, letterDict)

    # These are rows/cols but if two letters from a segment here are in the 
    # same row, then the whole thing is in a row
    rowsOrCols = letterDictHelpers.findOrderedRowsCols(digraphMap, letterDict)

    # Normalizes information in .inSameRow and .inSameCol instances
    letterDictHelpers.consolidateRowColPartners(letterDict)

    rows, cols = findStrictRowsCols(letterDict, rowsOrCols)

    return letterDict, rows, cols, rowsOrCols

# Finds entries in the list rowsOrCols that must either be in a row or in a co
def findStrictRowsCols(letterDict, rowsOrCols):
    rows = set()
    cols = set()

    # Loop through rows/cols, for each one check if two of its letters are
    # in the same row or column
    for rowOrCol in rowsOrCols:
        for i in range(len(rowOrCol)):
            letter1 = rowOrCol[i]
            for j in range(i+1, len(rowOrCol)):
                letter2 = rowOrCol[j]

                # Only need to check one way because it is symmetric
                if letter2 in letterDict[letter1].inSameRow:
                    rows.add(rowOrCol)
                elif letter2 in letterDict[letter1].inSameCol:
                    cols.add(letter2)
    
    # Only remove at end to not mess up looping
    rowsOrCols -= rows
    rowsOrCols -= cols
    
    return rows, cols


# Returns the longest row in the set 'rows' so that backtracking can place it
# first.
def findLongestRow(rows):
    if len(rows) == 0:
        return 0
    
    bestRow = None
    bestLength = 0

    for row in rows:
        if len(row) >= bestLength:
            bestLength = len(row)
            bestRow = row
    
    return bestRow


###########################################################################
#                    OuterBacktrack Function and Helpers
###########################################################################


# This places all row and column blocks, then once done calls an inner
# backtracking function
def outerBacktrack(board, rowSet, colSet, rowOrColSet, digraphMap, 
                   letterDict, lettersPlaced):
    print(board)
    # Base case
    if len(rowSet) + len(colSet) + len(rowOrColSet) == 0:
        return innerBacktrack(board, (0,0), letterDict, digraphMap, lettersPlaced)

    # Recursive case. Try to place a row, if none then place a col
    else:
        if len(rowSet) != 0:
            return checkPlaceSolveRow(board, digraphMap, letterDict, rowSet,
                                      colSet, rowOrColSet, lettersPlaced)

        elif len(colSet) != 0:
            return checkPlaceSolveCol(board, digraphMap, letterDict, rowSet,
                                      colSet, rowOrColSet, lettersPlaced)

        else: # we know rowsOrCols is nonepty, otherwise returned in base case
            rowOrCol = rowOrColSet.pop()

            rowSet.add(rowOrCol)
            # This function will pop entry from rowSet, which has to be
            # rowOrCol because rowSet was previously empty
            soln = checkPlaceSolveRow(board, digraphMap, letterDict, rowSet,
                                      colSet, rowOrColSet, lettersPlaced)
            
            if soln !=  None:
                return soln
            
            # If here, rowOrCol can't be a row, it must be a col
            rowSet.remove(rowOrCol)
            # So return whether there is a solution treating it as col
            colSet.add(rowOrCol)
            return checkPlaceSolveCol(board, digraphMap, letterDict, rowSet,
                                      colSet, rowOrColSet, lettersPlaced)

 
# Assumes rowSet is nonempty, removes and arbitrary rowstring
# This function loops through all places to put rowString, sees if any work
def checkPlaceSolveRow(board, digraphMap, letterDict, 
                       rowSet, colSet, rowOrColSet, lettersPlaced):
    rowString = rowSet.pop()
    newLettersPlaced = lettersPlaced | set(rowString)
    
    # Loop through starting locations
    boardDim = len(board)
    for row in range(boardDim):
        for col in range(boardDim):
            # Check that board has free spaces for row
            if not canPutRowInBoard(board, len(board), rowString, row, col):
                continue
    
            newBoard = putInRow(board, rowString, row, col)

            # Don't bother placing if not legal
            if not isLegalDigraphwise(newBoard, digraphMap, newLettersPlaced):
                continue

            soln = outerBacktrack(newBoard, rowSet, colSet, rowOrColSet, 
                                  digraphMap, letterDict, newLettersPlaced)
    
            if soln != None:
                return soln

            # Don't have to remove row from board, because board is still
            # as it was before, only newBoard changed

            # Also since still on the same row, don't have to remove or add
            # it to rowSet or rowOrColSet
        
    # If here, nothing worked. Put rowSet back to original
    rowSet.add(rowString)
    return None


# Assumes colSet is nonempty, removes and arbitrary colString
# This function loops through all places to put colString, sees if any work
def checkPlaceSolveCol(board, digraphMap, letterDict, 
                       rowSet, colSet, rowOrColSet, lettersPlaced):
    colString = colSet.pop()
    newLettersPlaced = lettersPlaced | set(colString)
    
    # Loop through starting locations
    boardDim = len(board)
    for row in range(boardDim):
        for col in range(boardDim):
            # Check that board has free spaces for row
            if not canPutColInBoard(board, len(board), colString, row, col):
                continue
    
            newBoard = putInCol(board, colString, row, col)

            # Don't bother placing if not legal
            if not isLegalDigraphwise(newBoard, digraphMap, newLettersPlaced):
                continue

            soln = outerBacktrack(newBoard, rowSet, colSet, rowOrColSet, 
                                  digraphMap, letterDict, newLettersPlaced)
    
            if soln != None:
                return soln

        
    # If here, nothing worked. Put lettersPlaced and rowSet back to original
    colSet.add(colString)
    return None
     

# Returns True if a row can be put in a board without changing any letters    
def canPutRowInBoard(board, boardDim, rowString, row, col):
    # Temporary, should be removed once know this error won't occur
    if len(rowString) > boardDim:
        print('Error, row was too long')
        return False
    
    for i in range(len(rowString)):
        currentCol = (col + i) % boardDim
        # The square either has to be empty or already contain the right letter
        # in order for the placement to be valid
        if board[row][currentCol] != 0 and board[row][currentCol] != rowString[i]:
            return False
    
    return True

# Returns True if a col can be put in a board without changing any letters    
def canPutColInBoard(board, boardDim, colString, row, col):
    # Temporary, should be removed once know this error won't occur
    if len(colString) > boardDim:
        print('Error, row was too long')
        return False
    
    for i in range(len(colString)):
        currentRow = (row + i) % boardDim
        # The square either has to be empty or already contain the right letter
        # in order for the placement to be valid
        if board[currentRow][col] != 0 and board[currentRow][col] != colString[i]:
            return False
    
    return True

# Returns new board which is old board but with row placed at specified location
# Before calling this, should call canPutRowInBoard to check legality
def putInRow(board, rowString, row, col):
    boardDim = len(board[0])
    newBoard = copy.deepcopy(board)

    # Put row in board
    for i in range(len(rowString)):
        newBoard[row][(col + i) % boardDim] = rowString[i]
    
    return newBoard
    
# Returns new board which is old board but with col placed at specified location
# Before calling this, should call canPutColInBoard to check legality
def putInCol(board, colString, row, col):
    boardDim = len(board[0])
    newBoard = copy.deepcopy(board)

    # Put row in board
    for i in range(len(colString)):
        newBoard[(row + i) % boardDim][col] = colString[i]
    
    return newBoard
    
   
# Returns False is from current board, a required digraph won't encrypt correctly
def isLegalDigraphwise(board, digraphMap, lettersPlaced):
    # Loop through digraphs in plaintext message
    for plainDigraph in digraphMap:
        plainLet1, plainLet2 = plainDigraph.let1, plainDigraph.let2
        
        # If both digraph letters have been placed, see what they encrypt to
        if plainLet1 in lettersPlaced and plainLet2 in lettersPlaced:
            solutionDigraph = encryptDecrypt.findNewDigraph(plainDigraph, board)
            solLet1, solLet2 = solutionDigraph.let1, solutionDigraph.let2
            cipherDigraph = digraphMap[plainDigraph]
            cipherLet1, cipherLet2 = cipherDigraph.let1, cipherDigraph.let2

            # If the corresponding cipher letters have been placed,
            # they must be in the same spot as the solution letters 
            if ((cipherLet1 in lettersPlaced and solLet1 != cipherLet1)
                or (cipherLet2 in lettersPlaced and solLet2 != cipherLet2)):
                return False
    return True


###########################################################################
#                    innerBacktrack Function and Helpers
###########################################################################

# This places all remaining letters (the ones not in row or col strings)
def innerBacktrack(board, lastLoc, letterDict, digraphMap, lettersPlaced):
    boardDim = len(board)

    if lastLoc == (boardDim-1, boardDim-1):
        return board

    else:
        newRow, newCol = findNewRowCol(lastLoc, boardDim)
        newLoc = newRow, newCol
        lastRow, lastCol = lastLoc
        lastLetter = board[lastRow][lastCol]

        # The spot may already be full, if so, move over one spot, try again
        if board[newRow][newCol] != 0:
            return innerBacktrack(board, newLoc, letterDict, digraphMap, lettersPlaced)
        
        # Start by trying to place letters later alphabetically than lastLetter
        for newLetter in makeLetterOrderAlpha(lastLetter, lettersPlaced):
            solution = checkPlaceSolveLetter(newLetter, board, newLoc, letterDict, digraphMap, lettersPlaced)
            if solution != None:
                return solution
        
        return None


# Finds location of next piece to place 
# (moving through board left to right, top to bottom)
def findNewRowCol(lastLoc, boardDim):
    oldRow, oldCol = lastLoc
    newRow, newCol = oldRow, oldCol + 1

    if newCol >= boardDim:
        newRow += (newCol // boardDim)
        newCol = newCol % boardDim
        
    
    return newRow, newCol


# Returns list of letters in alphabetical order after letter
# Example: letter = D, lettersPlaced = {A, F, J} returns:
# [E, G, H, I, K, ...]
def makeLetterOrderAlpha(letter, lettersPlaced):
    uppercaseLets = string.ascii_uppercase
    letterIndex = uppercaseLets.find(letter)
    newOrder = list(uppercaseLets[letterIndex+1:] + uppercaseLets[:letterIndex])

    i = 0
    while i < len(newOrder):
        if newOrder[i] in lettersPlaced:
            newOrder.pop(i)
        else:
            i += 1

    return newOrder


# Checks if legal, if so then places letter and solves from there,
# unplaces letter at end if no solution was found. Returns solution or None
def checkPlaceSolveLetter(letter, board, newLoc, letterDict, digraphMap, lettersPlaced):
    newRow, newCol = newLoc
    
    # This shouldn't happen with current setup, but have it just in case
    if letter in lettersPlaced:
        return None
    
    # Place letter
    board[newRow][newCol] = letter
    lettersPlaced.add(letter)
    
    # Check that letter obeys all info that we have
    if (isLegalLetterwise(letter, board, newLoc, letterDict, lettersPlaced) and
        isLegalDigraphwise(board, digraphMap, lettersPlaced)):
        
        solution = innerBacktrack(board, newLoc, letterDict, digraphMap, lettersPlaced)
        
        if solution != None:
            return solution

    # Undo changes if no solution   
    board[newRow][newCol] = 0
    lettersPlaced.remove(letter)    
    return None


# Checks whether the letter obeys all properties dictated by letterDict
def isLegalLetterwise(letter, board, newLoc, letterDict, lettersPlaced):
    newRow, newCol = newLoc

    # If letter's row partners have been placed, they must be in the same row
    for letter2 in letterDict[letter].inSameRow:
        if (letter2 in lettersPlaced and 
            not isInRow(newRow, letter2, board)):
            return False
    
    # If letter's col partners are placed, they must be in same col
    for letter2 in letterDict[letter].inSameCol:
        if (letter2 in lettersPlaced and
            not isInCol(newCol, letter2, board)):
            return False

    
    return True

    
# Says whether 'letter' is found in row number 'row' of 'board'
# Helper for isLegalLetterwise
def isInRow(row, letter, board):
    rowList = board[row]
    for entry in rowList:
        if entry == letter:
            return True
    
    return False

# Says whether 'letter' is in column number 'col' of board
# Helper for isLegalLetterwise
def isInCol(col, letter, board):
    rows = len(board)
    for row in range(rows):
        if board[row][col] == letter:
            return True
    
    return False

###########################################################################
#                               main
###########################################################################


def main():
    plaintext = 'This is a test I really hope it works are there enough letters here?'
    ciphertext = encryptDecrypt.encDecPlayfair(plaintext, 'object')
    print(ciphertext)

    
    print(crackKeyTable(plaintext, ciphertext))
   

main()

