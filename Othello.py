"""
Direction enumerations,
Board class, and Othello class for CS331 - Programming Assignment 2

Original C++ game code - authored by wong (April 2015)
Python adaptation - authored by Erich Kramer (April 2017)
Updated by Casey Nord (April 2020)
"""
from copy import deepcopy
from enum import Enum
from random import randint

BLANK_TILE = '.'  # this should only be a single character


class Direction(Enum):
    """Provides enumerations for cardinal directions."""
    N  = 1
    NE = 2
    E  = 3
    SE = 4
    S  = 5
    SW = 6
    W  = 7
    NW = 8


class Board:
    """Defines grid based game board.
    Board is initialized as m x n grid where rows is a list of length m
    and each entry in m is a list of length n representing columns.
    The board is initialized with the character in the global var BLANK_TILE.
    """
    def __init__(self, rows, cols):
        """
        :param rows: (int) Number of rows on game board.
        :param cols: (int) Number of columns on game board.
        """
        self.rows = rows
        self.cols = cols
        self.board = [[BLANK_TILE for y in range(rows)] for x in range(cols)]

    # getters/setters
    def get_row_count(self):
        """Returns number of rows.
        
        :return: (int) Number of rows.
        """
        return self.rows
    
    def get_col_count(self):
        """Returns number of columns
        
        :return: (int) Number of cols.
        """
        return self.cols

    def get_cell(self, row, col):
        """Attempts to return character at a given location.
        Reports error message if location is out of bounds.

        :return: (char) Symbol.
        """
        if self.in_bounds(row, col):
            return self.board[row][col]
        else:
            print("ERROR: attempting to get out of bounds cell! ")

    def set_cell(self, row, col, value):
        """Attempts to write character to a given location.
        Reports error message if location is out of bounds.
        """
        if self.in_bounds(row, col):
            self.board[row][col] = value
        else:
            print("ERROR: attempting to set out of bounds cell!")
    
    # state checks
    def in_bounds(self, row, col):
        """Checks if location is valid.

        :return: (bool) True if in bounds, False otherwise.
        """
        if (0 <= row < self.rows) and (0 <= col < self.cols):
            return True
        else:
            return False

    def cell_empty(self, row, col):
        """Checks if board location is empty.

        :return: (bool) True of cell is empty, false otherwise.
        """
        if self.board[row][col] == BLANK_TILE:
            return True
        else:
            return False

    # board operations
    def draw_board(self):
        """Draws game board to console window."""
        horz_edge = '--' * (self.cols + 1)
        vert_edge = '|'
        print(horz_edge + ' ')
        for r in range(self.rows):
            row = vert_edge + ' '
            for c in range(self.cols):
                row += self.board[r][c] + ' '
            row += vert_edge
            print(row)
        print(' ' + horz_edge)


