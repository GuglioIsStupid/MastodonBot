import json
import os
import requests
import random

idChars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

randomProfileColours = [
    "#ff0000",
    "#ff8000",
    "#ffff00",
    "#80ff00",
    "#00ff00",
    "#00ff80",
    "#00ffff",
    "#0080ff",
    "#0000ff",
    "#8000ff",
    "#ff00ff",
    "#ff0080",
]

# import image processing
from PIL import Image, ImageDraw, ImageFont

profilePath = "data/profiles/"

defaultProfileValues = {
    "money": 0,
    "inventory": [],
    "dailyTimer": 0,
}

def update_all_profiles():
    for file in os.listdir(profilePath):
        # does the file end with .json?
        if file.endswith(".json"):
            with open(profilePath + file, "r") as f:
                profile = json.load(f)
                for key in defaultProfileValues:
                    if key not in profile:
                        profile[key] = defaultProfileValues[key]
                save_profile(profile)

def create_profile(userId):
    profile = {
        "id": userId,
        "money": 0,
        "inventory": [],
    }

    with open(profilePath + userId + ".json", "w") as f:
        json.dump(profile, f)

def get_profile(userId):
    if not os.path.exists(profilePath + userId + ".json"):
        create_profile(userId)

    with open(profilePath + userId + ".json", "r") as f:
        return json.load(f)
    
def save_profile(profile):
    with open(profilePath + profile["id"] + ".json", "w") as f:
        json.dump(profile, f)

def update_profile(userId, key, value):
    profile = get_profile(userId)
    profile[key] = value
    save_profile(profile)

def get_stats(userId, profilePicture, displayName):
    #download profilePicture and save to temp/profiles/<randomID>.png
    randomID = ""
    for i in range(0, 10):
        randomID += idChars[random.randint(0, len(idChars) - 1)]
    response = requests.get(profilePicture)
    with open("temp/profiles/" + randomID + ".png", "wb") as f:
        f.write(response.content)
    
    # create a 1280x720 image data
    img = Image.new("RGB", (1280, 720), randomProfileColours[random.randint(0, len(randomProfileColours) - 1)])
    # paste the profile picture onto the image, resize to 256x256 to top left, but first draw a border
    pfp_img = Image.open("temp/profiles/" + randomID + ".png").resize((256, 256))
    # draw the border
    draw = ImageDraw.Draw(pfp_img)
    draw.rectangle([(0, 0), (256, 256)], outline=(0, 0, 0), width=5)
    # paste the image
    img.paste(pfp_img, (0, 0))
    # delete the profile picture
    os.remove("temp/profiles/" + randomID + ".png")
    # draw the text
    draw = ImageDraw.Draw(img)
    # set the font
    font = ImageFont.truetype("data/fonts/Roboto-Regular.ttf", 40)
    # draw the text
    draw.text((0, 256), "Stats for: " + displayName, (0, 0, 0), font=font)
    # draw the money
    draw.text((0, 344), "Money: $" + str(get_profile(userId)["money"]), (0, 0, 0), font=font)

    # save the image
    img.save("temp/profiles/" + randomID + ".png")

    # return the image
    return "temp/profiles/" + randomID + ".png"

update_all_profiles()