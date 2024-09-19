"""
inventory.py

This module defines the Inventory class, which manages the player's inventory.

Author: Sam Curran

Usage:
    # Example usage of the Inventory class
    player_inventory = Inventory()
    item = Item(name="Clue from Suspect", description="A crucial clue from a suspect.")
    player_inventory.add_item(item)
    player_inventory.use_item("Clue from Suspect", game_instance)
"""

class Inventory:
    """
    The Inventory class manages the player's inventory.
    """

    def __init__(self):
        """
        Initialize an empty inventory.
        """
        self.items = []

    def add_item(self, item):
        """
        Add an item to the inventory.

        :param item: The item to be added to the inventory.
        """
        self.items.append(item)
        print(f"You added {item.name} to your inventory.")

    def use_item(self, item_name, game):
        """
        Use an item from the inventory.

        :param item_name: The name of the item to be used.
        :param game: The game instance on which the item is used.
        """
        item = next((item for item in self.items if item.name.lower() == item_name.lower()), None)
        if item:
            item.use(game)
            self.items.remove(item)
            print(f"{item.name} has been removed from your inventory.")
        else:
            print(f"You don't have {item_name} in your inventory.")

    def print_inventory(self):
        """Print all items in the player's inventory."""
        if self.items:
            print("Items in your inventory:")
            for item in self.items:
                print(f"- {item.name}: {item.description}")
        else:
            print("Your inventory is empty.")