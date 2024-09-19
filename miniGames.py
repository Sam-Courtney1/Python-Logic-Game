# miniGames.py

"""
Haunted Games Library

Description:
This Python file contains three classes representing different haunted-themed games:
1. HauntedMansionGame: A guessing game set in a haunted mansion where the player tries to guess a secret word akin to wordle
2. RockPaperScissors: A classic Rock, Paper, Scissors game with a haunted twist.
3. Riddle: A game that presents the player with random riddles to solve.

Usage:
- Import this file into your Python program to use the HauntedMansionGame, RockPaperScissors, and Riddle classes.
- Each class provides methods for playing their respective games.

Author: Jamie, Sam Courtney, Finn and Hayden

Date: 01/12/2023

Note: Make sure to have the 'game_data.json' file available for the HauntedMansionGame and Riddle classes.
"""

import random
import json


class HauntedMansionGame:
    def __init__(self, max_attempts=6):
        """
        Initialize a HauntedMansionGame instance.

        Parameters:
        - secret_word (str): The secret word to be guessed.
        - max_attempts (int): The maximum number of attempts allowed for guessing the word. Default is 6.

        Returns:
        None
        """
        self.secret_word = self.get_random_word()
        self.max_attempts = max_attempts
        self.remaining_attempts = max_attempts
        self.guessed_letters = set()

    def display_word(self):
        """
        Display the current state of the secret word, revealing guessed letters and hiding others.

        Returns:
        str: The formatted secret word display.
        """
        return ' '.join(
            letter if letter in self.guessed_letters else '_' for letter in
            self.secret_word)

    def check_guess(self, guess):
        """
        Check the validity of the guess and update the game state accordingly.

        Parameters:
        - guess (str): The user's guess, either a single letter or a complete word.

        Returns:
        None
        """
        guess = guess.lower()
        if len(guess) == 1 and guess.isalpha():
            return self.check_letter(guess)
        elif len(guess) == len(self.secret_word) and guess.isalpha():
            return self.check_word(guess)
        else:
            print("Please enter a valid single letter or a complete word.")
            return None

    def check_letter(self, guess):
        """
        Check a single letter guess and update the game state.

        Parameters:
        - guess (str): The single letter guessed by the user.

        Returns:
        int or None: Returns 1 if the guessed letter is correct, None otherwise.
        """
        if guess in self.guessed_letters:
            print("You already guessed that letter.")
        else:
            self.guessed_letters.add(guess)
            self.remaining_attempts -= 1
            if guess not in self.secret_word:
                print(f"'{guess}' is not in the word.")
            else:
                print(f"'{guess}' is in the word.")
                if self.is_winner():
                    return 1  # User wins if they guessed the entire word
        return 0  # User did not win

    def check_word(self, guess):
        """
        Check a complete word guess and update the game state.

        Parameters:
        - guess (str): The complete word guessed by the user.

        Returns:
        None
        """
        if guess == self.secret_word:
            self.guessed_letters = set(self.secret_word)
            return 1  # User wins if they guessed the entire word
        else:
            correct_letters = set(letter for letter in guess if letter in self.secret_word)

            if correct_letters:
                self.guessed_letters.update(correct_letters)
                print(f"Correct letters: {', '.join(correct_letters)}")
            else:
                self.remaining_attempts -= 1
                print(f"Incorrect word guess. You have {self.remaining_attempts} guesses remaining. Choose carefully.")

            return 0  # User did not win

    def is_winner(self):
        """
        Check if the user has guessed the entire word correctly.

        Returns:
        bool: True if the user has guessed the entire word, False otherwise.
        """
        return set(self.secret_word) == self.guessed_letters

    def is_game_over(self):
        """
        Check if the game is over due to reaching the maximum attempts.

        Returns:
        bool: True if the game is over, False otherwise.
        """
        return self.remaining_attempts <= 0

    def get_random_word(self):
        """
        Get a random word from the 'Secret_words' list in 'game_data.json'.

        Returns:
        str: A random word.
        """
        try:
            with open('game_data.json', 'r') as file:
                game_data = json.load(file)

            secret_words = game_data.get("Secret_words", [])
            if secret_words:
                return random.choice(secret_words).lower()  # Convert to lowercase for case-insensitive comparison
            else:
                print("No secret words found in 'game_data.json'.")
                return ""
        except FileNotFoundError:
            print("'game_data.json' not found.")
            return ""

    def play_haunted_mansion_game(self):
        """
        Play the Haunted Mansion guessing game.

        Returns:
        int: 1 if the user wins, 0 if the game is lost.
        """
        print("Welcome to the Haunted Mansion!\nCan you guess the secret word?")
        print(f"You have {self.max_attempts} attempts.")
        print(self.display_word())

        while not self.is_game_over():
            guess = input("Enter your guess: ")
            result = self.check_guess(guess)
            print(self.display_word())

            if result == 1:
                print("Congratulations! You guessed the entire word.")
                return 1

        print(f"Game over! The secret word was '{self.secret_word}'.")
        return 0


