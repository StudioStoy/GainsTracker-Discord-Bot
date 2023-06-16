import json
import logging
import os

import discord
import requests
from dotenv import load_dotenv

from BaseCommand import BaseCommand
from Commands.LogNewWorkout import LogNewWorkoutCommand
from Commands.AvailableMeasurements import AvailableMeasurementsCommand
from Commands.AvailableWorkouts import AvailableWorkoutsCommand
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
    if userId in userTokensInSession:
        jwt = userTokensInSession[userId]
        session.headers["Authorization"] = jwt
    elif command.strip() != "login" and command.strip() != "help":
        json_example = '''login: username password'''
        embed = discord.Embed(title="You're not in the session", description="Please use the login command like so:")
        embed.add_field(name="Command", value=f'```json\n{json_example}\n```', inline=False)
        await message.channel.send(embed=embed)
        return

    data = {}

    if len(tokens) > 1:
        try:
            data = dict(json.loads(tokens[1].strip()))
        except json.decoder.JSONDecodeError:
            data = tokens[1].strip()

    match command:
        case "login":
            namePassword = data.split(" ")
            login = LoginCommand(str(namePassword[0]), str(namePassword[1]))
            response = await login.execute()
            userTokensInSession[userId] = getDataFromResponse(response)
        case "help":
            helpMenu = HelpCommand()
            await helpMenu.execute()
        case "workouts":
            availableWorkouts = AvailableWorkoutsCommand()
            await availableWorkouts.execute()
        case "log new workout":
            addWorkout = LogNewWorkoutCommand()
            await addWorkout.execute()
        case "measurements":
            availableMeasurements = AvailableMeasurementsCommand()
            await availableMeasurements.execute()
        case "log workout":
            logWorkout = LogWorkoutCommand()
            await logWorkout.execute()
        case "log workout":
            logNewWorkout = LogNewWorkoutCommand()
            await logNewWorkout.execute()
        case _:
            await message.channel.send(f"Unknown command chief. Try {GAINS_BOT}`help` for a list of commands.")


client.run(TOKEN)
