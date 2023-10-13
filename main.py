from mastodon import Mastodon, StreamListener
import os, json, requests, time
import asyncio
import backend.profile as profile
import backend.commands as commands
__use_test_account__ = True
global loginInfo, testStr
if __use_test_account__:
    loginInfo = {
        "emailORuser": open("secret/email-test.email", "r").read(),
        "password": open("secret/password-test.password", "r").read()
    }
    testStr = ""
else:
    testStr = ""
url = open("secret/url.secret", "r").read().strip()
""" Mastodon.create_app(
    'BotTesting',
    api_base_url = url,
    to_file = 'secret/botinfo.bot'
)  """

bot = Mastodon(
    client_id = 'secret/botinfo.bot',
    access_token = "secret/usercred.secret",
    api_base_url = url
)

bot.log_in(
    loginInfo["emailORuser"],
    loginInfo["password"],
    scopes = ['read', 'write']
)

# setup listener
listener = StreamListener()
# start listener
#bot.toot(testStr + "hillo peoples")
#bot.stream_public(listener, run_async=True, reconnect_async=True)

async def checkMentions():
    for notif in bot.notifications():
        if notif["type"] == "mention":
            if "@<span>GuglioBotTest</span>" in notif.status.content:
                # from the content
                content = notif.status["content"]
                # remove the html tags (will vary depending on the content)
                if content.startswith("<span class=\"h-card\">"):
                    #remove everything up to the last > and strip the spaces from start and end
                    content = content[content.rfind(">") + 1:].strip()
                content = content.strip()
                # if content starts with profile
                if content.startswith("profile"):
                    userID = notif.status["account"]["id"]
                    profilePictureURL = notif.status["account"]["avatar"]
                    displayName = notif.status["account"]["display_name"]
                    image = profile.get_stats(userID, profilePictureURL, displayName)

                    # upload image
                    media = bot.media_post(image, "image/png")
                    # post status
                    bot.status_post(testStr + "Here is your profile!", in_reply_to_id=notif.status["id"], media_ids=[media])

                    os.remove(image)
                else:
                    try:
                        command = content.split(" ")[0]
                        uid = notif.status["account"]["id"]
                        response = commands.commands[command][0](uid, *content.split(" ")[1:])

                        bot.status_post(testStr + response, in_reply_to_id=notif.status["id"])
                    except KeyError:
                        bot.status_post(testStr + "Command not found!", in_reply_to_id=notif.status["id"])
        
    bot.notifications_clear()

async def checkForDailyReset():
    # 12am EST
    curTime = time.time()

    # get current hour
    curHour = time.localtime(curTime).tm_hour
    curMinute = time.localtime(curTime).tm_min
    curSecond = time.localtime(curTime).tm_sec

    # get seconds until 12am EST
    secondsUntilReset = (24 - curHour) * 3600 - curMinute * 60 - curSecond

    # wait until 12am EST
    await asyncio.sleep(secondsUntilReset)

    # reset daily timers
    for file in os.listdir(profile.profilePath):
        # does the file end with .json?
        if file.endswith(".json"):
            with open(profile.profilePath + file, "r") as f:
                profile = json.load(f)
                profile["dailyTimer"] = 0
                profile.save_profile(profile)

async def main():
    while True:
        #print("loop")
        await checkMentions()
        await checkForDailyReset()
        # wait 1 second
        await asyncio.sleep(1)

asyncio.run(main())
#bot.user_stream(listener)