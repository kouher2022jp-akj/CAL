import json
import os
import random
import string

SAVE_FILE = "player_v2.json"


def load_user_name():
    if not os.path.exists(SAVE_FILE):
        number1 = "".join(random.choices(string.digits, k=4))

        letters = "".join(random.choices(string.ascii_uppercase, k=2))

        number2 = "".join(random.choices(string.digits, k=4))

        user_name = f"User{number1}{letters}{number2}"

        save_user_name(user_name)

        return user_name

    with open(SAVE_FILE, "r") as file:
        data = json.load(file)

    return data.get("user_name", "User Name")


def save_user_name(user_name):
    data = {}

    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            data = json.load(file)

    data["user_name"] = user_name

    with open(SAVE_FILE, "w") as file:
        json.dump(data, file)


def load_current_level():
    if not os.path.exists(SAVE_FILE):
        return 1

    with open(SAVE_FILE, "r") as file:
        data = json.load(file)

    return data.get("current_level", 1)


def save_current_level(current_level):
    data = {}

    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            data = json.load(file)

    data["current_level"] = current_level

    with open(SAVE_FILE, "w") as file:
        json.dump(data, file)


def delete_account():
    files_to_delete = [SAVE_FILE, "coins.json"]

    for file_name in files_to_delete:
        if os.path.exists(file_name):
            os.remove(file_name)

    return load_user_name()
