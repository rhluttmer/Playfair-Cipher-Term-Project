# Rose Luttmer

'''
Uses backtracking to find keytable when given plaintext and ciphertext.
First places all rows and columns in an outer backtracking loop,
then places all remaining letters
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
    
    # If there was an error, would return string describing error instead of
    # actual dictionary. In this case we return error message and stop
    if isinstance(digraphMap, str):
        return digraphMap

    # Make a dictionary that maps letters to letter instances that store
    # all the information about how the letter encrypts / decrypts
    letterDict, rowSet, colSet, rowOrColSet = createAndPopulateLetterDict(digraphMap)

    # LetterDict is only a string if there was an error
    if isinstance(letterDict, str):
        return letterDict
    
    board = [[0] * boardDim for _ in range(boardDim)] # Make empty board
    
    # Start by placing the longest row or column, if there is one
    longestRow, longRowLen = findLongestString(rowSet)
    longestCol, longColLen = findLongestString(colSet)

    # If the longest row is longer than longest col
    if longRowLen >= longColLen and longRowLen != 0:
        board = putInRow(board, longestRow, 0,0)
        rowSet.remove(longestRow)
        lettersPlaced = set(longestRow)
    # If longest col is longer (but nonzero)
    elif longColLen > longRowLen:
        board = putInCol(board, longestCol, 0,0)
        colSet.remove(longestCol)
        lettersPlaced = set(longestCol)
    # If rowset and colset are empty
    else:
        lettersPlaced = set()
    

    solution = outerBacktrack(board, rowSet, colSet, rowOrColSet, digraphMap, 
                              letterDict, lettersPlaced)
    

    if solution == None:
        return "There was no solution !!!"
    else:
        return formatSolution(solution)

    
###########################################################################
#                       Pre back-tracking Setup
###########################################################################

# Makes a dictionary of which ciphertext digraph each plaintext digraph maps to
def makeDigraphMap(plaintext, ciphertext):
    digraphMap = {}

    # Make upper, take away non-alpha chars, make all J's into I's
    plaintext = encryptDecrypt.removeNonAlphas(plaintext.upper()).replace('J', 'I')
    ciphertext = encryptDecrypt.removeNonAlphas(ciphertext.upper())

    # This way won't try to run if texts aren't compatible
    if abs(len(plaintext) - len(ciphertext)) > 1:
        return "Inputs not compatible !!!"

    # Loop through digraphs
    for i in range(0, len(plaintext), 2):
        plainChar1 = plaintext[i]
        # Add 'X' if needed
        if i + 1 >= len(plaintext) or plaintext[i+1] == plainChar1:
            plainChar2 = 'X'
        else:
            plainChar2 = plaintext[i+1]
        plainDigraph = classes.Digraph(plainChar1, plainChar2)
        
        # Add 'X' to pad
        cipherChar1 = ciphertext[i]
        cipherChar2 = 'X' if (i+1 >= len(ciphertext)) else ciphertext[i+1]
        cipherDigraph = classes.Digraph(cipherChar1, cipherChar2)

        # In playfair, a digraph always encrypts to same thing, so if
        # digraph is encrypting to two different things, something's wrong
        if plainDigraph in digraphMap and cipherDigraph != digraphMap[plainDigraph]:
            return f'Error {plainDigraph} becomes {digraphMap[plainDigraph]} & {cipherDigraph}!'
        
        digraphMap[plainDigraph] = cipherDigraph

        # Deals with if two plaintext digraphs map to same key
        keysToCipher = inverseDictionary(digraphMap, cipherDigraph)
        if len(keysToCipher) >= 2:
            plain1 = keysToCipher.pop()
            plain2 = keysToCipher.pop()
            return f"Error{plain1}&{plain2} map to {cipherDigraph}!!!!!"
            # This has werid spacing to look better on 5x5 grid
    
        
    
    return digraphMap


# Finds all keys that have a certain value
def inverseDictionary(dictionary, value):
    keys = set()
    for key in dictionary:
        if dictionary[key] == value:
            keys.add(key)

    return keys


# Creates a letter dictionary which maps letters to Letter instances
# These instances have letters that are encrypted to, letters in same row as
# and more info
def createAndPopulateLetterDict(digraphMap):
    letterDict = letterDictHelpers.makeEmptyLetterDict()

    temp = letterDictHelpers.addEncryptsTo(digraphMap, letterDict)

    # Will return an error if a letter encrypts to itself
    if temp != None:
        return temp, None, None, None
    
    # Adds some letters that must be in same row
    letterDictHelpers.makeRowPartners(letterDict)

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
                    cols.add(rowOrCol)
    
    # Only remove at end to not mess up looping
    rowsOrCols -= rows
    rowsOrCols -= cols
    
    return rows, cols


# Returns the longest string in the set so that backtracking can place it
# first.
def findLongestString(set):
    if len(set) == 0:
        return None, 0
    
    bestString = None
    bestLength = 0

    for row in set:
        if len(row) >= bestLength:
            bestLength = len(row)
            bestString = row
    
    return bestString, bestLength


###########################################################################
#                    OuterBacktrack Function and Helpers
###########################################################################


# This places all row and column blocks, then once done calls an inner
# backtracking function
def outerBacktrack(board, rowSet, colSet, rowOrColSet, digraphMap, 
                   letterDict, lettersPlaced):
    # Base case
    if len(rowSet) + len(colSet) + len(rowOrColSet) == 0:
        return innerBacktrack(board, 'start', letterDict, digraphMap, lettersPlaced)

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

            soln = checkPlaceSolveCol(board, digraphMap, letterDict, rowSet,
                                      colSet, rowOrColSet, lettersPlaced)

            if soln != None:
                return soln

            # Put the string back in place if there was no solution
            rowOrColSet.add(rowOrCol)
            colSet.remove(rowOrCol)
            return None

 
# Assumes rowSet is nonempty, removes an arbitrary rowstring
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
            if not canPutRowInBoard(board, len(board), rowString, 
                                    row, col, lettersPlaced):
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


# Assumes colSet is nonempty, removes an arbitrary colString
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
            if not canPutColInBoard(board, len(board), colString, 
                                    row, col, lettersPlaced):
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
def canPutRowInBoard(board, boardDim, rowString, row, col, lettersPlaced):
    for i in range(len(rowString)):
        currCol = (col + i) % boardDim
        # The square either has to be empty or already contain the right letter
        # in order for the placement to be valid
        if board[row][currCol] != 0 and board[row][currCol] != rowString[i]:
            return False
        
        # If 'A' is already on the board from a previous word, we can't place 
        # the 'A' in our string over an empty square (it needs to be over 'A')
        elif (rowString[i] in lettersPlaced and 
              board[row][currCol] != rowString[i]):
            return False
    
    return True


# Returns True if a col can be put in a board without changing any letters    
def canPutColInBoard(board, boardDim, colString, row, col, lettersPlaced):    
    for i in range(len(colString)):
        currCol = (row + i) % boardDim
        # The square either has to be empty or already contain the right letter
        # in order for the placement to be valid
        if board[currCol][col] != 0 and board[currCol][col] != colString[i]:
            return False
        
        # If 'A' is already on the board from a previous word, we can't place 
        # the 'A' in our string over an empty square (it needs to be over 'A')
        elif (colString[i] in lettersPlaced and 
              board[currCol][col] != colString[i]):
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
        if lastLoc == 'start':
            newRow, newCol = (0,0)
            lastLetter = 0
        else:
            newRow, newCol = findNewRowCol(lastLoc, boardDim)
            lastRow, lastCol = lastLoc
            lastLetter = board[lastRow][lastCol]
        newLoc = newRow, newCol
        

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
# Example: letter = D, lettersPlaced = {A, F, I} returns:
# [E, G, H, K, ...]
def makeLetterOrderAlpha(letter, lettersPlaced):
    uppercaseLets = string.ascii_uppercase
    
    # Deals with case when "last letter" is over an empty square (filled with 0)
    if letter == 0:
        newOrder = list(uppercaseLets)
    
    else:
        letterIndex = uppercaseLets.find(letter)
        newOrder = list(uppercaseLets[letterIndex+1:] + uppercaseLets[:letterIndex])

    i = 0
    while i < len(newOrder):
        if newOrder[i] in lettersPlaced or newOrder[i] == 'J':
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
#                              final steps
###########################################################################

# Makes grid most likely to ressemble key table. Key table starts with key
# word and then does rest of alphabet, so probably, the row with the most 
# letters at the end of the alphabet is the bottom row. So it moves this row
# to the bottom and then arranges the row so that first alphabetical letter
# is first
def formatSolution(solution):
    heaviestRow = findHeaviestRow(solution)
    solution = solution[heaviestRow + 1:] + solution[:heaviestRow + 1]

    index = indexOf1stLetterAlphabetically(solution[-1])

    for i in range(len(solution)):
        colList = solution[i]
        colList = colList[index:] + colList[:index]
        solution[i] = colList

    return solution


# Finds row whose letters are last alphabetically (A has weight 0, Z has weight
# 25, 'heaviest' row is one whose letters sum to biggest weight)
def findHeaviestRow(solution):
    heaviestRowNum = None
    heaviestWeight = 0

    for i in range(len(solution)):
        currRow = solution[i]

        currWeight = 0
        for entry in currRow:
            entryWeight = ord(entry) - ord('A')
            currWeight += entryWeight
        
        if currWeight > heaviestWeight:
            heaviestRowNum = i
            heaviestWeight = currWeight
    
    return heaviestRowNum


# Takes string as input, returns index of first letter alphabetically
def indexOf1stLetterAlphabetically(row):
    bestLetter = chr(ord('Z') + 1)
    bestLetterLoc = None

    for i in range(len(row)):
        entry = row[i]
        if entry < bestLetter:
            bestLetterLoc = i
            bestLetter = entry
    
    return bestLetterLoc

