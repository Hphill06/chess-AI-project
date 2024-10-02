import chessengine
import chessopen
import chessAi

import numpy as np
import pygame as p






WIDTH = HEIGHT = 512# resolution of img
DIMENSIONS = 8
SQ_SIZE = HEIGHT / DIMENSIONS
MAX_FPS = 1
IMAGES = {}

'''
first thing to do is load images from the z pieces folder
'''


def loadImages():
    pieces = np.array(['wp', 'bp', "wK", "bK", "wQ", "bQ", "wB", "bB", "wR", "bR", "wN", "bN"])
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('files/z pieces/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))
    # now you can call an image by using IMAGES['wP']


# this will be our main driver handles user input and updating the graphics
def endcmd(movelog):

    x1 = 0
    x2 = 1
    chessopen.open1 = movelog
    for i in movelog:
        val = x1 % 2
        if (val == 0):
            print(str(x2) + "." + i.notation1(), end=" ")
            x2 += 1
        else:
            print(i.notation1())
        x1 += 1

    chessopen1 = chessopen.chessopen(movelog)
    print(chessopen1.correctopen)


def main():

    p.init()
    undo = False
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessengine.gamestate()
    validMoves = gs.getValidMoves()
    moveMade = False  # flag var for when a move is made
    animate = False  # flage var
    loadImages()  # only runs once
    running = True
    sqSelected = ()  # starts empty since no square has been selected keeps track of last square user clicked on
    playerClicks = []  # keeps track of user clicks (two tuples : [(3,5), (3,7)])
    gameOver = False
    player1 = False# if human is playing white this will be True, if its an ai playing white then false
    player2 = False  # same as above but for black
    while running:
        humanTurn = (gs.whitetomove and player1) or (not gs.whitetomove and player2)
        for e in p.event.get():
            if e.type == p.QUIT:
                endcmd(gs.movelog)
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()  # x y location of mouse if i add panle i need to change the SQ_SIZE value
                    col = int(location[0] / SQ_SIZE)
                    row = int(location[1] / SQ_SIZE)
                    if ((row, col) == sqSelected):
                        sqSelected = ()  # if you click on the peice twice it will undo the first click and let you selecte something else
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)  # append both clicks
                    if len(playerClicks) == 2:  # after 2nd click
                        if gs.board[playerClicks[0][0]][playerClicks[0][1]] != "--":
                            move = chessengine.Move(startSq=playerClicks[0], endSq=playerClicks[1], board=gs.board)
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMove(validMoves[i])
                                    moveMade = True
                                    animate = True
                                    sqSelected = ()
                                    playerClicks = []
                            if not moveMade:
                                playerClicks = [sqSelected]
                        sqSelected = ()
                        playerClicks = []


            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo when the z key is pressed
                    gs.undoMove()
                    undo = not undo
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_r:  # resets the board
                    gs = chessengine.gamestate()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
        # ai move finder logic
        if not gameOver and not humanTurn:
            AImove = chessAi.findBestMove(gs, validMoves)
            if AImove is None:
                AImove = chessAi.findBestMoveMinMax(validMoves)
            gs.makeMove(AImove)
            moveMade = True
            animate = False

        if moveMade:
            if animate:
                animateMove(gs.movelog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()  # in order to make the code easier on the system we only generate possilbe moves when a move is made instead of after every frame
            moveMade = not moveMade
            animate = False
        drawGameState(screen, gs, validMoves, sqSelected)
        if gs.checkmate:
            gameOver = True
            if gs.whitetomove:
                drawText(screen, "black wins by checkmate")
            else:
                drawText(screen, "white wins by checkmate")
        elif gs.stalemate:
            gameOver = True
            drawText(screen, "Stalemate")
        clock.tick(MAX_FPS)
        p.display.flip()


'''
highlights sqr selected and posible moves for a peice that is selcected
'''


def highlightSquares(screen, gs, validMoves, sqSelcted):
    if sqSelcted != ():
        r, c = sqSelcted
        if gs.board[r][c][0] == ("w" if gs.whitetomove else 'b'):  # sqselcted is a peice that can be moved
            # highlights the selcted square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(150)  # transparancy value 0  -> transparent 255 -> solid
            s.fill(p.Color("black"))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            # highlight pos moves from that square
            s.fill(p.Color('black'))
            for i in validMoves:
                if (i.startRow == r and i.startCol == c):
                    screen.blit(s, (SQ_SIZE * i.endCol, SQ_SIZE * i.endRow))


'''
responsable for all of the graphics 
'''


def drawGameState(screen, gs, validMoves, sqSelcted):
    drawBoard(screen)  # draws the squares on the board
    highlightSquares(screen, gs, validMoves, sqSelcted)
    drawPieces(screen, gs.board)  # draws pieces ontop of squares


'''
draws the board squares
'''


def drawBoard(screen):
    global colors
    colors = [p.Color('light gray'), p.Color("dark gray")]
    for row in range(DIMENSIONS):
        for col in range(DIMENSIONS):
            color = colors[((row + col) % 2)]
            p.draw.rect(screen, color, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
draws the peices on the board using the current gamestate.board
'''


def drawPieces(screen, board):
    for row in range(DIMENSIONS):
        for col in range(DIMENSIONS):
            piece = board[col][row]
            if (not piece.__eq__("--")):
                screen.blit(IMAGES[piece], p.Rect(row * SQ_SIZE, col * SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
handles moving with animation
'''


def animateMove(move, screen, board, clock):
    global colors

    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 1# frames it takes for a peice to move one square of an animation
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erace peice that is being moved
        col = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, col, endSquare)
        # draw captured peice onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw the moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 30, True, False)
    textObject = font.render(text, True, p.Color("grey"))
    textloc = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObject.get_width() / 2,
                                               HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textloc)
    textObject = font.render(text, True, p.Color("black"))
    screen.blit(textObject, textloc.move(-2, -2))


if __name__ == "__main__":
    main()



