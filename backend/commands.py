import asyncio
import json
import os, time
import backend.profile as profile
import random
# set seed to current time
def command(name, description):
    # Decorator for commands

    def decorator(func):
        commands[name] = [func, description]
        return func

    return decorator

def daily(userID):
    cur_profile = profile.get_profile(userID)
    if (cur_profile["dailyTimer"] or 0) + 86400 <= time.time():
        random.seed(time.time())
        rand = random.randint(100, 175)
        cur_profile["money"] += rand
        if not cur_profile["dailyTimer"]:
            cur_profile["dailyTimer"] = time.time()

        profile.update_profile(userID, "dailyTimer", cur_profile["dailyTimer"])
        profile.update_profile(userID, "money", cur_profile["money"])

        return "You have claimed your daily reward of {} coins!".format(rand)
    else:
        return "You have already claimed your daily reward today!"

def gamble(userID, amount, choice):
    amount = int(amount)
    choice = int(choice)
    cur_profile = profile.get_profile(userID)
    if choice == None:
        return "You must choose either 1 or 2!"
    if cur_profile["money"] >= amount:
        cur_profile["money"] -= amount
        profile.update_profile(userID, "money", cur_profile["money"])

        random.seed(time.time())    
        if random.randint(1, 2) == choice:
            randomAmount = random.randint(1, 2) + random.random()
            cur_profile["money"] += int(amount * randomAmount)
            profile.update_profile(userID, "money", cur_profile["money"])
            return "You won " + str(int(amount * randomAmount)) + " coins!"
        else:
            return "You lost " + str(amount) + " coins :("
    else:
        return "You don't have enough money!"

def very_rare_chance_to_get_100000_coins(userID):
    random.seed(time.time())
    if random.randint(1, 100000) == 1:
        cur_profile = profile.get_profile(userID)
        cur_profile["money"] += 100000
        profile.update_profile(userID, "money", cur_profile["money"])
        return "You got 100000 coins from a very rare chance!"
    else:
        return "You didn't get 100000 coins from a very rare chance LOL"

def help_(userID):
    # Returns a string of all commands and their descriptions
    helpStr = "Commands:\n"
    for command in commands:
        helpStr += command + ": " + commands[command][1] + "\n"

    return helpStr

commands = {
    # Dictionary of commands (hold function pointers)

    # Command: [function, description]
    "daily": [daily, "Claim your daily reward\n- Usage: daily"],
    "gamble": [gamble, "Gamble your money away\n- Usage: gamble <amount> <choice>"],
    "very_rare_chance_to_get_100000_coins": [very_rare_chance_to_get_100000_coins, "Very rare chance to get 100000 coins\n- Usage: very_rare_chance_to_get_100000_coins"],
    "help": [help_, "Get a list of all commands\n- Usage: help"],
}