class RockPaperScissors:
    def __init__(self):
        """
        Initialize a RockPaperScissors instance.

        Returns:
        None
        """
        self.choices = ["rock", "paper", "scissors"]
        self.attempts = 3

    def get_user_choice(self):
        """
        Get the user's choice for Rock, Paper, or Scissors.

        Returns:
        str: The user's choice.
        """
        while True:
            user_choice = input("What is your choice Rock, Paper, "
                                "or Scissors: ").lower()
            if user_choice in self.choices:
                return user_choice
            else:
                print("Pick only rock, paper, or scissors!!")

    def get_computer_choice(self):
        """
        Get the computer's random choice for Rock, Paper, or Scissors.

        Returns:
        str: The computer's choice.
        """
        return random.choice(self.choices)

    def determine_winner(self, user_choice, computer_choice):
        """
        Determine the winner of the Rock, Paper, Scissors game.

        Parameters:
        - user_choice (str): The user's choice.
        - computer_choice (str): The computer's choice.

        Returns:
        bool: True if the user wins, False otherwise.
        """
        if user_choice == computer_choice:
            print("Draw!!")
            return False
        elif (user_choice == "rock" and computer_choice == "scissors") or \
                (user_choice == "paper" and computer_choice == "rock") or \
                (user_choice == "scissors" and computer_choice == "paper"):
            print("You win!")
            return True
        else:
            self.attempts -= 1
            print(f"Another win for me. You have {self.attempts} chances left.")
            return False

    def play_game(self):
        """
        Play the Rock, Paper, Scissors game.

        Returns:
        None
        """
        print("This game is Rock, Paper, Scissors! You have 3 tries, or you are not allowed in!")
        while self.attempts > 0:
            user_choice = self.get_user_choice()
            computer_choice = self.get_computer_choice()
            print(f"You chose {user_choice}. I chose {computer_choice}.")
            result = self.determine_winner(user_choice, computer_choice)
            if result:
                return True
            if self.attempts > 0:
                print(f"You have {self.attempts} chances left.")
            else:
                print("You are out of attempts. Game over!")


class Riddle:
    def __init__(self):
        self.riddles_and_answers = self.load_riddles_and_answers()
        self.current_riddle = None  # Store the current riddle

    def load_riddles_and_answers(self):
        with open("game_data.json", "r") as file:
            data = json.load(file)
        return data

    def print_riddle(self):
        """
                Selects a riddle at random from a list
                and displays it to the user
        """
        self.current_riddle = random.choice(list(self.riddles_and_answers["Riddles"].keys()))
        print(self.current_riddle)

    @property
    def get_answer(self):
        return self.riddles_and_answers["Riddles"].get(self.current_riddle, "")


class MiniGameCounter:
    def __init__(self):
        self.counter = 1

    def display_counter(self):
        print(f"You have completed {self.counter} / 3 mini-games")
        self.counter += 1
