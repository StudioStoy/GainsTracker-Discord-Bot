import logging

import discord
from discord import app_commands

from Requests.GetAvailableNewWorkouts import GetAvailableNewWorkoutsRequest
from Requests.GetExistingWorkouts import GetExistingWorkoutsRequest

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(message)s')

cachedNewWorkouts = []
cachedExistingWorkouts = []


async def new_workout_select_autocomplete(interaction: discord.Interaction, current: str) \
        -> list[app_commands.Choice[str]]:
    global cachedNewWorkouts
    if len(cachedNewWorkouts) == 0:
        cachedNewWorkouts = await GetAvailableNewWorkoutsRequest(interaction=interaction).execute()

    return [
        app_commands.Choice(name=workout["type"], value=workout["type"])
        for workout in cachedNewWorkouts if current.lower() in str(workout["type"].lower())
    ]


async def existing_workout_select_autocomplete(interaction: discord.Interaction, current: str) \
        -> list[app_commands.Choice[str]]:
    global cachedExistingWorkouts
    if len(cachedExistingWorkouts) == 0:
        logger.info("Requested.")
        cachedExistingWorkouts = await GetExistingWorkoutsRequest(interaction=interaction).execute()

    return [
        app_commands.Choice(name=workout["type"], value=workout["type"])
        for workout in cachedExistingWorkouts if current.lower() in str(workout["type"].lower())
    ]


def clear_cached_workout_lists():
    global cachedNewWorkouts
    global cachedExistingWorkouts
    cachedNewWorkouts = []
    cachedExistingWorkouts = []
