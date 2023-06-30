import logging
import os

import discord
from dotenv import load_dotenv

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


# Startup of the bot.
@client.event
async def on_ready():
    logger.info(f"[INFO] Client logged in as {client.user}")
    logger.info(f"[INFO] Version {GAINS_VERSION}")

    client.loop.create_task(changeStatus(client))
    logger.info("[INFO] Created 'changing bot status' loop")

    logger.info("[INFO] Initialized BaseCommand with session and logger")

    logger.info("[INFO] Ready!")


@client.tree.command()
async def help(interaction: discord.Interaction):
    """Get an epic helpmenu!"""
    helpMenu = HelpCommand(interaction, logger)
    logger.info("[INFO] Executing help command!")
    await helpMenu.execute()


@client.tree.command()
async def new(interaction: discord.Interaction):
    """Log a new workout!"""
    addWorkout = LogNewWorkoutCommand(interaction, logger)
    logger.info("[INFO] Executing new command!")
    await addWorkout.execute()


@client.tree.command()
async def log(interaction: discord.Interaction):
    """Log a measurement of an existing workout!"""
    logWorkout = LogWorkoutCommand(interaction, logger)
    logger.info("[INFO] Executing log command!")
    await logWorkout.execute()


@client.tree.command()
async def progress(interaction: discord.Interaction):
    """Get your progress of a specific workout!"""
    getProgress = GetProgressCommand(interaction, logger)
    logger.info("[INFO] Executing progress command!")
    await getProgress.execute()


@client.tree.command()
async def pbs(interaction: discord.Interaction):
    """Get all your PB's!"""
    getPBs = GetPBsCommand(interaction, logger)
    logger.info("[INFO] Executing pbs command!")
    await getPBs.execute()


client.run(TOKEN)
