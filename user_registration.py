# user_registration.py

"""
User Registration Module

Description:
This Python module provides functions for user registration and login using a JSON file to store user data.
It includes password hashing for enhanced security.

Functions:
1. register_user(username, password): Registers a new user with a unique username and hashed password.
2. login_user(username, password): Validates user login credentials by checking the entered password against the stored hashed password.

Usage:
- Import this module into your Python program to use the user registration and login functionalities.

Authors: Sam Curran, Hayden Carroll
Date: 26/11/2023

Note: Make sure to have the 'user_data.json' file available for user data storage.
"""

import json
import bcrypt


def register_user(username, password):
    # Load existing user data from JSON file
    try:
        with open('user_data.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}

    # Check if the username is already taken
    if username.lower() in users:
        print("Username already exists. Please choose a different one.")
        return False

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Save user data to JSON file with an initial score of 0
    users[username.lower()] = {"name": username, 'hashed_password':
        hashed_password.decode('utf-8'), 'score': 0}
    with open('user_data.json', 'w') as file:
        json.dump(users, file, indent=2)

    return True


def login_user(username, password):
    # Load user data from JSON file
    try:
        with open('user_data.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        print("No users registered yet, please register to continue")
        return False

    # Check if the username exists
    if username not in users:
        print("Username not found, please try again or register to continue")
        return False

    # Retrieve hashed password
    stored_hashed_password = users[username]['hashed_password']

    counter = 5
    while counter > 0:
        # Verify the entered password
        if bcrypt.checkpw(password.encode('utf-8'),
                          stored_hashed_password.encode('utf-8')):
            return True
        else:
            counter -= 1
            print(f"Incorrect password,{counter} attempts left, try again")
            password = input("Enter your password: ")

    return False
