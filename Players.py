"""
Player class and Minimax class for CS331 - Programming Assignment 2

Original C++ game code - authored by wong (April 2015)
Python adaptation - authored by Erich Kramer (April 2017)
Updated by Casey Nord (April 2020)
"""


class HumanPlayer:
    """Defines human player."""
    def __init__(self, symbol):
        """
        Initializes player object with game piece.

        :param: symbol (char) Player game piece.
        """
        self.symbol = symbol

    def get_symbol(self):
        """Returns player symbol.
        
        :return: (char) Symbol.
        """
        return self.symbol

    @staticmethod
    def get_move():
        """Get human player move.
        Note that this takes col/row input as opposed to the code being written as row/col.
        This feels more natural for the player to input coordinates as x, y
        but for those with experience in linear algebra it feels more natural to program in rows/cols.

        :return: (int)(tuple) Coordinate pair.
        """
        while True:
            try:
                x = int(input("Enter col: "))
                assert (x >= 0), "Value must be positive"
                break
            except:
                print("Value must be a positive integer.")

        while True:
            try:
                y = int(input("Enter row: "))
                assert (x >= 0), "Value must be positive"
                break
            except:
                print("Value must be a positive integer.")
        return y, x


class MinimaxPlayer:
    """Defines minimax computer player.

    This class should manage code for controlling the ai player.
    """
    def __init__(self, symbol):
        """Initialize ai minimax player.

        :param: symbol (char) Player game piece.
        """
        self.symbol = symbol
