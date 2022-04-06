import encryptDecrypt
import classes
import letterDictHelpers


def crackKeyTable(plaintext, ciphertext):
    boardDim = 5

    # Makes dictionary of what each digraph encrypts to
    digraphMap = makeDigraphMap(plaintext, ciphertext)
    
    # Make a dictionary that maps letters to letter instances that store
    # all the information about how the letter encrypts / decrypts
    letterDict = createAndPopulateLetterDict(digraphMap)

    board = [[0]*5 for _ in range(boardDim)]
    firstToPlace = findLetterWithMostInfo(letterDict)
    board[0][0] = firstToPlace
    lettersPlaced = {firstToPlace}

    return crackTableHelper(board, (0,0), letterDict, lettersPlaced)

def crackTableHelper(board, lastLoc, letterDict, lettersPlaced):
    lastRow, lastCol = lastLoc
    
    if lastLoc == (len(board)-1, len(board[0])-1):
        return board
    else:
        pass
    # TO DO : left off here - finish

# Makes a dictionary of which ciphertect digraph each plaintext digraph maps to
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

    letterDictHelpers.updateProcSuccLetters(letterDict, rowsOrCols)

    return letterDict


def findLetterWithMostInfro(letterDict):
    mostInfo = 0 
    bestLetter = None

    for letter in letterDict:
        letterInfo = letter.amountOfInfo()
        if letterInfo >= mostInfo:
            bestLetter, mostInfo = letter, letterInfo
    
    return bestLetter


def main():
    
    plaintext = 'EX AM PL EA QU IC KB RO WN FO XI UM PS OV ER TH EL AZ YD OG AB MX AC DB'
    ciphertext = 'CZ BL LM AB RQ HD GE TM XM IL YH RP NU LY BU SI AP EV DI MI BC NW BD EC'
    
    crackKeyTable(plaintext, ciphertext)


    '''
    digraphMap = makeDigraphMap(plaintext, ciphertext)

    letterDict = makeEmptyLetterDict()
    addEncryptsTo(digraphMap, letterDict)
    print()
    print(letterDict)
    print()

    makeRowPartners(letterDict)
    print(letterDict)
    '''
    
    '''
    rectangles, rowsOrCols = findRectOrRowPairs(digraphMap)
    print(rowsOrCols)
    print(makeRowPartners(rows))
    '''
    

main()

