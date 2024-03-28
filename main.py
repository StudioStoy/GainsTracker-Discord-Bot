import logging
import os

import discord
from discord import app_commands
from dotenv import load_dotenv

from Commands.GetPBs import GetPBsCommand
from Commands.Help import HelpCommand
from Commands.LogNewWorkout import LogNewWorkoutCommand
from Commands.LogWorkout import LogWorkoutCommand
from Common.Constants import GAINS_VERSION
from GainsTrackerClient import GainsTrackerClient
from Infrastructure.autocomplete import new_workout_select_autocomplete, existing_workout_select_autocomplete, \
    clear_cached_workout_lists
from Routines.ChangeStatus import changeStatus

# Initialize logging.
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger.info('INFO: initializing GainsTrackerBot')

# Initialize environment.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILDS = str(os.getenv('GUILDS')).split(",")

# Set intents (permissions).
intents = discord.Intents.default()
intents.message_content = True
client = GainsTrackerClient(intents=intents, guild_ids=GUILDS)

# Startup of the bot.
@client.event
async def on_ready():
    logger.info(f"[INFO] Client logged in as {client.user}")
    logger.info(f"[INFO] Version {GAINS_VERSION}")

    logger.info("[INFO] Initialized BaseCommand with session and logger")

    client.loop.create_task(changeStatus(client))
    logger.info("[INFO] Created 'changing bot status' loop")

    logger.info("[INFO] Ready!")


@client.tree.command(description="Get an epic helpmenu! 🏅")
async def help(interaction: discord.Interaction):
    helpMenu = HelpCommand(interaction)
    logger.info("[INFO] Executing help command!")
    await helpMenu.execute()


@client.tree.command(description="Log a new workout! 💪")
@app_commands.autocomplete(workout=new_workout_select_autocomplete)
async def new(interaction: discord.Interaction, workout: str = ""):
    addWorkout = LogNewWorkoutCommand(interaction, workout)
    logger.info("[INFO] Executing new command!")
    await addWorkout.execute()
    clear_cached_workout_lists()


@client.tree.command(description="Log a measurement of an existing workout! 💪")
@app_commands.autocomplete(workout=existing_workout_select_autocomplete)
async def log(interaction: discord.Interaction, workout: str = ""):
    logWorkout = LogWorkoutCommand(interaction, workout)
    logger.info("[INFO] Executing log command!")
    await logWorkout.execute()
    clear_cached_workout_lists()


@client.tree.command(description="Get all your personal bests! 🏋")
@app_commands.choices(share=[app_commands.Choice(name="Yes", value="Yes"), app_commands.Choice(name="No", value="No")])
async def pbs(interaction: discord.Interaction, share: app_commands.Choice[str] = "No"):
    if isinstance(share, str):
        shouldShare = share == "Yes"
    else:
        shouldShare = share.value == "Yes"

    getPBs = GetPBsCommand(interaction, share=shouldShare)
    logger.info("[INFO] Executing pbs command!")
    await getPBs.execute()


# TODO: progress command.
# @client.tree.command()
# async def progress(interaction: discord.Interaction):
#     """Get your progress of a specific workout!"""
#     getProgress = GetProgressCommand(interaction)
#     logger.info("[INFO] Executing progress command!")
#     await getProgress.execute()


client.run(TOKEN)
