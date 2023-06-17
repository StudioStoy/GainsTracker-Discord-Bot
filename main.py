import logging
import os

import discord
import requests
from dotenv import load_dotenv

from BaseCommand import BaseCommand
from Commands.GetProgress import GetProgressCommand
from Commands.LogNewWorkout import LogNewWorkoutCommand
from Commands.GetPBs import GetPBsCommand
from Commands.Help import HelpCommand
from Commands.LogWorkout import LogWorkoutCommand
from Commands.Login import LoginCommand
from Common.Constants import GAINS_BOT
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

    tokens = messageContent.replace("<@1117078463187271680> ", "").split(":", 1)
    command = str(tokens[0].strip()).lower()

    userId = message.author.id
    if userId not in userTokensInSession and command.strip() != "help":
        login = LoginCommand(userId)
        response = await login.execute()
        userTokensInSession[userId] = getDataFromResponse(response)

    if userTokensInSession.__contains__(userId):
        session.headers["Authorization"] = userTokensInSession[userId]

    match command:
        case "login":
            login = LoginCommand(userId)
            response = await login.execute()
            userTokensInSession[userId] = getDataFromResponse(response)
        case "help":
            helpMenu = HelpCommand()
            await helpMenu.execute()
        case "new workout":
            addWorkout = LogNewWorkoutCommand()
            await addWorkout.execute()
        case "progress":
            getProgress = GetProgressCommand()
            await getProgress.execute()
        case "pbs":
            getPBs = GetPBsCommand()
            await getPBs.execute()
        case "log workout":
            logWorkout = LogWorkoutCommand()
            await logWorkout.execute()
        case _:
            await message.channel.send(f"Unknown command chief. Try {GAINS_BOT} `help` for a list of commands.")


client.run(TOKEN)
