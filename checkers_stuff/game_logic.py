import pygame
from .constants import RED, WHITE
from checkers_stuff.board import Board

class Game:
    def __init__(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        # valid play will be a dictionary of ways a player can move their piece
        self.valid_moves = {}
        self.win = win

    def update(self):
        self.board.draw()
        pygame.display.update()






# responsible for handing the rules and logic of the game







