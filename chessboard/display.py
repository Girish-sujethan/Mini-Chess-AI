"""
    Ahira Justice, ADEFOKUN
    justiceahira@gmail.com
"""


import os
import sys
import pygame
from pygame.locals import *

from . import board


os.environ['SDL_VIDEO_CENTERED'] = '1' # Centre display window.

FPS = 30
FPSCLOCK = pygame.time.Clock()

DISPLAYSURF = None

BASICFONT = None

gameboard = None

colors = {
    'Ash':  ( 50,  50,  50),
    'White':(255, 255, 255),
    'Black':(  0,   0,   0),
}

BGCOLOR = colors['Ash']

WINDOWWIDTH, WINDOWHEIGHT = 600, 600

BASICFONTSIZE = 30


def terminate():
    pygame.display.quit()
    # sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() #terminate if any QUIT events are present
        return
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
            return
        pygame.event.post(event) # put the other KEYUP event objects back

    return False


def start(fen='', size=8):
    global gameboard, font, DISPLAYSURF

    if not pygame.get_init():
        pygame.init()

    # Setting up the GUI window.
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Python Chess')
    font = pygame.font.Font(pygame.font.get_default_font(), 48)

    checkForQuit()

    DISPLAYSURF.fill(BGCOLOR)
    gameboard = board.Board(colors, BGCOLOR, DISPLAYSURF, size=size)
    gameboard.displayBoard()

    if (fen):
        gameboard.updatePieces(fen)
    else:
        gameboard.drawPieces()
    pygame.display.update()
    # FPSCLOCK.tick(FPS)

def update(fen, winner):
    global font, DISPLAYSURF

    checkForQuit()
    gameboard.displayBoard()
    gameboard.updatePieces(fen)

    if winner is not None:
        if winner == 'White':
            text_surface = font.render('White wins!', True, (50, 168, 82))
        elif winner == 'Draw':
            text_surface = font.render('Draw!', True, (255, 255, 255))
        elif winner == 'Black':
            text_surface = font.render('Black wins!', True, (168, 60, 50))

        DISPLAYSURF.blit(text_surface, dest=(25, 25))

    pygame.display.update()
    # FPSCLOCK.tick(FPS)
