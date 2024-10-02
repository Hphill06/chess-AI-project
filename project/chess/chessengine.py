'''
this class stores info about the chessgame, all info about the chess game
knows what moves are legal and not legal, also keeps a log
part 8 and beyond for changing to advanced check
'''

import numpy as np








class gamestate():
    def __init__(self):
        # board is 8*8 2d numpy array
        # first char repersents the color of the piece, second charachter is the type of piece
        # "--" = empty space
        '''
        self.board = np.array([
                    ["bR","bN","bB","bQ","bK","bB","bN","bR"],
                    ["bp","bp","bp","bp","bp","bp","bp","bp"],
                    ["--","--","--","--","--","bQ","--","--"],
                    ["--","--","bB","--","--","--","--","--"],
                    ["--","--","--","--","--","--","--","--"],
                    ["--","--","--","--","--","--","--","--"],
                    ["wp","wp","wp","wp","wp","wp","wp","wp"],
                    ["wR","wN","wB","wQ","wK","wB","wN","wR"],
                    ])
        '''
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ])

        self.moveFunctions = {
            'p': self.getPawnMoves,
            'R': self.getRookMoves,
            'N': self.getKnightMoves,
            'B': self.getBishopMoves,
            'Q': self.getQueenMoves,
            'K': self.getKingMoves
        }
        self.whitetomove = True
        self.movelog = []
        # keeping track of kings locals
        self.whitekingloc = (7, 4)
        self.blackkingloc = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.enPesantPos = ()  # cords for a square where en pesant is possilbe
        self.currentCaslteRights = castleRights(True, True, True, True)
        self.castlerightslog = [castleRights(self.currentCaslteRights.wks, self.currentCaslteRights.bks,
                                             self.currentCaslteRights.wqs, self.currentCaslteRights.bqs)]

    def makeMove(self, move):
        if move.pieceMoved != "--":
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.movelog.append(move)  # log the move so we can veiw later
            self.whitetomove = not self.whitetomove
            # updating the kings location
            if move.pieceMoved[1] == "K":
                if move.pieceMoved[0] == "w":
                    self.whitekingloc = (move.endRow, move.endCol)
                if move.pieceMoved[0] == "b":
                    self.blackkingloc = (move.endRow, move.endCol)
        # asking if move is pawn promo
        if move.PawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'  # grabs the color of pawn being promoted and makes it a queen
        # enpesant move
        if move.enPesantMove:
            self.board[move.startRow][move.endCol] = "--"  # caputring the pawn
        # update en pesantPos varable
        if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2:  # only on two sqr pawn advances
            self.enPesantPos = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enPesantPos = ()
        # castle moves
        if move.isCastlemove:
            if (move.endCol - move.startCol == 2):
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = "--"
            else:  # queenside castle move
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = "--"
        # updates castle rights -when rook or king move
        self.updateCastleRights(move)
        self.castlerightslog.append(castleRights(self.currentCaslteRights.wks, self.currentCaslteRights.bks,
                                                 self.currentCaslteRights.wqs, self.currentCaslteRights.bqs))

    def undoMove(self):

        if (len(self.movelog) != 0):
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whitetomove = not self.whitetomove
            if move.pieceMoved[1] == "K":  # updating the kings pos when undo move happens
                if move.pieceMoved[0] == "w":
                    self.whitekingloc = (move.startRow, move.startCol)
                if move.pieceMoved[0] == "b":
                    self.blackkingloc = (move.startRow, move.startCol)
            # undoing en pesant
            if move.enPesantMove:
                self.board[move.endRow][move.endCol] = "--"  # sets the square that the pawn laned on to blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enPesantPos = (move.endRow, move.endCol)
            # undo a 2 pawn advance
            if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2:
                self.enPesantPos = ()
            # undoing castling rights
            self.castlerightslog.pop()
            if move.isCastlemove:
                if move.endCol - move.startCol == 2:  # kingside

                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = "--"

                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = "--"

            self.currentCaslteRights = castleRights(self.castlerightslog[-1].wks, self.castlerightslog[-1].bks,
                                                    self.castlerightslog[-1].wqs, self.castlerightslog[-1].bqs)
            self.checkmate = False
            self.stalemate = False


    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCaslteRights.wks = False
            self.currentCaslteRights.wqs = False
        if move.pieceMoved == 'bK':
            self.currentCaslteRights.bks = False
            self.currentCaslteRights.bqs = False
        if move.pieceMoved == "wR":
            if (move.startRow == 7):
                if (move.startCol == 0):  # left white rook
                    self.currentCaslteRights.wqs = False
                elif (move.startCol == 7):  # right white rook
                    self.currentCaslteRights.wks = False
        if move.pieceMoved == "bR":
            if (move.startRow == 0):
                if (move.startCol == 0):  # left black rook
                    self.currentCaslteRights.bqs = False
                elif (move.startCol == 7):  # right white rook
                    self.currentCaslteRights.bks = False

    # undo caslte move

    '''	
    all moves that have checks
    '''

    def getValidMoves(self):
        tempenpesantpos = self.enPesantPos
        tempCastleRights = castleRights(self.currentCaslteRights.wks, self.currentCaslteRights.bks,
                                        self.currentCaslteRights.wqs, self.currentCaslteRights.bqs)
        # slower method
        # 1 gen all pos moves
        moves = self.getAllMoves()
        if self.whitetomove:
            self.getCastleMoves(self.whitekingloc[0], self.whitekingloc[1], moves)
        else:
            self.getCastleMoves(self.blackkingloc[0], self.blackkingloc[1], moves)
        # 2 for each move make the move
        for i in range(len(moves) - 1, -1, -1):  # when removing things from a list start from the end

            self.makeMove(moves[i])
            self.whitetomove = not self.whitetomove  # must switch move turn before calling ischeck
            if self.isCheck():
                moves.remove(moves[i])
            self.whitetomove = not self.whitetomove
            self.undoMove()

        if len(moves) == 0:
            if self.isCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.stalemate = False
            self.checkmate = False
        self.enPesantPos = tempenpesantpos
        self.currentCaslteRights = tempCastleRights
        return moves

    # determens if cur player is in check
    def isCheck(self):

        if self.whitetomove:
            return self.sqrUnderattk(self.whitekingloc[0], self.whitekingloc[1])
        else:
            return self.sqrUnderattk(self.blackkingloc[0], self.blackkingloc[1])

    # determens if
    def sqrUnderattk(self, r, c):
        self.whitetomove = not self.whitetomove  # switches to opp turn
        oppmoves = self.getAllMoves()
        self.whitetomove = not self.whitetomove
        for move in oppmoves:
            # r = king loc[0] c = kingloc[1]
            if move.endRow == r and move.endCol == c:  # square is under attack
                return True
        return False

    '''
    all moves without considering checks
    '''

    def getAllMoves(self):
        moves = []
        for r in range(len(self.board)):  # could use chessmain.DIMENSIONS as well
            for c in range(len(self.board[r])):  # number of col in row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whitetomove) or (turn == 'b' and not self.whitetomove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)

        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whitetomove:  # white pawn moves
            if self.board[r - 1][c] == "--":  # 1 square pawn advance
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r - 2, c), self.board))
            # white taking to the left
            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r - 1, c - 1) == self.enPesantPos:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isenpesantmove=True))
            # white taking to the right
            if c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.enPesantPos:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isenpesantmove=True))

        else:  # black pawn moves
            if self.board[r + 1][c] == "--":  # 1 square pawn advance
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r + 2, c), self.board))
            # black taking to the left
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r + 1, c - 1) == self.enPesantPos:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isenpesantmove=True))
            # black taking to the right
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r + 1, c + 1) == self.enPesantPos:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isenpesantmove=True))

    def getRookMoves(self, r, c, moves):
        posdirections = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up left down right
        enycol = "b" if self.whitetomove else "w"
        for d in posdirections:
            for i in range(1, 8):
                endrow = r + d[0] * i
                endcol = c + d[1] * i
                if 0 <= endrow < 8 and 0 <= endcol < 8:
                    endpc = self.board[endrow][endcol]
                    if endpc == "--":
                        moves.append(Move((r, c), (endrow, endcol), self.board))

                    elif endpc[0] == enycol:
                        moves.append(Move((r, c), (endrow, endcol), self.board))

                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        Nmoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        alycol = "w" if self.whitetomove else "b"
        for i in Nmoves:
            endRow = r + i[0]
            endCol = c + i[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != alycol:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        posdirections = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enycol = "b" if self.whitetomove else "w"
        for d in posdirections:
            for i in range(1, 8):
                endrow = r + d[0] * i
                endcol = c + d[1] * i
                if 0 <= endrow < 8 and 0 <= endcol < 8:
                    endpc = self.board[endrow][endcol]
                    if endpc == "--":
                        moves.append(Move((r, c), (endrow, endcol), self.board))
                    elif endpc[0] == enycol:
                        moves.append(Move((r, c), (endrow, endcol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)
        '''
        posdirections = ((-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(0,-1),(1,0),(0,1))
        enycol = "b" if self.whitetomove else "w"
        for d in posdirections:
            for i in range(1,8):
                endrow = r + d[0] *i
                endcol = c + d[1] *i
                if 0<= endrow < 8 and 0 <= endcol < 8:
                    endpc = self.board[endrow][endcol]
                    if endpc == "--":
                        moves.append(Move((r,c),(endrow,endcol),self.board))
                    elif endpc[0] == enycol:
                        moves.append(Move((r,c),(endrow,endcol),self.board))
                        break
                    else:
                        break
                else:
                    break
        '''

    def getKingMoves(self, r, c, moves):
        Nmoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        alycol = "w" if self.whitetomove else "b"
        for i in Nmoves:
            endRow = r + i[0]
            endCol = c + i[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != alycol:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getCastleMoves(self, r, c, moves):
        if self.sqrUnderattk(r, c):
            return  # cant castle while in check
        if (self.whitetomove and self.currentCaslteRights.wks) or (
                not self.whitetomove and self.currentCaslteRights.bks):
            self.getkingsideCaslteMoves(r, c, moves)
        if (self.whitetomove and self.currentCaslteRights.wqs) or (
                not self.whitetomove and self.currentCaslteRights.bqs):
            self.getqueensidecastlemoves(r, c, moves)

    def getkingsideCaslteMoves(self, r, c, moves):
        if (self.board[r][c + 1] == "--" and self.board[r][c + 2] == "--"):
            if not self.sqrUnderattk(r, c + 1) and not self.sqrUnderattk(r, c + 2):
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove=(True, "ksm")))

    def getqueensidecastlemoves(self, r, c, moves):
        if (self.board[r][c - 1] == "--" and self.board[r][c - 2] == "--" and self.board[r][c - 3] == "--"):
            if not self.sqrUnderattk(r, c - 1) and not self.sqrUnderattk(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=(True, "qsm")))


'''
add a move getter method that just takes those pos directions 
as well as row and col to make it a bit faster i think
can only use for rook bishop and queen i think
'''


class castleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move():
    def __init__(self, startSq, endSq, board, isenpesantmove=False, isCastleMove=(False, 00)):
        self.ranksToRows = {
            "1": 7,
            "2": 6,
            "3": 5,
            "4": 4,
            "5": 3,
            "6": 2,
            "7": 1,
            "8": 0,
        }
        self.rowsToRanks = {v: k for k, v in self.ranksToRows.items()}
        self.filesToCols = {
            "a": 0,
            "b": 1,
            "c": 2,
            "d": 3,
            "e": 4,
            "f": 5,
            "g": 6,
            "h": 7,
        }
        self.colsToFiles = {v: k for k, v in self.filesToCols.items()}

        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        try:
            self.pieceCaptured = board[self.endRow][self.endCol]
        except IndexError:
            self.pieceCaptured = "--"
        # pawn promotion
        self.PawnPromotion = (
                (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7))
        # en pesant
        self.enPesantMove = isenpesantmove
        if self.enPesantMove:
            try:
                self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
            except IndexError:
                self.pieceCaptured = "-1"

        # castle move
        self.isCastlemove = isCastleMove[0]
        self.kindcastlemove = isCastleMove[1]

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''
    overriding 
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def notation1(self):
        try:
            if self.isCastlemove:
                if (self.kindcastlemove == "ksm"):
                    return "0-0"
                else:
                    return "0-0-0"
            if (self.pieceCaptured.__eq__('--')) and (not self.pieceMoved[1] == 'p'):
                return str(self.pieceMoved[1]) + str(self.colsToFiles[self.endCol]) + "" + str(
                    self.rowsToRanks[self.endRow])
            elif self.pieceMoved[1] == 'p':
                if (not self.pieceCaptured.__eq__('--')):

                    return str(self.colsToFiles[self.startCol]) + "x" + str(self.colsToFiles[self.endCol]) + "" + str(
                        self.rowsToRanks[self.endRow])
                else:
                    return str(self.colsToFiles[self.endCol]) + str(self.rowsToRanks[self.endRow])
            else:
                return str(self.pieceMoved[1]) + "x" + str(self.colsToFiles[self.endCol]) + str(
                    self.rowsToRanks[self.endRow])
        except KeyError:
            pass
