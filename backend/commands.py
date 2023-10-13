import asyncio
import json
import os, time
import backend.profile as profile
import random, math

from PIL import Image, ImageDraw, ImageFont
# set seed to current time

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


#### Start of gambling commands ####
def gamble(userID, amount, choice):
    if type(amount) == str and amount == "all":
        amount = profile.get_profile(userID)["money"]
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

def gamble_all(userID, choice):
    return gamble(userID, "all", choice)

def spin(userID, notif):
    print("spin")
    # is coins >= 1000?
    cur_profile = profile.get_profile(userID)

    if cur_profile["money"] >= 1000:
        # create a gif of a spinning wheel
        _spinnerSegments = [
            500,
            500,
            1000,
            1000,
            1000,
            2000,
            250,
            1,
            100,
        ]

        images = []
        _imgWidth = 500
        _imgHeight = 500

        _center = (_imgWidth // 2, _imgHeight // 2)

        _spinnerSegmentColours = [
            (255, 0, 0),
            (255, 255, 0),
            (0, 255, 0),
            (0, 255, 255),
            (0, 0, 255),
            (255, 0, 255),
            (255, 255, 255),
            (100, 100, 100),
            (255, 255, 255),
        ]

        _step = len(_spinnerSegments)

        # create original image
        image = Image.new("RGB", (_imgWidth, _imgHeight), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        # draw the segments
        for i in range(_step):
            draw.pieslice(
                [
                    (_center[0] - _imgWidth // 2, _center[1] - _imgHeight // 2),
                    (_center[0] + _imgWidth // 2, _center[1] + _imgHeight // 2),
                ],
                360 // _step * i,
                360 // _step * (i + 1),
                fill=_spinnerSegmentColours[i],
            )

        # save the original image
        images.append(image)

        # create the other images

        # choose our random segment
        random.seed(time.time())
        _randomSegment = random.randint(0, _step - 1)

        # set angle to segment position
        _angle = 360 // _step * _randomSegment

        # make a gif of the wheel spinning to the random segment (3 turns)
        for i in range(3 * _step):
            # create new image
            image = Image.new("RGB", (_imgWidth, _imgHeight), (255, 255, 255))
            draw = ImageDraw.Draw(image)            # draw the segments
            for j in range(_step):
                draw.pieslice(
                    [
                        (_center[0] - _imgWidth // 2, _center[1] - _imgHeight // 2),
                        (_center[0] + _imgWidth // 2, _center[1] + _imgHeight // 2),
                    ],
                    360 // _step * j + _angle + 180,
                    360 // _step * (j + 1) + _angle + 180,
                    fill=_spinnerSegmentColours[j],
                )

            # draw numbers and pointer on the right
            draw.polygon(
                [
                    (_center[0] + _imgWidth // 2 - 20, _center[1]),
                    (_center[0] + _imgWidth // 2, _center[1] - 10),
                    (_center[0] + _imgWidth // 2, _center[1] + 10),
                ],
                fill=(0, 0, 0),
            )

            for j in range(_step):
                # draw the text
                font = ImageFont.truetype("data/fonts/Roboto-Regular.ttf", 40)
                text = str(_spinnerSegments[j])
                textWidth, textHeight = font.getsize(text)
                draw.text( 
                    (
                        # from the center, offsetted by 50px
                        _center[0] * math.cos(math.radians(360 // _step * j + _angle + 180)) + _center[0] - textWidth // 2 - 50,
                        _center[1] * math.sin(math.radians(360 // _step * j + _angle + 180)) + _center[1] - textHeight // 2 - 50
                    ),
                    text,
                    (0, 0, 0),
                    font=font,
                )

            # set its last frame to the original image

            # save the image
            images.append(image)

            # increment the angle
            _angle += 360 // _step

        # set the last 15 frames to the random segment
        for i in range(15):
            # create new image
            image = Image.new("RGB", (_imgWidth, _imgHeight), (255, 255, 255))
            draw = ImageDraw.Draw(image)            # draw the segments
            for j in range(_step):
                draw.pieslice(
                    [
                        (_center[0] - _imgWidth // 2, _center[1] - _imgHeight // 2),
                        (_center[0] + _imgWidth // 2, _center[1] + _imgHeight // 2),
                    ],
                    360 // _step * j + _angle + 180,
                    360 // _step * (j + 1) + _angle + 180,
                    fill=_spinnerSegmentColours[j],
                )
            
            # draw numbers and pointer on the right
            draw.polygon(
                [
                    (_center[0] + _imgWidth // 2 - 20, _center[1]),
                    (_center[0] + _imgWidth // 2, _center[1] - 10),
                    (_center[0] + _imgWidth // 2, _center[1] + 10),
                ],
                fill=(0, 0, 0),
            )

            for j in range(_step):
                # draw the text
                font = ImageFont.truetype("data/fonts/Roboto-Regular.ttf", 40)
                text = str(_spinnerSegments[j])
                textWidth, textHeight = font.getsize(text)
                draw.text( 
                    (
                        _center[0] * math.cos(math.radians(360 // _step * j + _angle + 180)) + _center[0] - textWidth // 2 - 50,
                        _center[1] * math.sin(math.radians(360 // _step * j + _angle + 180)) + _center[1] - textHeight // 2 - 50
                    ),
                    text,
                    (0, 0, 0),
                    font=font,
                )

            # set its last frame to the original image

            # save the image
            images.append(image)

        # on all images, set a black pointer on the right side of the image
        # (and print the text onto the correct segment)
        for i in range(len(images)):
            image = images[i]
            draw = ImageDraw.Draw(image)

            # draw the pointer
            draw.polygon(
                [
                    (_center[0] + _imgWidth // 2 - 20, _center[1]),
                    (_center[0] + _imgWidth // 2, _center[1] - 10),
                    (_center[0] + _imgWidth // 2, _center[1] + 10),
                ],
                fill=(0, 0, 0),
            )

            # save the image
            images[i] = image


        # create the gif
        images[0].save(
            "data/spinners/" + userID + ".gif",
            save_all=True,
            append_images=images[1:],
            duration=100,
            loop=0,
        )

        # upload the gif
        #media = bot.media_post("data/spinners/" + userID + ".gif", "image/gif")

        # post the gif
        #bot.status_post(
        #    "Here is your spinner!",
        #    in_reply_to_id=notif.status["id"],
        #    media_ids=[media],
        #)
        return "data/spinners/" + userID + ".gif"

def money(userID):
    cur_profile = profile.get_profile(userID)
    return "You have " + str(cur_profile["money"]) + " coins!"

def very_rare_chance_to_get_100000_coins(userID):
    random.seed(time.time())
    if random.randint(1, 100000) == 1:
        cur_profile = profile.get_profile(userID)
        cur_profile["money"] += 100000
        profile.update_profile(userID, "money", cur_profile["money"])
        return "You got 100000 coins from a very rare chance!"
    else:
        return "You didn't get 100000 coins from a very rare chance LOL"

def recommend(userID, *thing):
    thing = " ".join(thing)
    cur_profile = profile.get_profile(userID)
    if len(thing) == 0:
        return "You must provide a thing to recommend me!"
    else:
        try:
            with open("data/recommendations/" + userID + ".json", "r") as f:
                recommendations = json.load(f)
                recommendations.append(thing)
                with open("data/recommendations/" + userID + ".json", "w") as f:
                    json.dump(recommendations, f)
        except:
            with open("data/recommendations/" + userID + ".json", "w") as f:
                json.dump([thing], f)
        return "Your recommendation has been added! @_, please review it!"

    return "You must provide a reason!"

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
    "gamble_all": [gamble_all, "Gamble all your money away\n- Usage: gamble_all <choice>"],
    "spin": [spin, "Spin the wheel of fortune\n- Usage: spin"],
    "very_rare_chance_to_get_100000_coins": [very_rare_chance_to_get_100000_coins, "Very rare chance to get 100000 coins\n- Usage: very_rare_chance_to_get_100000_coins"],
    "recommend": [recommend, "Recommend something to me\n- Usage: recommend <thing>"],
    "help": [help_, "Get a list of all commands\n- Usage: help"],
}