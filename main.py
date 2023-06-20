import logging
import os

import discord
import requests
from dotenv import load_dotenv

from BaseCommand import BaseCommand
from Commands.GetPBs import GetPBsCommand
from Commands.GetProgress import GetProgressCommand
from Commands.Help import HelpCommand
from Commands.LogNewWorkout import LogNewWorkoutCommand
from Commands.LogWorkout import LogWorkoutCommand
from Common.Constants import GAINS_VERSION
from GainsTrackerClient import GainsTrackerClient
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
client = GainsTrackerClient(intents=intents)

session = requests.session()
session.headers = {
    'Content-type': 'application/json',
    "accept": "application/json",
}


# Startup of the bot.
@client.event
async def on_ready():
    logger.info(f"[INFO] Client logged in as {client.user}")
    logger.info(f"[INFO] Version {GAINS_VERSION}")

    client.loop.create_task(changeStatus(client))
    logger.info("[INFO] Created 'changing bot status' loop")

    BaseCommand.setSession(session)
    BaseCommand.setLogger(logger)
    logger.info("[INFO] Initialized BaseCommand with session and logger")

    logger.info("[INFO] Ready!")


@client.tree.command()
async def help(interaction: discord.Interaction):
    """Get an epic helpmenu!"""
    await BaseCommand.initialize(interaction)
    helpMenu = HelpCommand()
    await helpMenu.execute()


@client.tree.command()
async def new(interaction: discord.Interaction):
    """Log a new workout!"""
    await BaseCommand.initialize(interaction)
    addWorkout = LogNewWorkoutCommand()
    await addWorkout.execute()


@client.tree.command()
async def log(interaction: discord.Interaction):
    """Log a measurement of an existing workout!"""
    await BaseCommand.initialize(interaction)
    logWorkout = LogWorkoutCommand()
    await logWorkout.execute()


@client.tree.command()
async def progress(interaction: discord.Interaction):
    """Get your progress of a specific workout!"""
    await BaseCommand.initialize(interaction)
    getProgress = GetProgressCommand()
    await getProgress.execute()


@client.tree.command()
async def pbs(interaction: discord.Interaction):
    """Get all your PB's!"""
    await BaseCommand.initialize(interaction)
    getPBs = GetPBsCommand()
    await getPBs.execute()


client.run(TOKEN)
