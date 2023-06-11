import json
import logging
import os

import discord
import requests
from dotenv import load_dotenv

from BaseCommand import BaseCommand
from Commands.AddWorkout import AddWorkoutCommand
from Commands.AvailableWorkouts import AvailableWorkoutsCommand
from Commands.Login import LoginCommand
from Common.Methods import getDataFromResponse
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
    logger.info("[INFO] Version 0.1")
    client.loop.create_task(changeStatus(client))
    BaseCommand.setSession(session)
    logger.info("[INFO] Initialized session and added to BaseCommand")
    logger.info("[INFO] Ready!")


# When a message is sent.
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    messageContent = str(message.content)
    if not messageContent.startswith("<@1117078463187271680>"):
        return

    BaseCommand.setMessage(message)

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
            login = LoginCommand(str(data["username"]), str(data["password"]))
            response = await login.execute()
            userTokensInSession[userId] = getDataFromResponse(response)
        case "available workouts":
            availableWorkouts = AvailableWorkoutsCommand()
            await availableWorkouts.execute()
        case "add workout":
            addWorkout = AddWorkoutCommand(data)
            await addWorkout.execute()


client.run(TOKEN)
