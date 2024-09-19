"""
characters.py

This module defines the Character, NPC, Suspect, and Witness classes for characters in a crime investigation game.

Author: Haydens Little Helpers
Date: 18/11/2023

Description: - The Character class serves as the base class, providing
common attributes and methods for characters. - The Suspect and Witness
classes are subclasses that inherit from Character and introduce their
unique attributes and methods. - The NPC class represents non-player
characters with general interactions. - The Suspect class represents
characters under suspicion in the crime investigation, providing alibis and
potential deception cues. - The Witness class represents characters who have
witnessed or heard something related to the crime, sharing observations.

Classes:
    - Character: Base class with common attributes and methods for characters.
    - NPC: Non-player character class inheriting from Character.
    - Suspect: Represents characters under suspicion with alibi information.
    - Witness: Represents characters who have witnessed or heard something related to the crime.

"""

# Import necessary modules and classes

from abc import ABC, abstractmethod


# Define a base class for characters


class Character(ABC):
    """ The Character class serves as the base class, providing common
    attributes and methods for characters. The Suspect and Witness classes
    are subclasses that inherit from Character and introduce their unique
    attributes and methods. """

    def __init__(self, name, dialogue, action, age):
        self._name = name
        self._dialogue = dialogue
        self._interacted = False
        self.action = action
        self.age = age

    def interact(self):
        if not self._interacted:
            interaction = f"{self._name}: {self._dialogue}"
            self._interacted = True
        else:
            interaction = f"{self._name} is no longer interested in talking."

        return interaction

    @property
    def name(self):
        return self._name

    @abstractmethod
    def perform_action(self):
        pass


# Define an NPC class
class NPC(Character):
    def __init__(self, name, dialogue, action, age):
        super().__init__(name, dialogue, action, age)

    @property
    def interact(self):
        if not self._interacted:
            self._interacted = True
            return f'{self._name}: "{self._dialogue}"'
        else:
            return f"{self._name} is no longer interested in talking."

    def perform_action(self):
        return f"{self._name} {self.action}"

    # Define a property to get the name
    @property
    def name(self):
        return self._name

    # Define a property to get the dialogue

    @property
    def dialogue(self):
        return self._dialogue


# Define a suspect character class
class Suspect(Character):
    """This is a special type of character. This is the suspect in our crime
    investigation."""

    def __init__(self, name, dialogue, alibi, action, age):
        super().__init__(name, dialogue, action, age)
        self._alibi = alibi

    def __repr__(self):
        return f"{self._name}: {self._dialogue}. Their Alibi: {self._alibi}"

    def provide_alibi(self):
        return f"{self._name}'s Alibi: {self._alibi}"

    def interact(self):
        if not self._interacted:
            interaction = (
                f"§{self._name} reacts nervously:"
                f"{self._dialogue}"
            )
            interaction += (
                "\nYou notice subtle body language cues indicating potential "
                "deception"
            )
            self._interacted = True
        else:
            interaction = (
                f"Suspect {self._name} avoids eye contact and "
                "remains silent."
            )

        return interaction

    def perform_action(self):
        return f"{self._name} {self.action}"

    @property
    def interacted(self):
        return self._interacted

    # Define a property to get the name
    @property
    def name(self):
        return self._name


# Define a witness character class
class Witness(Character):
    """This class is the witness. This person has either seen or heard
    something to do with the crime."""

    def __init__(self, name, dialogue, observation, action, age):
        super().__init__(name, dialogue, action, age)
        self.observation = observation

    def share_observation(self):
        return f"{self._name}'s Observation: {self.observation}"

    def interact(self):
        if not self._interacted:
            interaction = (
                f"Witness {self._name} speaks hurriedly: "
                f"{self._dialogue}"
            )
            interaction += (
                "\nYou sense genuine anxiety and urgency in the "
                "witness's words."
            )
            self._interacted = True
        else:
            interaction = f"Witness {self._name} hesitates and murmurs softly."

        return interaction

    def perform_action(self):
        return f"{self._name} {self.action}"

    @property
    def interacted(self):
        return self._interacted

    # Define a property to get the name
    @property
    def name(self):
        return self._name
