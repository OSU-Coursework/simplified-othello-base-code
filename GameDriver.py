#!/usr/bin/env python3

"""
GameDriver class for CS331 - Programming Assignment 2

This file functions as the 'main' program for running the game

Original C++ game code - authored by wong (April 2015)
Python adaptation - authored by Erich Kramer (April 2017)
Updated by Casey Nord (April 2020)
"""
import sys

from Players import *
from Othello import *


class GameDriver:
    """Manages Othello game execution."""
    def __init__(self, player_one_type, player_two_type, num_rows, num_cols):
        """
        :param: player_one_type (string) Defines whether player one is human or ai/minmax.
        :param: player_two_type (string) Defines whether player one is human or ai/minmax.
        :param: num_rows (int) number of rows on game board.
        :param: num_cols (int) number of columns on game board.
        """
        if player_one_type.lower() in "human":
            self.player_one = HumanPlayer('X')
        elif player_one_type.lower() in "minimax" or player_one_type.lower() in "ai":
            self.player_one = MinimaxPlayer('X')
        else:
            print("ERROR: Invalid type for Player 1!")
            exit(-1)
       
        if player_two_type.lower() in "human":
            self.player_two = HumanPlayer('O')
        elif player_two_type.lower() in "minimax" or player_two_type.lower() in "ai":
            self.player_two = MinimaxPlayer('O')
        else:
            print("ERROR: Invalid type for Player 2!")
            exit(-1)

        self.board = Othello(num_rows, num_cols, self.player_one.symbol, self.player_two.symbol)
        self.board.initialize()

    def process_move(self, current_player, opponent):
        """Executes game move.
        Will loop indefinitely until a valid move is entered.

        :param: current_player (object) Players object for current player.
        :param: opponent (object) Players object for opponent player.
        """
        invalid_move = True
        while invalid_move:
            (row, col) = current_player.get_move()
            if self.board.is_legal_move(row, col, current_player.symbol):
                invalid_move = False
                print("Move:", [col, row], "\n")
                self.board.play_move(row, col, current_player.symbol)
            else:
                print("ERROR: Invalid move!")

    def run_game(self):
        """Executes game loop."""
        current_player = self.player_one  # player 1 will always go first
        opponent = self.player_two
        self.board.draw_board()

        has_moves_available = False
        toggle_player = 0

        print("Player 1(", self.player_one.symbol, ") move: ")
        while True:
            if self.board.legal_moves_remain(current_player.symbol):
                has_moves_available = True
                self.process_move(current_player, opponent)
                self.board.draw_board()
            else:
                print("No moves available...")
                if not has_moves_available:
                    break
                else:
                    has_moves_available = False

            toggle_player = (toggle_player + 1) % 2
            if toggle_player == 0:
                current_player, opponent = self.player_one, self.player_two
                print("Player 1(", self.player_one.symbol, ") move: ")
            else:
                current_player, opponent = self.player_two, self.player_one
                print("Player 2(", self.player_two.symbol, ") move: ")

        # determine game outcome
        state = self.board.calculate_score(self.player_one.symbol) - \
            self.board.calculate_score(self.player_two.symbol)
        if state == 0:
            print("Tie game!")
        elif state > 0:
            print("Player 1 wins!")
        else:
            print("Player 2 wins!")


# main program
if __name__ == "__main__":
    # check for the correct number of command line args
    if len(sys.argv) != 3:
        print(f"USAGE: {sys.argv[0]} <player_one_type> <player_two_type>")
        exit(1)

    game = GameDriver(sys.argv[1], sys.argv[2], 4, 4)
    game.run_game()    
