import pygame
import json
import os

def calculate_coins(question_start_ticks, limit_seconds=15):
    limit_milliseconds = limit_seconds * 1000

    elapsed_milliseconds = pygame.time.get_ticks() - question_start_ticks

    remaining_milliseconds = max(0, limit_milliseconds - elapsed_milliseconds)

    coin = round(remaining_milliseconds / limit_milliseconds * 100)

    return coin

#------------------------------------------------
SAVE_FILE = "coins.json"


def load_total_coins():
    if not os.path.exists(SAVE_FILE):
        return 0

    with open(SAVE_FILE, "r") as file:
        data = json.load(file)

    return data.get("total_coins", 0)


def save_total_coins(total_coins):
    with open(SAVE_FILE, "w") as file:
        json.dump({"total_coins": total_coins}, file)


def add_coins(total_coins, amount):
    total_coins += amount

    save_total_coins(total_coins)

    return total_coins
