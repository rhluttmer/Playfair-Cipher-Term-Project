# Rose Luttmer

'''
Finds key table from input of plaintext and ciphertext.

Attempts to be more efficient than 'badCrackTable' by being more
selective in how letters are placed. However, even though I gather a lot of
info about the digraphs at the begginning, not all of it is used. THe program
ultimately takes much too long to run. 
 '''

import encryptDecrypt
import classes
import letterDictHelpers
import string

# Given plaintext and ciphertext, returns the key table used for the encoding
def crackKeyTable(plaintext, ciphertext):
    boardDim = 5 # to avoid magic number

    # Makes dictionary of what each digraph encrypts to
    digraphMap = makeDigraphMap(plaintext, ciphertext)
    
    # Make a dictionary that maps letters to letter instances that store
    # all the information about how the letter encrypts / decrypts
    letterDict = createAndPopulateLetterDict(digraphMap)
    
    for letter in letterDict:
        print(letterDict[letter])

    board = [[0]*5 for _ in range(boardDim)]
    firstToPlace = findLetterWithMostInfo(letterDict)
    board[0][0] = firstToPlace
    lettersPlaced = {firstToPlace}

    return crackTableHelper(board, (0,0), letterDict, digraphMap, lettersPlaced)

# Backtracking function to find the table
def crackTableHelper(board, lastLoc, letterDict, digraphMap, lettersPlaced):
    print(board)
    boardDim = len(board)
    
    if lastLoc == (boardDim-1, boardDim-1):
        return board
    else:
        newRow, newCol = findNewRowCol(lastLoc, boardDim)
        newLoc = newRow, newCol
        lastRow, lastCol = lastLoc
        lastLetter = board[lastRow][lastCol]
        
        # This backtracking doesn't always do things perfectly chronologically
        # If this spot is already full, just move one spot over and try again
        if board[newRow][newCol] != 0:
            return crackTableHelper(board, newLoc, letterDict, digraphMap, lettersPlaced)
        
        # Start by trying to place letters that succeed lastLatter
        for newLetter in makeLetterOrder(lastLetter, letterDict):
            solution = placeCheckUnplace(newLetter, board, newLoc, letterDict, digraphMap, lettersPlaced)
            if solution != None:
                return solution
        
        return None
     

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
    letterDictHelpers.makeRowPartners(letterDict)

    rowsOrCols = letterDictHelpers.findOrderedRowsCols(digraphMap, letterDict)

    letterDictHelpers.updatePrecSuccLetters(letterDict, rowsOrCols)

    return letterDict



# Decides which letter to place first by seeing which instance has the most info
def findLetterWithMostInfo(letterDict):
    mostInfo = 0 
    bestLetter = None

    for letter in letterDict:
        letterInfo = letterDict[letter].amountOfInfo()
        if letterInfo >= mostInfo:
            bestLetter, mostInfo = letter, letterInfo
    
    return bestLetter

# Finds location of next piece to place 
# (moving through board left to right, top to bottom)
def findNewRowCol(lastLoc, boardDim):
    oldRow, oldCol = lastLoc
    newRow, newCol = oldRow, oldCol + 1

    if newCol >= boardDim:
        newRow += (newCol // boardDim)
        newCol = newCol % boardDim
        
    
    return newRow, newCol


# Decide which order to search in
def makeLetterOrder(letter, letterDict):
    letterInst = letterDict[letter]
    priority1 = letterInst.precedes
    
    priority2 = letterInst.inSameRow - priority1
    priority3 = letterInst.encryptsTo - priority2 - priority1
    leftovers = set(string.ascii_uppercase) - priority3 - priority2 - priority1

    return (sorted(priority1) + sorted(priority2) + 
            sorted(priority3) + sorted(leftovers))

# Checks if legal, if so then places letter and solves from there,
# unplaces letter at end if no solution was found
def placeCheckUnplace(letter, board, newLoc, letterDict, digraphMap, lettersPlaced):
    newRow, newCol = newLoc
    if letter in lettersPlaced:
        # print('already placed', lettersPlaced)
        return None
    
    board[newRow][newCol] = letter
    lettersPlaced.add(letter)
    
    if (isLegalLetterwise(letter, board, newLoc, letterDict, lettersPlaced) and
        isLegalDigraphwise(board, digraphMap, lettersPlaced)):
        # print('passed legality')
        solution = crackTableHelper(board, newLoc, letterDict, digraphMap, lettersPlaced)
        
        if solution != None:
            return solution
        
    board[newRow][newCol] = 0
    lettersPlaced.remove(letter)    
    return None

# Checks whether the letter obeys all properties dictated by letterDict
def isLegalLetterwise(letter, board, newLoc, letterDict, lettersPlaced):
    newRow, newCol = newLoc
    boardDim = len(board)

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

    # If there happened to be any letters placed, they need to be good
    succeedingRowLetter = board[(newRow + 1) % boardDim][newCol]
    if (succeedingRowLetter != 0 and 
        succeedingRowLetter not in letterDict[letter].precedes):
        return False
    succeedingColLetter = board[newRow][(newCol+1) % boardDim]
    if (succeedingColLetter != 0 and 
        succeedingColLetter not in letterDict[letter].precedes):
        return False
    
    return True

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

    
# Says whether 'letter' is found in row number 'row' of 'board'
def isInRow(row, letter, board):
    rowList = board[row]
    for entry in rowList:
        if entry == letter:
            return True
    
    return False

# Says whether 'letter' is in column number 'col' of board
def isInCol(col, letter, board):
    rows = len(board)
    for row in range(rows):
        if board[row][col] == letter:
            return True
    
    return False



def main():
    
    plaintext = 'EX AM PL EA QU IC KB RO WN FO XI UM PS OV ER TH EL AZ YD OG AB MX AC DB'
    ciphertext = 'CZ BL LM AB RQ HD GE TM XM IL YH RP NU LY BU SI AP EV DI MI BC NW BD EC'
    
    print(crackKeyTable(plaintext, ciphertext))
    '''
    digraphMap = makeDigraphMap(plaintext, ciphertext)
    letterDict = createAndPopulateLetterDict(digraphMap)
    print(makeLetterOrder('A', letterDict))
    print(len(makeLetterOrder('A', letterDict)))
    '''

    
    

main()

