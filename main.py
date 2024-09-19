"""
main.py

This script initializes and runs a game, loads a leaderboard from a JSON file, and displays the top players.

Author: Haydens Little Helpers
Date: 01/12/2023

Description:
    - The script imports the necessary modules (Game and Leaderboard) for running a game and managing leaderboards.
    - It initializes an instance of the Game class, runs the game, and then creates an empty Leaderboard instance.
    - The script loads a leaderboard from the "user_data.json" file and saves it to the Leaderboard instance.
    - It retrieves the top players from the leaderboard and prints their names and scores.

Usage:
    - Ensure the 'game.py' and 'leaderboard.py' files are in the same directory.
    - Run this script to play the game, load the leaderboard, and display top players.
"""

from game import Game
from leaderboard import Leaderboard

if __name__ == "__main__":

    game = Game()
    game.run()
    game_leaderboard = Leaderboard()  # creates a new empty instance of
    # leaderboard class
    game_leaderboard = game_leaderboard.load_leaderboard("user_data.json")
    # saves the file to the leaderboard instance

    top_players = game_leaderboard.get_top_players()  # gets top players from
    # leaderboard, saved as dictionary
    for player, score in top_players:

        print(f"{player}: {score}")
