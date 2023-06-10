import json
import os
import discord
import logging
from dotenv import load_dotenv

from Authentication import loginUser
from Commands.AvailableWorkouts import availableWorkouts

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


# Startup of the bot.
@client.event
async def on_ready():
    print(f"Client logged in as {client.user}")
    logger.info("Version 0.1")


# When a message is sent.
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    messageContent = str(message.content).lower()
    if not messageContent.startswith("<@1117078463187271680>"):
        return

    tokens = messageContent.replace("<@1117078463187271680> ", "").split("data=")

    userId = message.author.id
    command = tokens[0].strip()
    data = dict(json.loads(tokens[1].strip()))

    print(data)

    match command:
        case "login":
            await loginUser(str(data["username"]), str(data["password"]))
        case "add workout":
            workouts = await availableWorkouts()
            await message.channel.send(workouts)


client.run(TOKEN)
