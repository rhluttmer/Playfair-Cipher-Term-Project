# MUST BE FIXED


# Uses backtracking but with very brute force technique

import crackTable1
import helpers
import string
import digraphClass

def crackKeyTable(plaintext, ciphertext):
    boardDim = 5
    digraphMap = crackTable1.makeDigraphMap(plaintext, ciphertext)
    
    board = [[0]*5 for _ in range(boardDim)]
    board[0][0] = 'A'
    lettersPlaced = {'A'}
    
    return crackHelper(board, (0,0), lettersPlaced, digraphMap)

def crackHelper(board, lastLoc, lettersPlaced, digraphMap):
    #print(lettersPlaced, len(lettersPlaced))
    #print(board)
    #print(len(lettersPlaced) * 4, '%')
    #print(board)

    lastRow, lastCol = lastLoc
    
    if lastLoc == (len(board)-1, len(board[0])-1):
        return board
    
    else:
        if lastCol == len(board[0]) - 1:
            newCol = 0
            newRow = lastRow + 1
        else:
            newCol = lastCol + 1
            newRow = lastRow
        
        for letter in string.ascii_uppercase:
            if (letter not in lettersPlaced and letter != 'J'):
                # Temporarily place letter
                board[newRow][newCol] = letter
                lettersPlaced.add(letter)
                
                # Check legal placement, if legal check for solution
                if isLegal(board, digraphMap, lettersPlaced):
                    solution = crackHelper(board, (newRow, newCol), 
                                           lettersPlaced, digraphMap)
                    if solution != None:
                        return solution
                
                # If it wasn't legal or there was no solution, undo placement
                lettersPlaced.remove(letter)
                board[newRow][newCol] = 0
        
        return None

# Returns False is from current board, a required digraph won't encrypt correctly
def isLegal(board, digraphMap, lettersPlaced):
    # Loop through digraphs in plaintext message
    for plainDigraph in digraphMap:
        plainLet1, plainLet2 = plainDigraph.let1, plainDigraph.let2

        # If both digraph letters have been placed, see what they encrypt to
        if plainLet1 in lettersPlaced and plainLet2 in lettersPlaced:
            solutionDigraph = helpers.findNewDigraph(plainDigraph, board)
            solLet1, solLet2 = solutionDigraph.let1, solutionDigraph.let2
            cipherDigraph = digraphMap[plainDigraph]
            cipherLet1, cipherLet2 = cipherDigraph.let1, cipherDigraph.let2

            # If the corresponding cipher letters have been placed,
            # they must be in the same spot as the solution letters 
            if ((cipherLet1 in lettersPlaced and solLet1 != cipherLet1)
                or (cipherLet2 in lettersPlaced and solLet2 != cipherLet2)):
                return False
    return True



def main():
    plaintext = 'LATELYIVEBEXNXNOTICINGHOWMYSENTENCESHAVEATENDENCYTOKEXPGOINGWHENIWRITETHEMONSCREXNTHISGOESFORCONCENTRATEDWRITINGASWELXASCORXESPONDENCETWAINPROBABLYBELIEVEDTHATCORRESPONDENCEINANIDEALWORLDALSODEMANDSCONCENTRATIONBUTHENEVERUSEDEMAILLASTWEEKICAUGHTMYSELFPACKINGFOURCONIUNCTIONSINTOATHREXLINESENTENCEINANEMAILTHATSINEXCUSABLESINCETHENIHAVETRIEDTOESCHEWCONIUNCTIONSWHENEVERPOSXSIBLEGONEARETHECOMMASTHEANDSBUTSANDSOSINARESTACXATODECLARATIVESBETXERTOREADLIKEBADHEMINGWAYTHANBADFAULKNER'
    ciphertext = 'TDNADLTXACCZIZTURLHCRMFQZGLYMENAIEDUFCZAFAMEEAIEVLSFCZWPQTRMXGMERXILNAIFMUUTQDNBZIIFLQFPDUOVIBUTDATRTBNABYILRLRMDOZBIYDOAQIWDUQPLEMEDARVCTRUTPCBDRWDDNNCZAALFCIAPTNBUQUTEAIECNTETLEADTVPINEBDYSAMUETKYAQIEMERIFATQREONMCEMZANPUDEAFELNTDOLZBDMCHEOHKNFLYDNGOBDHLRMOVPNAQTLZEAITQLULTAVFAGICZNLEMUDTRMEDALTETMUCTNRFCLOLTCZEQODDRDULTDAIFMECQFTANILAEAVDUHQBZAQTLZEAITQLUXGMEAZBNQPQYQLDRBMUTABNBIFADUFFEOLMCETKYEPLOETKYPULTBTDUAFHIFASAADTDTBRLZAPDANZCIRPTABKDLHACBEMCHNRMVBVLFCREBEOFSNMLBN'
    #digraphMap = crackTable1.makeDigraphMap(plaintext, ciphertext)
    #print(digraphMap)
    print(crackKeyTable(plaintext, ciphertext))


main()

