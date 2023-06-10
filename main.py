import json
import os
import asyncio
import discord
import logging
import requests
from dotenv import load_dotenv

from Authentication import loginUser
from Commands.AddWorkout import addWorkout
from Commands.AvailableWorkouts import availableWorkouts
from Common import checkStatusCode, getDataFromResponse
from Routines.ChangeStatus import changeStatus

# Initialize logging.
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger.info('INFO: initializing GainsTrackerBot')

# Initialize environment.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set intents (permissions).
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

session = requests.session()
session.headers = {
    'Content-type': 'application/json',
    "accept": "application/json",
}
userTokensInSession = {}


# Startup of the bot.
@client.event
async def on_ready():
    print(f"Client logged in as {client.user}")
    logger.info("Version 0.1")
    client.loop.create_task(changeStatus(client))


# When a message is sent.
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    messageContent = str(message.content)
    if not messageContent.startswith("<@1117078463187271680>"):
        return

    tokens = messageContent.replace("<@1117078463187271680> ", "").split("data=")
    command = str(tokens[0].strip()).lower()

    userId = message.author.id
    if userId in userTokensInSession:
        jwt = userTokensInSession[userId]
        session.headers["Authorization"] = jwt
    elif command.strip() != "login":
        json_example = '''
login data={
    "username": "yourName", 
    "password": "yourPassword"
}'''
        embed = discord.Embed(title="You're not in the session", description="Please use the login command like so:")
        embed.add_field(name="Command", value=f'```json\n{json_example}\n```', inline=False)
        await message.channel.send(embed=embed)
        return

    data = {}

    if len(tokens) > 1:
        data = dict(json.loads(tokens[1].strip()))

    match command:
        case "login":
            response = await loginUser(str(data["username"]), str(data["password"]), session=session)
            if response.status_code != 200:
                await checkStatusCode(response, message.channel, data["username"])
                return

            userTokensInSession[userId] = getDataFromResponse(response)
            await message.channel.send(f"Successfully authenticated user {data['username']}.")
            await asyncio.sleep(2)
            await message.channel.send(f"**Let the gains begin!**")

        case "available workouts":
            response = await availableWorkouts(session=session)
            if response.status_code != 200:
                await checkStatusCode(response, message.channel)
                return

            workouts = getDataFromResponse(response)
            await message.channel.send(workouts)

        case "add workout":
            response = await addWorkout(data, session=session)
            if response.status_code != 200:
                await checkStatusCode(response, message.channel, data["workoutType"])
                return

            await message.channel.send("Successfully added workout. Let's put the _fit_ around f**ict**!")
            await asyncio.sleep(4)
            await message.channel.send("Still doesn't really roll of the tongue that well..")


client.run(TOKEN)
