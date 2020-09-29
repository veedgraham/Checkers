# Drawing the board for Checkers
import pygame

from checkers_stuff.constants import WIDTH, HEIGHT, SQUARE_SIZE
from checkers_stuff.game import Game

# from checkers_stuff.board import Board

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")


# this will tell us based on the position of our mouse what square
# row and col it is on


def get_row_col_from_mouse(pos):
    # we will get the x, y of our mouse and it will tell us what row and col we're in
    x, y = pos
    # if square size is 100 and we're trying to figure out what row we're in
    # if our y is at 650 then we know we must be in row six because 100
    # goes into 650 six times
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    # while run is true we will run this loop
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    # it's Game() because that is what the class is named

    # enable to check the board being drawn
    # board = Board()

    # checking if piece is deleted, and then redrawn at the specified square
    # comment out this piece to see that the function mouse button down works
    # piece = board.get_piece(0, 1)

    while run:
        clock.tick(FPS)

        if game.winner() != None:
            # checking if there's a winner and printing out something when there is a winner
            print(game.winner())

        for event in pygame.event.get():
            # if the red 'X' is pushed, quit the game
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                # commented out so game_logic will do this
                # piece = board.get_piece(row, col)
                # to show the piece gets moved, comment out for actually functionality
                # board.move(piece, 4, 3)
                # if game.turn == RED:
                game.select(row, col)

        game.update()

        # commented out enabled to test game mechanics
        # board.draw(WIN)
        # pygame.display.update()

    pygame.quit()


main()
