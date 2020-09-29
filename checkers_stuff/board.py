import pygame
from .constants import BLACK, ROWS, COLS, RED, WHITE, SQUARE_SIZE
from .piece import Piece


class Board:
    def __init__(self):
        # internal representation of the board
        self.board = []
        # removing --> enable to test game and piece
        # self.selected_piece = None
        # keeping track of how many checkers are on the board standard is 12
        self.red_left = self.white_left = 12
        # keeping track of how many kings there are on the board, there are not kings starting out
        self.red_kings = self.white_kings = 0
        self.create_board()

    # giving it a window (win) to draw the red and black cubes in a checker board pattern
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                # mod 2 (row % 2), this will start off in row 0 to paint red cubes and 0 % 2 = 0 so it will
                # start drawing in column 0, then step by 2 and draw in column 2, then 4, then 6, etc.
                # then it will go up in ROWS to row 1 where it used to be row 0. RO % 2 = 1 % 2 = 1
                # so it will start drawing in column 1, then step by two to column 3, the 5, then 7 etc.
                # this will go all the way down the board
                pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # give me the piece and the row and col of the square it should move to
    def move(self, piece, row, col):
        # swaps the places of the pieces
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        # they have to move to become king, they won't become king if they start in that row
        # if we reach row 7 or row 0 you have made it to the opposite side of the board and must be kinged
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    # get the position of a piece so you can move it on the board
    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        # rows don't change but the columns do to fill board with pieces first
        # then once cols done it will increase row, etc.
        for row in range(ROWS):
            # creating an interior list to represent each row
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        # zero will be a blank piece to keep track of separators
                        self.board[row].append(0)
                else:
                    # zero will be a blank piece to keep track of separators on other row
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                # if the piece is zero we will NOT draw a piece there
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    # returns the winning color by keeping track of how many pieces are left for each color and when they reach 1 or
    # less than it declares the other color the winner (the one who still has pieces left on the board)
    def winner(self):
        if self.red_left <= 0:
            return "White"
        elif self.white_left <= 0:
            return "Red"

        return None

    def get_valid_moves(self, piece):
        # dictionary of valid moves
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        # if the piece is red or a king do something
        if piece.color == RED or piece.king:
            # if we are red we're moving up the y axis and we need to see if that is a valid move, aka still on the board
            # start= row -1, start at the row above the current row that we're at
            # stop= how far up are we going to look? Look at the maximum of (row -3, -1)
            # -1 says stop at -1 aka look up to row 0
            # -3  means don't wanna look further than two pieces away from where I currently am,
            #  if I start at row -1 and i move to maximum row -3 then that means I'm only looking two above the current
            #  row which I am at, at most
            # step = -1 is saying move up when we decrement this for loop
            # the color it is
            # left =is where we're gonna start for our col and what we're gonna subtract as we move upwards
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            # it's all the same except we move to the right so
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
            # essentially traverse left and traverse right are going to fill the dictionary with a list of valid moves

        # if a piece is white or a king do something
        if piece.color == WHITE or piece.king:
            # start is gonna be +1 because we're moving down the y axis
            # it's the min of rows+3, and ROWS (so you stop at the top row and don't move more than two pieces away)
            # ROWS = stop at the top row, look up to the top row
            # +3 means don't wanna look further than two pieces away from where I currently am
            # step = 1 is saying move down  when we increment this for loop
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
        return moves

    # what square do we start at, what square do we stop at, how many steps are taken to get there, what is the color,
    # start stop step are for the for loops
    # step tells us if we go up or down the board on the y axis, top left diagonal or bottom left diagonal
    # skipped have we skipped any pieces yet and if we have we can only move to squares when we skip another piece
    # traverse right is telling us where are we starting in terms of the col when we're traversing to the left/right
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        # what row am i starting at, what row am i stopping at, what am i stepping by
        for r in range(start, stop, step):
            # if we are at the end of the board and the left is no longer in the range of col we have then we break
            if left < 0:
                break

            # row and then the variable keeping track of what col we're on
            current = self.board[r][left]
            # if current is = 0 and we skipped a piece and we have NOT seen a piece yet (aka last is undefined (because
            # there hasn't been a move before your first move) then break'
            # last is the piece that we would skip to move to where we're gonna go
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                # if current is = to 0 that means we found the an empty square (does not have a piece on it) [ABOVE]
                # OTHERWISE [BELOW] if it's not = 0 (and there's a piece on that square) so the piece has a color attribute
                # and if it's color is = to our color then we can't move there cause we're blocked by our own piece
                if last:
                    # what direction are we going, up or down?
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                        # see if we can double jump or triple jump
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                # then we break because there are no other available moves to be made since this one is blocked
                break
            # if the color is not = to our own color THEN it means it was the other color and we could potentially
            # move over top of it (jump it/capture it), assuming that there is an empty square next
            # BELOW we're seeing if we can jump, last is equal to current and we loop again to look at the next row and
            # [running through the loop from the top]
            # we move left and we look at the other diagonal piece
            # if current now, if this next piece is zero, and if we skipped and not last(no break from method/function)
            # if skip only, and it's zero and none of the above is true, then we add this as a possible move
            # if it's zero and last existed then we can jump over it move r , last
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        # what row am i starting at, what row am i stopping at, what am i stepping by
        for r in range(start, stop, step):
            # if we are at the end of the board and the left is no longer in the range of col we have then we break
            if right >= COLS:
                break

            # row and then the variable keeping track of what col we're on
            current = self.board[r][right]
            # if current is = 0 and we skipped a piece and we have NOT seen a piece yet (aka last is undefined (because
            # there hasn't been a move before your first move) then break'
            # last is the piece that we would skip to move to where we're gonna go
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                # if current is = to 0 that means we found the an empty square (does not have a piece on it) [ABOVE]
                # OTHERWISE [BELOW] if it's not = 0 (and there's a piece on that square) so the piece has a color attribute
                # and if it's color is = to our color then we can't move there cause we're blocked by our own piece
                if last:
                    # what direction are we going, up or down?
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                        # see if we can double jump or triple jump
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                # then we break because there are no other available moves to be made since this one is blocked
                break
            # if the color is not = to our own color THEN it means it was the other color and we could potentially
            # move over top of it (jump it/capture it), assuming that there is an empty square next
            # BELOW we're seeing if we can jump, last is equal to current and we loop again to look at the next row and
            # [running through the loop from the top]
            # we move left and we look at the other diagonal piece
            # if current now, if this next piece is zero, and if we skipped and not last(no break from method/function)
            # if skip only, and it's zero and none of the above is true, then we add this as a possible move
            # if it's zero and last existed then we can jump over it move r , last
            else:
                last = [current]

            right += 1

        return moves
