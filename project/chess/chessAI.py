import random
import os


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


pieceValue = {
    'K': 9999,
    'Q': 9,
    'R': 5,
    'N': 3,
    'B': 4,
    'p': 1
}
checkmate = 1000
stalemate = 0
#IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT 
#IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT 

DEPTH = 10
#above is the amount of moves ahead the chess ai will look, so if you 
#adjust it too high it will take longer to run based off your pcs specs
#IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT 
#IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT 

def findRandomMove(validMoves):  # gets a random move
    return validMoves[random.randint(0, len(validMoves) - 1)]


def findBestMove(gs, validMoves):
    turnMulti = 1 if gs.whitetomove else -1
    oppMinMaxScore = checkmate

    bestPlayerMove = None
    random.shuffle(validMoves)

    for plymove in validMoves:
        gs.makeMove(plymove)
        opponentMoves = gs.getValidMoves()
		
        if gs.stalemate:
            oppMaxScore = stalemate
        elif gs.checkmate:
            oppMaxScore = -checkmate
        else:
            oppMaxScore = -checkmate
            for oppmoves in opponentMoves:
                gs.makeMove(oppmoves)
                gs.getValidMoves()
                if gs.checkmate:
                    score = checkmate
                elif gs.stalemate:
                    score = stalemate
                else:
                    score = -turnMulti * scoreMat(gs.board)
                if score > oppMaxScore:
                    oppMaxScore = score
                gs.undoMove()
        if oppMaxScore < oppMinMaxScore:
            oppMinMaxScore = oppMaxScore
            bestPlayerMove = plymove
        gs.undoMove()
	
    return bestPlayerMove

'''
helper method to make first recursive call 
'''
def findBestMoveMinMax(gs,validMoves):
    global nextMove
    nextMove = None
    findmoveMinMax(gs,validMoves,DEPTH,gs.whitetomove)
    return nextMove


def findmoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMat(gs.board)
    if whiteToMove:
        maxScore = -checkmate
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findmoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = checkmate
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findmoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore


def scoreBoard(gs):
    if gs.checkmate:
        if gs.whitetomove:
            return -checkmate #black wins
        else:
            return checkmate #black wins
    elif gs.stalemate:
        return stalemate
    score = 0
    for r in gs.board:
        for sqr in r:
            if sqr[0] == 'w':
                score += pieceValue[sqr[1]]
            elif sqr[0] == 'b':
                score -= pieceValue[sqr[1]]
    return score


'''
score the board based on material 
'''


def scoreMat(board):
    score = 0
    for r in board:
        for sqr in r:
            if sqr[0] == 'w':
                score += pieceValue[sqr[1]]
            elif sqr[0] == 'b':
                score -= pieceValue[sqr[1]]
    return score
