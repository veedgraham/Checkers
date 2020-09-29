import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from checkers_stuff.board import Board

# responsible for handing the rules and logic of the game

class Game:
    # you pass game a WIN argument in checker.py, so you must add the second attribute as win in the class
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    # underscore in front of def init makes it private
    # aka no one else can call it, must be called using the reset method
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        # valid play will be a dictionary of ways a player can move their piece
        self.valid_moves = {}

# init is technically initalizing the game, we don't want the user to have to call and init
# method when they want to reset the game
# making it private so the user doesn't see init they just see reset

    def reset(self):
        self._init()

    def winner(self):
        # wrote winner in the board.py, not in game.py but called it in checkers from game.py so this fixes that
        # could also just move the winner into game and delete the one in board...
        return self.board.winner()

    # when you select something you will call the select method, you will tell use the row and col that you selected
    # and then based on that whatever information we're currently storing in the state of the game will do something

    def select (self, row, col):
        # if we already selected something then let's try to move what we've selected to the row and col that you
        # put in self.move(row, col)
        if self.selected:
            result = self._move(row, col)
            # select will determine whether or not we should move something based on what you've already selected
            # if we are able to successfully move something,so if the row and col selected was valid, because I've
            # already something selected, say a diagonal square we could move to, then we will actually move it but
            # otherwise we will select a different piece, or at least try to select another piece, and try to move to
            # another square that is valid
            if not result:
                # if not result then reselect a space
                self.selected = None
                self.select(row, col)
# ####################################################################################################################
        # commented out
        # else:
            # Tell the user it was a valid move and return true or it's not a valid move and return false
# ####################################################################################################################
        piece = self.board.get_piece(row, col)
        # if piece doesn't = 0 (we;re not selecting an empty piece, we're selecting something that's red or white
        # and then whatever turn it currently is then we can actually select that piece
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            # then we can select that piece, and valid moves are equal to self.board.get_valid_moves and we'll give it
            # that piece
            self.valid_moves = self.board.get_valid_moves(piece)
            # return True to say what you selected is correct and a valid move so we will move
            return True
        # otherwise it's not a valid move and you can't move
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        # if we have actually selected something and the row col = 0 (aka does not have a piece already on it and
        # the row, col is a valid move then we will can move it
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            # we will move the currently selected piece to the specified row, col
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        # otherwise if this is not true return false
        else:
            return False
        # if you did move the piece return true
        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)


    def change_turn(self):
        # after the turn is complete the blue dots will go away since the dictionary is set to zero at the beginning
        self.valid_moves = {}
        # if it's reds turn change it to white's turn
        if self.turn == RED:
            self.turn = WHITE
        # if it's white's turn change it to red's turn
        else:
            self.turn = RED