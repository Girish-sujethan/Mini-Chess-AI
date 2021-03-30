"""
    Ahira Justice, ADEFOKUN
    justiceahira@gmail.com
"""


import os
import pygame

from . import pieces
from . import fenparser


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, 'images')


class Board:

    btile = pygame.image.load(os.path.join(IMAGE_DIR, 'btile.png'))
    wtile = pygame.image.load(os.path.join(IMAGE_DIR, 'wtile.png'))

    def __init__(self, colors, BGCOLOR, DISPLAYSURF, size=8):
        self.colors = colors
        self.BGCOLOR = BGCOLOR
        self.DISPLAYSURF = DISPLAYSURF
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)

        self.pieceRect = []

        self.boardRect, self.tile_size = self._generate_board_rect(size)

    def _generate_board_rect(self, size):

        start = 100
        end = 500
        stride = (end - start) // size
        board_rect = []

        for column in range(0, size):
            board_rect.append(tuple([(start + row * stride, start + column * stride) for row in range(0, size)]))

        return board_rect, stride

    def displayBoard(self):
        self.DISPLAYSURF.fill(self.BGCOLOR)
        pygame.draw.rect(self.DISPLAYSURF, self.colors['Black'], (95, 95, 410, 410), 10)

        self.drawTiles()


    def drawTiles(self):
        wtile = pygame.transform.scale(Board.wtile, (self.tile_size, self.tile_size))
        btile = pygame.transform.scale(Board.btile, (self.tile_size, self.tile_size))

        for i in range(1, len(self.boardRect)+1):
            for j in range(1, len(self.boardRect[i-1])+1):
                if self.isOdd(i):
                    if self.isOdd(j):
                        self.DISPLAYSURF.blit(wtile, self.boardRect[i-1][j-1])
                    elif self.isEven(j):
                        self.DISPLAYSURF.blit(btile, self.boardRect[i-1][j-1])
                elif self.isEven(i):
                    if self.isOdd(j):
                        self.DISPLAYSURF.blit(btile, self.boardRect[i-1][j-1])
                    elif self.isEven(j):
                        self.DISPLAYSURF.blit(wtile, self.boardRect[i-1][j-1])

        # draw letters
        files = 'abcdefgh'
        ranks = '12345678'
        size = len(self.boardRect)
        for i in range(0, len(self.boardRect)):

            text_surface = self.font.render(ranks[size - i - 1], True, (200, 200, 200))
            rect = self.boardRect[i][-1]
            rect = (rect[0] + self.tile_size + 20, rect[1] + 40)
            self.DISPLAYSURF.blit(text_surface, dest=rect)

        for i in range(0, len(self.boardRect)):
            text_surface = self.font.render(files[i], True, (200, 200, 200))
            rect = self.boardRect[-1][i]
            rect = (rect[0] + 40, rect[1] + self.tile_size + 15)
            self.DISPLAYSURF.blit(text_surface, dest=rect)


    def isOdd(self, number):
        if number % 2 == 1:
            return True


    def isEven(self, number):
        if number % 2 == 0:
            return True


    def drawPieces(self):
        self.mapPieces()

        for piece in self.pieceRect:
            piece.displayPiece()


    def mapPieces(self):
        for i in range(len(Board.posb)):
            if i in [0, 1, 2, 3, 4, 5, 6, 7]:
                piece = self.createPiece(pieces.BLACK, pieces.PAWN, Board.posb[i])
                self.pieceRect.append(piece)
            elif i in [8, 15]:
                piece = self.createPiece(pieces.BLACK, pieces.ROOK, Board.posb[i])
                self.pieceRect.append(piece)
            elif i in [9, 14]:
                piece = self.createPiece(pieces.BLACK, pieces.KNGHT, Board.posb[i])
                self.pieceRect.append(piece)
            elif i in [10, 13]:
                piece = self.createPiece(pieces.BLACK, pieces.BISHOP, Board.posb[i])
                self.pieceRect.append(piece)
            elif i in [11]:
                piece = self.createPiece(pieces.BLACK, pieces.QUEEN, Board.posb[i])
                self.pieceRect.append(piece)
            elif i in [12]:
                piece = self.createPiece(pieces.BLACK, pieces.KING, Board.posb[i])
                self.pieceRect.append(piece)

        for i in range(len(Board.posw)):
            if i in [0, 1, 2, 3, 4, 5, 6, 7]:
                piece = self.createPiece(pieces.WHITE, pieces.PAWN, Board.posw[i])
                self.pieceRect.append(piece)
            elif i in [8, 15]:
                piece = self.createPiece(pieces.WHITE, pieces.ROOK, Board.posw[i])
                self.pieceRect.append(piece)
            elif i in [9, 14]:
                piece = self.createPiece(pieces.WHITE, pieces.KNGHT, Board.posw[i])
                self.pieceRect.append(piece)
            elif i in [10, 13]:
                piece = self.createPiece(pieces.WHITE, pieces.BISHOP, Board.posw[i])
                self.pieceRect.append(piece)
            elif i in [11]:
                piece = self.createPiece(pieces.WHITE, pieces.QUEEN, Board.posw[i])
                self.pieceRect.append(piece)
            elif i in [12]:
                piece = self.createPiece(pieces.WHITE, pieces.KING, Board.posw[i])
                self.pieceRect.append(piece)


    def createPiece(self, color, type, position):
        piece = pieces.Piece(color, type, self.DISPLAYSURF, self.tile_size)
        piece.setPosition(position)
        return piece


    def updatePieces(self, fen):
        self.pieceRect = []
        fp = fenparser.FenParser(fen)
        fenboard = fp.parse()

        for i in range(len(fenboard)):
            for j in range(len(fenboard[i])):
                if fenboard[i][j] in ['b', 'B']:
                    if fenboard[i][j] == 'b':
                        piece = self.createPiece(pieces.BLACK, pieces.BISHOP, self.boardRect[i][j])
                        self.pieceRect.append(piece)
                    elif fenboard[i][j] == 'B':
                        piece = self.createPiece(pieces.WHITE, pieces.BISHOP, self.boardRect[i][j])
                        self.pieceRect.append(piece)

                elif fenboard[i][j] in ['k', 'K']:
                    if fenboard[i][j] == 'k':
                        piece = self.createPiece(pieces.BLACK, pieces.KING, self.boardRect[i][j])
                        self.pieceRect.append(piece)
                    elif fenboard[i][j] == 'K':
                        piece = self.createPiece(pieces.WHITE, pieces.KING, self.boardRect[i][j])
                        self.pieceRect.append(piece)

                elif fenboard[i][j] in ['n', 'N']:
                    if fenboard[i][j] == 'n':
                        piece = self.createPiece(pieces.BLACK, pieces.KNGHT, self.boardRect[i][j])
                        self.pieceRect.append(piece)
                    elif fenboard[i][j] == 'N':
                        piece = self.createPiece(pieces.WHITE, pieces.KNGHT, self.boardRect[i][j])
                        self.pieceRect.append(piece)

                elif fenboard[i][j] in ['p', 'P']:
                    if fenboard[i][j] == 'p':
                        piece = self.createPiece(pieces.BLACK, pieces.PAWN, self.boardRect[i][j])
                        self.pieceRect.append(piece)
                    elif fenboard[i][j] == 'P':
                        piece = self.createPiece(pieces.WHITE, pieces.PAWN, self.boardRect[i][j])
                        self.pieceRect.append(piece)

                elif fenboard[i][j] in ['q', 'Q']:
                    if fenboard[i][j] == 'q':
                        piece = self.createPiece(pieces.BLACK, pieces.QUEEN, self.boardRect[i][j])
                        self.pieceRect.append(piece)
                    elif fenboard[i][j] == 'Q':
                        piece = self.createPiece(pieces.WHITE, pieces.QUEEN, self.boardRect[i][j])
                        self.pieceRect.append(piece)

                elif fenboard[i][j] in ['r', 'R']:
                    if fenboard[i][j] == 'r':
                        piece = self.createPiece(pieces.BLACK, pieces.ROOK, self.boardRect[i][j])
                        self.pieceRect.append(piece)
                    elif fenboard[i][j] == 'R':
                        piece = self.createPiece(pieces.WHITE, pieces.ROOK, self.boardRect[i][j])
                        self.pieceRect.append(piece)

        for piece in self.pieceRect:
            piece.displayPiece()
