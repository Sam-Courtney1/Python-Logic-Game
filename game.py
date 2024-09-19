# game.py

"""
Game Module

Description:
This Python module defines the main game class, 'Game', which manages the behavior and flow of the mystery game.
It includes interactions with characters, exploring locations, playing mini-games, and keeping track of the player's progress.

Classes:
1. Game: Represents the main game class, managing the player's journey, interactions, inventory, and overall progress.

Usage:
- Import this module into your Python program to use the 'Game' class.

Author: Sam Curran, Sam Courtney, Hayden Carroll, Jamie O'Neill, Finn Delaney
Date: 15/11/2023 - 01/12/2023
"""

import time
import json
from colorama import \
    Fore  # Easily installed via Pycharm (requirement for project submission)
from loggable import Loggable
from character import Suspect, NPC, Witness
from leaderboard import Leaderboard
from miniGames import HauntedMansionGame, RockPaperScissors, Riddle, MiniGameCounter
from inventory import Inventory
from item import Item
from location import CrimeScene, Kitchen, Attic, Library, Location
from user_registration import register_user, login_user


# Define the main game class
class Game:
    """The Game class is set up to manage the game's behavior."""

    def __init__(self):
        self.username = None
        self.player_name = None
        self.game_leaderboard = Leaderboard()
        self.game_log = Loggable()
        self.game_riddle = Riddle()
        self.__error_logger = Loggable()
        self.haunted_game = HauntedMansionGame()
        self.inventory = Inventory()  # Initialize the player's inventory
        self.library = Library()
        self.attic = Attic()
        self.kitchen = Kitchen()
        self.secret_passages = Location(3)
        self.rock_paper_scissors = RockPaperScissors()
        self.running = True
        self.started = False
        self.characters_interacted = False
        self.npcs_interacted = False
        self.kitchen_npc_interacted = False
        self.attic_npc_interacted = False
        self.library_npc_interacted = False
        self.score = 0
        self.mini_game = MiniGameCounter()
        self.crime_scene = CrimeScene("Mansion's Drawing Room")
        self.witness = Witness(
            "Mr. Drew the Gardener",
            "I am not so sure this is as simple a case, people have been "
            "very suspicious recently, the chef and the butler are acting "
            "strange, I suggest you talk to them, if you haven't already",
            "Chef and butler acting strange",
            "Leaves the room to go back to gardening",
            48,
        )
        self.witness2 = Witness(
            "Ms. Parker",
            "I saw someone near the window at the time of the incident, "
            "just after my walk with Lady Victoria",
            "Suspicious figure in dark clothing.",
            "calmly walks away",
            45,
        )
        self.suspect = Suspect(
            "Mr. Reginald, the butler",
            "I was working last night but left at 8",
            "Claims to have left at 8",
            "walks away in a rush",
            61,
        )
        self.suspect2 = Suspect(
            "Lady Victoria Starling",
            "I cant believe my Diamond necklace was"
            " Stolen!\nI heard someone in my room last night, it was worth "
            "so much aswell!!",
            "Was on a walk with Mr. Parker",
            "walks away",
            78,
        )
        self.suspect3 = Suspect(
            "The Chef",
            "Get out my kitchen, I dont need to talk to you",
            "Left at 9 with the butler (You notice the times dont match up)",
            "Acting Suspicious",
            78,
        )

        self.npcs = [
            NPC(
                "Beatrice",
                "How do you do.",
                "decides to hang around and see what will happen",
                68,
            ),
            NPC("Seamus", "Welcome to the mansion", "decides to walk away",
                29),
            NPC("The Child", "Go away this is my house!",
                "angrily storms away", 8),
        ]

        self.doors_checker = [False] * 3
        self.doors = ["Hidden Passage(1)", "Hidden Passage(2)", "Hidden "
                                                                "Passage(3)"]
        self.game_scores = {
            "Haunted Mansion": 0,
            "Rock Paper Scissors": 0,
            "Riddle": 0,
            # Add more games as needed
        }

    def __score__(self):
        # this gives you 10 points for interacting with a witness
        if self.witness.interacted:
            self.score += 10

        # this gives you 10 points for interacting with a witness
        if self.witness2.interacted:
            self.score += 10

        # this gives you 15 points for interacting with a suspect
        if self.suspect.interacted:
            self.score += 15

        # this gives you 2 points for interacting with NPCs
        if self.npcs_interacted:
            self.score += 2

        if self.attic_npc_interacted:
            self.score += 2

        if self.library_npc_interacted:
            self.score += 2

        if self.kitchen_npc_interacted:
            self.score += 2

        # this gives you a point for every clue you find
        if self.crime_scene.review_clue():
            self.score += len(self.crime_scene.review_clue())

        if self.attic.review_clue():
            self.score += len(self.attic.review_clue())

        if self.library.review_clue():
            self.score += len(self.library.review_clue())

        if self.kitchen.review_clue():
            self.score += len(self.kitchen.review_clue())

        return self.score

    @property
    def log(self):
        # to do: think of some appropriate access checks here. For example,
        # only admins are allowed to read out logs.
        return self.game_log

    @property
    def error_log(self):
        return self.__error_logger

    def get_past_progress(self):
        with open('user_data.json', 'r') as file:
            game_data = json.load(file)
        self.player_name = game_data[self.username]["name"]
        self.score = game_data[self.username]["score"]
        try:
            self.crime_scene.import_past_progress(game_data[self.username][
                                                      "Location_clues"][
                                                      "CrimeScene"])
            self.attic.import_past_progress(game_data[self.username][
                                                "Location_clues"][
                                                "Attic"])
            self.kitchen.import_past_progress(game_data[self.username][
                                                  "Location_clues"][
                                                  "Kitchen"])
            self.library.import_past_progress(game_data[self.username][
                                                  "Location_clues"][
                                                  "Library"])
            self.secret_passages.import_past_progress(game_data[
                                                          self.username][
                                                          "Location_clues"][
                                                          "Secret Passages"])
        except KeyError:
            print("You found no clues last time, or didn't exit properly!")

    def initialize_player(self):
        max_login_attempts = 3

        while max_login_attempts > 0:
            user_choice = input("Do you want to register(R) or login(L): ")

            if user_choice.lower() not in ["r", "l"]:
                print("Please enter a valid option (R/L).")
                continue

            self.username = input("Enter your username: ")
            password = input("Enter your password: ")

            if user_choice.lower() == "r":
                if register_user(self.username, password):
                    print("Successfully Registered, enjoy the game")
                    break
                else:
                    print(
                        "Registration failed. Please choose a different username.")
            elif user_choice.lower() == "l":
                if login_user(self.username, password):
                    print("Login successful!")
                    self.get_past_progress()

                    break
                else:
                    print("Login failed")

    def update_user_score(self, username, score):
        try:
            with open('user_data.json', 'r') as file:
                user_data = json.load(file)
        except FileNotFoundError:
            user_data = {}

        user_data[username]["score"] = score

        with open('user_data.json', 'w') as file:
            json.dump(user_data, file, indent=2)

    def completed_mini_game_message(self):
        self.crime_scene.add_clue("The letter on the ground")
        self.inventory.add_item(Item("Letter", "Letter found in the butlers "
                                               "pantry", "You read the "
                                                         "letter to find the "
                                                         "butler has been "
                                                         "talking to a "
                                                         "jeweller about "
                                                         "selling "
                                                         "jewellery", 15))
        print("You have discovered a secret letter")

    def run(self):
        text = "\033[1;31mWelcome to 'The Poirot Mystery'\n" \
               "You are about to embark on a thrilling " \
               "adventure as a detective\n" \
               "Your expertise is needed to solve a complex case " \
               "and unveil the truth\n\033[0m"

        for char in text:
            print(char, end="", flush=True)
            time.sleep(0.005)  # Adjust the delay time as needed

        self.initialize_player()

        while self.running:
            try:
                self.update()
            except ValueError as ve:
                self.__error_logger.log(f"Error found:\n {ve}.")
            except Exception as e:
                self.__error_logger.log("Unexpected error from run():\n{e}.")
                print(
                    "Unexpected caught error during running of the Game. "
                    f"\n{e}\n"
                    "We continue playing..."
                )
            else:
                self.game_log.log("Successfully updating")
            finally:
                self.game_log.log("---")
        self.end_game()

    def update(self):
        """The update method waits for player input and responds to their
         choice to start the game or quit."""

        if self.started:
            player_input = input(Fore.GREEN +
                                 "Press one of the following keys: \n'q' to quit\n"
                                 "'r' to review your clues\n"
                                 "'e' to explore the mansion further\n"
                                 "'s' to see your current score \n"
                                 "'u' to use an item from your inventory: \n"
                                 "'c' to conclude investigation\n"
                                 "Please Enter your selection: "
                                 )

            self.game_log.log(f"Player input is {player_input}.")

            if player_input.lower() == "q":
                print("exiting...")
                self.running = False
                self.game_log.log("Player quit the game")
            elif player_input.lower() == "r":
                self.game_log.log("Player chose to review clues "
                                  "at Crime Scene")
                if self.crime_scene:
                    clues = self.crime_scene.review_clue() + self.attic.review_clue() + self.library.review_clue() + self.kitchen.review_clue()
                    if clues:
                        print("You review your clues:")
                        for clue in clues:
                            print(clue)
                    else:
                        print("No clues have been gathered yet.")
                        self.game_log.log("Player had no clues to review")
            elif player_input.lower() == "e":
                self.explore_options()
            elif player_input.lower() == "s":
                self.game_log.log("Player chose to see their score")
                print(f"Your current score is {self.__score__()}")
            elif player_input.lower() == "u":
                # Print all items in the inventory
                self.inventory.print_inventory()
                item_name = input(
                    "Enter the name of the item you want to use: ")
                self.inventory.use_item(item_name, Game)
            elif player_input.lower() == "c":
                self.user_guess()
            else:
                raise ValueError("Incorrect user entry.")

        else:
            player_input = input("Press 'q' to quit or 's' to start: ")
            if player_input.lower() == "q":
                self.game_log.log("Player chose to quit the game")
                print("exiting...")
                self.running = False
            elif player_input.lower() == "s":
                self.game_log.log("Player chose to start the game")
                self.started = True
                self.start_game()
            else:
                raise ValueError("Incorrect user entry.")


    def start_game(self):
        """The start_game method introduces the player
        to the mystery case and sets the scene."""
        if not self.player_name:
            self.player_name = input("Please enter your detective name:")

            text = ("\033[1;31mAs the renowned detective, "
                    f"{self.player_name},\n"
                    "you were called in to solve the baffling case of the "
                    "missing Diamond Necklace Starlight Serenade\n\n"
                    "You have been tasked with finding the missing piece "
                    "of the mansion's owner, Lady Victoria Starling!\n"
                    "You can find her in the mansions drawing room...\n\033[0m")

            for char in text:
                print(char, end="", flush=True)
                time.sleep(0.005)  # Adjust the delay time as needed

            print(f"Welcome {self.player_name}")
        else:
            print(f"Welcome back {self.player_name}")

    def explore_options(self):

        explore_choice = input(Fore.GREEN + "Which path do you dare to take,"
                                            "The path that leads upstairs(1) or"
                                            " The path that leads downstairs("
                                            "2) : ")
        if explore_choice == '1':
            self.explore_upstairs()
        elif explore_choice == '2':
            self.door_choice()
        else:
            raise ValueError(f"Invalid door choice: {explore_choice}")

    def explore_upstairs(self):
        while True:
            room_choice = input(Fore.GREEN + "As you venture forward 4 rooms "
                                             "are revealed "
                                             "to you:\nA Kitchen(K)"
                                             "\nA huge Library(L)"
                                             "\nA dusty Attic(A)"
                                             f"\nThe {self.crime_scene.name}(D)"
                                             f"\n--To go back(B)--\n"
                                             "Which do you want to choose")

            if room_choice.lower() == 'k' and not self.kitchen.visited:
                self.kitchen.visited = True
                print('you walk through the seemingly never ending upstairs '
                      'hallway of the mansion on your way to the kitchen '
                      'you open the door and see an old man cutting carrots')
                interact_choice = input("Do you want to talk to the chef "
                                        "(Y/N) : ")
                while True:
                    if interact_choice.lower() == 'y':
                        print(self.suspect3.interact())
                        self.kitchen.add_clue("chef is hostile and doesnt seem to "
                                              "want to help you solve the crime")
                        break
                    elif interact_choice.lower() == 'n':
                        print('Scared off interaction...How embarrassing, '
                              'you might\'ve missed an important clue...')
                        break
                    else:
                        print("Please choose a valid option (Y/N):")

                explore_choice1 = input(
                    "do you want to explore kitchen further"
                    " ? (Y/N) :")
                while True:
                    if explore_choice1.lower() == 'y':
                        print(
                            "you walk around the kitchen searching for clues...\n"
                            "you see signs of a forced entry on the knife press\n"
                            "and you also heard the chef complain about missing\n"
                            "utensils earlier")
                        self.kitchen.add_clue("looks like someone stole a knife "
                                              "from the kitchen")
                        break
                    elif explore_choice1.lower() == 'n':
                        print("You return to the hallway")
                        break
                    else:
                        print("Please choose a valid option (Y/N):")

                explore_choice1 = input(
                    "do you want to explore kitchen further"
                    "? (Y/N) :")
                if explore_choice1.lower() == 'y':
                    print(
                        "\nAs you are leaving you see a camera in the corner "
                        "off\n"
                        "the kitchen that looks to be off. The Chef says \n"
                        "'it wasn't on when i arrived this morning'.\nThis "
                        "person"
                        "must know a lot about this mansion, you think to "
                        "yourself \n As you walk out of the kitchen you get "
                        "a strong distinct smell of a cigar...interesting")
                    self.kitchen.add_clue("camera system has been shut off")

            elif room_choice.lower() == 'k' and self.kitchen.visited:
                print("You have already explored this room\n"
                      "Select a door to explore")

            elif room_choice.lower() == "a" and not self.attic.visited:
                self.attic.visited = True
                print(
                    "You walk through the never ending halls of the mansion on"
                    "your way to the attic. You reach a dimly lit room, As you"
                    " walk in there\'s a young girl writing at a desk")
                interact_choice = input(
                    f"do you want to talk to the girl? (y/n) : ")
                if interact_choice.lower() == 'y':
                    print(self.attic.interact_with_npcs)
                    self.attic_npc_interacted = True
                    print(self.attic.npc_action)
                else:
                    print("You back out of the room")

                explore_choice2 = input("do you want to explore attic further"
                                        " ? (Y/N) :")
                if explore_choice2.lower() == 'y':
                    print("\n as you walk around the attic you feel a cold "
                          "breeze coming from\nthe window at the back of the "
                          "room.\nYou see it has been opened and see a muddy "
                          "footprint on the windowsill.\n\nAs you examine it "
                          "closer it looks to be forces open")
                    self.attic.add_clue("window open in attic")
                    self.attic.add_clue("muddy footprint on attic windowsill")
                    self.attic.add_clue("window appears to be forced open")
                else:
                    print(
                        'Scared of a bit of investigating...How embarrassing,'
                        'you might\'ve missed an important clue...')
            elif room_choice.lower() == "a" and self.attic.visited:
                print("You have already explored the attic"
                      "\nChoose another door to explore more")

            elif room_choice.lower() == "l" and not self.library.visited:
                self.library.visited = True
                print(
                    "you walk through the never ending halls of the mansion on "
                    "your way to the library.")
                interact_choice = input(
                    "do you want to talk to the librarian? (y/n) : ")
                if interact_choice.lower() == 'y':
                    print(self.library.interact_with_npcs)
                    self.library_npc_interacted = True
                    print(self.library.npc_action)
                    self.library.add_clue("someone was walking in the attic"
                                          " late last night")
                else:
                    print("You walk back out of the room")

                explore_choice3 = input(
                    "do you want to explore library further"
                    " ? (Y/N) :")
                if explore_choice3.lower() == 'y':
                    print("\nas you walk through the isles of bookshelves you "
                          "see a trail of footprints\nleading from what seems "
                          "to be a hidden passage.")
                    self.library.add_clue(
                        "hidden passage that leads to library")
                    self.library.add_clue("muddy footprints in library")

            elif room_choice.lower() == "l" and self.library.visited:
                print("You have already explored the library"
                      "Continue to explore, you never know what you might find")

            elif room_choice.lower() == "b":
                break
            elif room_choice.lower() == 'd':
                text = ("\033[1;31mIt appears you found the Crime Scene,\n"
                        "what you find here is of the upmost\n"
                        "importance so be very careful\n\033[0m")

                for char in text:
                    print(char, end="", flush=True)
                    time.sleep(0.005)  # Adjust the delay time as needed

                text = (
                    "\033[1;31mAs you make your way through the winding "
                    "stairs that"
                    "lead\n"
                    " to the crime scene you feel all eyes are on you, "
                    "you must\n"
                    "solve this crime. You reach the top of the stairs and "
                    "go\n"
                    "to the bedroom were the precious jewels were stored. "
                    "You\n"
                    "slowly push the door open.\n\033[0m")
                for char in text:
                    print(char, end="", flush=True)
                    time.sleep(0.005)

                while True:
                    player_input = input(Fore.RED +
                                         "Press one of the following keys: "
                                         "\n'b' to go back to"
                                         "the hallway\n"
                                         "'i' to interact with characters at "
                                         "the crime scene\n"
                                         "'r' to review your clues\n"
                                         "Please Enter your selection: "
                                         )

                    self.game_log.log(f"Player input is {player_input}.")

                    if player_input.lower() == "b":
                        print("Leaving...")
                        time.sleep(1)
                        break
                    elif player_input.lower() == "i":
                        character_choice = input(
                            "If you want to speak to the witness and a suspect,"
                            "choose 1. "
                            "If you'd like to speak to other people in the"
                            " room, choose 2:"
                        )
                        self.game_log.log(
                            "Player chose to interact with characters")
                        if character_choice == "1":
                            self.game_log.log(
                                "Player chose to interact with witness and "
                                "suspects"
                            )
                            self.interact_with_characters()
                        elif character_choice == "2":
                            self.game_log.log(
                                "Player chose to interact with NPCs")
                            self.interact_with_npcs()
                    elif player_input.lower() == "r":
                        self.game_log.log("Player chose to review clues "
                                          "at Crime Scene")
                        if self.crime_scene:
                            clues = self.crime_scene.review_clue()
                            if clues:
                                print("You review your clues:")
                                for clue in clues:
                                    print(clue)
                            else:
                                print("No clues have been gathered yet.")
                                self.game_log.log(
                                    "Player had no clues to review")

                        print(f"Your current score is {self.__score__()}")

    def door_choice(self):
        """This method handles the door examination option. User input is
        being handled. The user can make 3 choices: door 1 leads to the
        front door, door 2 leads to the library and door 3 leads to the
        kitchen. Wrong user input is being handled via print-outs for error
        handling."""

        while True:
            print("You venture forward within this decrepted mansion,Three dark "
                  "passages appear before you:")
            for i, door in enumerate(self.doors, start=1):
                print(f"{i}. {door}")
            print("\n--To go back(B)--")
            player_input = int(
                input("Which passage will you venture through...Brave"
                      f" detective:")
            )

            if 0 < player_input < len(self.doors) + 1:  # for valid entry check
                self.game_log.log(f"Player chose to enter door {player_input}")
                if int(player_input) == 1 and not self.doors_checker[0]:
                    print("Those who dare to enter ahead..guess this word...or "
                          f"ill take your head")
                    # Play mini-game only for the first door choice
                    word_result = self.haunted_game.play_haunted_mansion_game()
                    if word_result:
                        self.doors_checker[0] = True
                        print(
                            "inside is a small kitchen with a butler making food\n"
                            "you ask him who he is  and he tells you hes the "
                            "the mansion's butler, Mr. Reginald\n"
                            "you are surised he is the butler at first as his"
                            " trousers seem to be stained with mud and his shoes\n"
                            "look tarnished after talking, you realise he has a"
                            " suspiciously extensive knowledge of the mansion's "
                            "layout\n"
                        )
                        self.secret_passages.add_clue(
                            "Mr. Reginald's rugged look and extensive knowledge "
                            "of the mansion's layout"
                        )
                        self.secret_passages.add_clue(
                            "Mr. Reginald's rugged look and extensive knowledge "
                            "of the mansion's layout"
                        )
                        # Calls the method reward_for_game_completion adds to the users score.
                        self.mini_game.display_counter()

                elif int(player_input) == 2 and not self.doors_checker[1]:
                    print("Those who dare to enter ahead..Prove to me you are "
                          "worthy, Beat me in this game of wit..before you end "
                          "up dead")

                    rps_result = self.rock_paper_scissors.play_game()
                    if rps_result:
                        self.doors_checker[1] = True
                        print(
                            "You slowly open the door to reveal a...\n"
                            "...a dark corridor which leads you to stairs\n"
                        )
                        self.secret_passages.add_clue("The letter on the ground")
                        # Calls the method reward_for_game_completion adds to the users score.
                        self.mini_game.display_counter()

                elif int(player_input) == 3 and not self.doors_checker[2]:
                    print(
                        "Those who dare to proceed ahead...let me riddle you a question before you end up dead")
                    # Use the new methods from the updated Riddle class
                    self.game_riddle.print_riddle()
                    user_input = input("What is your guess Detective:")
                    # Access the answer using the get_answer property
                    if user_input.lower().strip() == self.game_riddle.get_answer.strip():
                        print("Very good Detective, you may proceed")
                        print(
                            "You open the library door to reveal a hidden\n"
                            "passage...\n"
                            "What secrets does it hold?"
                        )
                        self.secret_passages.add_clue(
                            "The hidden passage behind the library door")
                        self.doors_checker[2] = True
                        # Calls the method reward_for_game_completion adds to the users score.
                        self.mini_game.display_counter()

                    elif player_input == "B":
                        break

                else:
                    self.game_log.log(
                        f"Player chose to enter door {player_input} "
                        f"but they had already looked inside"
                    )
                    print(
                        f"You've already been to {self.doors[player_input - 1]} "
                        f"Detective."
                    )
            else:
                raise ValueError(f"Invalid door choice Detective: {player_input}")
        if self.mini_game.counter == 4:
            self.completed_mini_game_message()

    def interact_with_characters(self):
        if not self.characters_interacted:
            print("You decide to interact with the characters in the room.")

            clue_suspect = self.suspect.interact()
            self.crime_scene.add_clue(clue_suspect)
            print(clue_suspect)  # keep the outputs going
            self.game_log.log(f"{self.suspect.name} interacted with Player")
            self.game_log.log(
                f"{self.suspect.name} provided clue:" f" {clue_suspect}")

            time.sleep(2)
            # this adds the suspect alibi to a variable
            # adds it to the clue list,
            # then prints that and the suspect action
            suspect_alibi = self.suspect.provide_alibi()
            self.crime_scene.add_clue(suspect_alibi)
            print(suspect_alibi)
            print(self.suspect.perform_action())
            self.game_log.log(
                f"{self.suspect.name} " f"provided alibi: {clue_suspect}")

            time.sleep(2)

            clue_witness = self.witness.interact()
            self.crime_scene.add_clue(clue_witness)
            print(clue_witness)
            self.game_log.log(f"{self.witness.name} interacted with Player")
            self.game_log.log(
                f"{self.suspect.name} " f"provided clue: {clue_suspect}")

            # this adds the witness observation to a variable adds
            # it to the clue list, then prints that and the witness action
            # and changes interacted to true
            witness_observation = self.witness.share_observation()
            self.crime_scene.add_clue(witness_observation)
            print(witness_observation)
            print(self.witness.perform_action())
            self.game_log.log(
                f"{self.suspect.name} " f"provided observation: {clue_suspect}"
            )

            time.sleep(2)

            clue_witness = self.witness2.interact()
            self.crime_scene.add_clue(clue_witness)
            print(clue_witness)
            self.game_log.log(f"{self.witness2.name} interacted with Player")
            self.game_log.log(
                f"{self.suspect.name} " f"provided clue: {clue_suspect}")

            time.sleep(2)

            # this adds the witness2 observation
            # to a variable adds it to the clue list, then prints that and
            # the witness action and changes interacted to true
            witness_observation = self.witness2.share_observation()
            self.crime_scene.add_clue(witness_observation)
            print(witness_observation)
            print(self.witness2.perform_action())
            self.characters_interacted = True
            self.game_log.log(
                f"{self.suspect.name} provided observation:" f" {clue_suspect}"
            )

            # this compares the age of the 2 witnesses
        else:
            print(
                "You have already interacted with the characters. \nThey no"
                "longer wish to speak to you."
            )

    def interact_with_npcs(self):
        if not self.npcs_interacted:
            print("You decide to interact some others in the room.")
            for index, npc in enumerate(self.npcs):
                self.game_log.log(f"{npc.name} interacted with Player")
                interaction = npc.interact
                action = npc.perform_action()
                print(f"{interaction}\n{action}")
                self.game_log.log(
                    f"{npc.name} said to the player:" f" {npc.dialogue}")
            self.crime_scene.add_clue(
                "Three people hanging around the Crime Scene"
                "who have nothing to do with the crime"
            )
            self.npcs_interacted = True
            # Detail needed to be added here, Storyline etc

    def examine_clues(self):
        if not self.crime_scene.investigated:
            print(
                "You step into the dimly lit crime scene.\nBroken glass lies "
                "near the window, and a table is overturned.\n"
                "You find a torn piece of fabric near the window.\n"
                "There's a distinct smell of Cigars lingering in the air.\n"
                "The mystery deepens."
            )

            # Add items to the inventory when examining clues
            self.crime_scene.add_clue("Torn fabric")
            self.inventory.add_item(
                Item("Torn Fabric", "A torn piece of fabric near the "
                                    "window", "You notice this piece of "
                                             "fabric is part of the butlers "
                                             "suit", 2))
            self.crime_scene.add_clue("Broken glass near window")
            self.crime_scene.add_clue("An overturned table at crime scene")
            self.inventory.add_item(Item("Overturned Table",
                                         "Table overturned at the crime "
                                         "scene", "Leads you to believe "
                                                  "someone left in a hurry",
                                         3))
            self.crime_scene.add_clue("Smell of perfume")
            self.inventory.add_item(
                Item("Cigar", "Cigar at crime scene",
                     "You think that whoever did the crime smokes cigars", 1))
            self.crime_scene.investigated = True
        else:
            print(
                "You have already investigated the Crime Scene (Use 'r' to "
                "review the clues gathered)"
            )

    def user_guess(self):
        guilty = '1'
        interrogate_choice = input(
            "After reviewing your clues you have 3 possible suspects\n"
            "1. Mr. Reginald (the butler)\n"
            "2. Lady Victoria Starling\n"
            "3. The Chef\n"
            "Would you like to interrogate the suspects? (Y/N) : ")

        if interrogate_choice.lower() == 'y':
            suspect_interrogated_choice = input("\n\nwho would you like to interrogate ? \n"
                                                "1. Mr. Reginald (the butler)\n"
                                                "2. Lady Victoria Starling\n"
                                                "3. The Chef\n"
                                                "choose now : ")
            if suspect_interrogated_choice == '1':
                print("At first Mr. Reginald seems to be avoiding the"
                      " questions.\nas you continue to push he breaks and "
                      "admits it was him.")
                print("\ncongratulations Detective you have found the suspect")
                self.end_game()
            elif suspect_interrogated_choice == '2':
                print("Lady Victoria Starling was irate that you could even"
                      " think she did this and kicks you out of the mansion."
                      "\nYour investigation has come to an end........")
                self.end_game()
            elif suspect_interrogated_choice == '3':
                print("As you ask the chef questions you feel he is hiding"
                      " something.\nAfter an hour of probing he slips and tells"
                      " you he caught Mr. Reginald doing it last night\n"
                      " and agreed to be silent for a cut after the necklace is"
                      " sold \n")
                extra_interrogation = input("With this new information would"
                                            " you like to interrogate "
                                            "Mr. Reginald ? (Y/N) : ")
                if extra_interrogation.lower() == 'y':
                    print("\nWhen you present your finding to Mr. Reginalde "
                          "immediately admits defeat and confesses.")
                    self.end_game()
            else:
                raise ValueError(f"Invalid choice Detective: "
                                 f"{suspect_interrogated_choice}")

        elif interrogate_choice.lower() == 'n':
            guess = input("Who do you believe commited the crime? : ")
            if guilty.lower() == guess.lower():
                print("congratulations Detective you have found the suspect")
                self.end_game()
            else:
                print("unlucky detective you didnt find the suspect. the theif was"
                      "'Mr. Reginald (the butler)'")
                self.end_game()

        else:
            raise ValueError(f"Invalid choice Detective: "
                             f"{interrogate_choice}")

    def end_game(self):
        # Find the scores from the individual games
        haunted_game_score = self.game_scores["Haunted Mansion"]
        rps_score = self.game_scores["Rock Paper Scissors"]
        riddle_score = self.game_scores["Riddle"]

        # Calculate the final total score
        final_score = self.__score__() + haunted_game_score + rps_score + riddle_score

        # log_filename = input("Please enter a filename to save the logs:")
        self.log.save_logs_to_file("log_file")

        print(f"Game Over! Your final score was {final_score}")
        self.game_log.log(
            f"Player ended the game with a final score of" f" {final_score}"
        )

        # Update user's score in user_data.json
        self.update_user_score(self.username, final_score)
        self.store_clues()

        if final_score > 35:
            print("Well done, that's impressive!!")
        else:
            print("That's disappointing... expected better from you")

        self.running = False

    def store_clues(self):
        try:
            with open('user_data.json', 'r') as file:
                user_data = json.load(file)
        except FileNotFoundError:
            user_data = {}

        user_data[self.username]["name"] = self.player_name

        user_data[self.username]["Location_clues"] = {
            "CrimeScene": {
                "All clues found": self.crime_scene.all_clues_found,
                "Clues": self.crime_scene.review_clue(),
                "Visited": self.crime_scene.visited
            },
            "Attic": {
                "All clues found": self.attic.all_clues_found,
                "Clues": self.attic.review_clue(),
                "Visited": self.attic.visited
            },
            "Kitchen": {
                "All clues found": self.kitchen.all_clues_found,
                "Clues": self.kitchen.review_clue(),
                "Visited": self.kitchen.visited
            },
            "Library": {
                "All clues found": self.library.all_clues_found,
                "Clues": self.library.review_clue(),
                "Visited": self.library.visited
            },
            "Secret Passages": {
                "All clues found": self.library.all_clues_found,
                "Clues": self.secret_passages.review_clue(),
                "Visited": self.secret_passages.visited
            }
        }

        with open('user_data.json', 'w') as file:
            json.dump(user_data, file, indent=2)
