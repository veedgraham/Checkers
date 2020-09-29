import pygame

from .constants import GREY, SQUARE_SIZE, CROWN


class Piece:
    PADDING = 15
    OUTLINE = 5

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        # 1 draws crown 0 no crown
        self.king = False

# ###################################################################################
        # commented out because we now have directions and logic in the game.py

        # telling the red pieces to go up aka negative numbers and
        # telling the white pieces to go down aka positive numbers
        # since 0,0 is in the top left corner of the window
        # if self.color == RED:
            # self.direction = -1
        # else:
            # self.direction = 1
# ####################################################################################
        self.x = 0
        self.y = 0
        # calculating the position (x,y) coordinates to draw checker in the square
        self.calc_pos()

    def calc_pos(self):
        # centering the center of the circle checker it gets drawn from the center out
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw(self, win):
        # drawing checker piece, last variable is the padding between square and circle piece
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            # blits an image, doesn't draw on window, to center the crown on the piece need to draw
            # the image with x,y as the top left corner of it
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)