class Othello(Board):
    """Defines game of Othello, inherits from Board"""
    def __init__(self, rows, cols, player1, player2):
        """
        :param rows: (int) Number of rows on game board.
        :param cols: (int) Number of columns on game board.
        :param player1: (char) Character for player one.
        :param player2: (char) Character for player two.
        """
        Board.__init__(self, rows, cols)
        self.player1 = player1
        self.player2 = player2

    def initialize(self):
        """Initializes game board (Othello rules).
        Note that the difference between Othello and Reversi is that Reversi
        starts with an empty board.  This freedom can result in a less
        interesting game depending on where pieces are played in the opening
        moves.
        """
        # randomly pick which pieces go where
        choice = randint(1, 2)

        # assume choice 1 by default
        game_piece_a = self.player1
        game_piece_b = self.player2
        if choice == 2:  # reassign game pieces
            game_piece_a = self.player2
            game_piece_b = self.player1

        # place top left piece
        self.set_cell((self.rows // 2) - 1, (self.rows // 2) - 1, game_piece_a)
        # place bottom right piece
        self.set_cell(self.rows // 2, self.rows // 2, game_piece_a)
        # place top right piece
        self.set_cell((self.rows // 2) - 1, self.rows // 2, game_piece_b)
        # place bottom left piece
        self.set_cell(self.rows // 2, (self.rows // 2) - 1, game_piece_b)

    def play_move(self, row, col, symbol):
        """Executes game move."""
        self.set_cell(row, col, symbol)
        self.flip_pieces(row, col, symbol)

    def calculate_score(self, symbol):
        """Iterates over symbols and calculates player score.

        :return: (int) Number of times passed symbol appears on board.
        """
        score = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == symbol:
                    score += 1
        return score

    def copy_game(self):
        """Clones game object.

        :return: A new game object in the same state as the original object.
        """
        game_copy = Othello(self.rows, self.cols, self.player1, self.player2)
        game_copy.board = deepcopy(self.board)
        return game_copy

    @staticmethod
    def set_direction(row, col, d):
        """Sets coordinates in a cardinal direction.
        Utilizes 'Direction' enumeration defined at the top of file.

        :param: row (int) index of game board.
        :param: col (int) index of game board.
        :param: dir (enum) direction to move in.
        :return: (int)(tuple) Coordinate pair.
        """
        if d.name == 'N':
            row += 1
        elif d.name == 'NE':
            col += 1
            row += 1
        elif d.name == 'E':
            col += 1
        elif d.name == 'SE':
            col += 1
            row -= 1
        elif d.name == 'S':
            row -= 1
        elif d.name == 'SW':
            col -= 1
            row -= 1
        elif d.name == 'W':
            col -= 1
        elif d.name == 'NW':
            col -= 1
            row += 1
        else:
            print("ERROR: set_direction() - Direction is invalid!")
        return row, col

    def is_legal_move(self, row, col, symbol):
        """Checks if a move is valid.

        :param: row (int) index of game board.
        :param: col (int) index of game board.
        :param: symbol (char) player game piece.
        :return: (bool) True if move is valid, false otherwise.
        """
        if self.in_bounds(row, col) and self.cell_empty(row, col):
            for d in Direction:
                (next_row, next_col) = self.set_direction(row, col, d)
                if self.check_endpoint(next_row, next_col, symbol, d, False):
                    return True
        else:
            return False

    def legal_moves_remain(self, symbol):
        """Iterates over game board and checks if there are legal moves available.

        :param: symbol (char) player game piece.
        :return: (bool) True if there are valid moves available, false otherwise.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cell_empty(row, col) and self.is_legal_move(row, col, symbol):
                    return True
        return False

    def flip_pieces(self, row, col, symbol):
        """Flips pieces surrounded by opposing pieces.
        Flips the piece(s) between two pieces once a piece is played at
        the specified row/col position.
        The symbol argument specifies who the current move belongs to.
        
        :param: row (int) index of game board.
        :param: col (int) index of game board.
        :param: symbol (char) player game piece.
        :return: (int) Number of pieces flipped.
        """
        flipped_piece_count = 0
        if not self.in_bounds(row, col):
            print("ERROR: flip_pieces() - Bad paramaters!")
            exit()  # we should exit if this occurs as it is game breaking
        else:
            for d in Direction:
                (next_row, next_col) = self.set_direction(row, col, d)
                if self.check_endpoint(next_row, next_col, symbol, d, False):
                    flipped_piece_count += self.flip_pieces_helper(next_row, next_col, symbol, d)
        return flipped_piece_count

    def flip_pieces_helper(self, row, col, symbol, d):
        """Sets flipped game piece on board
        Recursively checks through pieces and sets flipped piece if
        it is determined to be between opposing pieces.

        :param: row (int) index of game board.
        :param: col (int) index of game board.
        :param: symbol (char) player game piece.
        :param: dir (enum) direction to check in.
        :return: (int) Number of pieces flipped.
        """
        if self.get_cell(row, col) == symbol:  # this is one of our pieces
            return 0
        else:  # this is an opposing piece so flip it
            self.set_cell(row, col, symbol)
            (next_row, next_col) = self.set_direction(row, col, d)
            return self.flip_pieces_helper(next_row, next_col, symbol, d) + 1

    def check_endpoint(self, row, col, symbol, d, match_symbol):
        """
        Starting at (row, col) and moving in direction d, this function will check the endpoint
        of a trail of pieces. If match_symbol is true, it will return true if the endpoint matches
        the argument symbol (and false otherwise). If match_symbol is false, it will return true
        if the endpoint doesn't match the argument symbol (and false otherwise).
         
        :param: row (int) The row of the starting point.
        :param: col (int) The column of the starting point.
        :param: symbol (char) The symbol of the current player.       
        :param: dir (enum) The direction you are moving in.
        :param: match_symbol (bool) Defines if we are trying to find a matching or non-matching symbol        
        :return: (bool) If match_symbol True, returns true if the symbol parm matches the endpoint. 
                        If match_symbol False, return true if the arg symbol doesn't match the endpoint.
        """
        if not self.in_bounds(row, col) or self.cell_empty(row, col):  # this space is empty or out of bounds
            return False
        else:  # this space has a symbol
            if match_symbol:  # we are looking for a matching symbol
                if self.get_cell(row, col) == symbol:
                    return True
                else:
                    (next_row, next_col) = self.set_direction(row, col, d)
                    return self.check_endpoint(next_row, next_col, symbol, d, match_symbol)
            else:
                if self.get_cell(row, col) == symbol:
                    return False
                else:
                    (next_row, next_col) = self.set_direction(row, col, d)
                    return self.check_endpoint(next_row, next_col, symbol, d, (not match_symbol))
