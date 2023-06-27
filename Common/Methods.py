import asyncio
import json
import re

import discord
import requests

from Infrastructure.Login import login


async def checkStatusCode(response: requests.Response, interaction: discord.Interaction, param=""):
    message = ""
    match response.status_code:
        case 400:
            message = "Ai Caramba that's a bad request if I ever saw one."
        case 401:
            await interaction.response.defer()
            await login(interaction.user.id, interaction)
        case 403:
            message = f"User {param} not authorized for this action."
        case 404:
            message = f"{param} not found."
        case 409:
            message = f"Conflict: {param} already exists/was already added."
        case 500:
            message = "Something went wrong, my bad g"
        case _:
            return

    print(f"[WARNING]: {response.content}")

    if message != "":
        await interaction.channel.send(message)
        raise Exception


def getDataFromResponse(response) -> json:
    if response.content is None:
        return None

    try:
        return json.loads(response.content)
    except json.decoder.JSONDecodeError:
        # Sometimes, he say no. Meaning: even though it is pretty valid json, it cannot decode it starting with "b'".
        if str(response.content).startswith("b'"):
            return str(response.content).removeprefix("b'").removesuffix("'")
        # Otherwise, there's no hope for this man.


# TODO: Move this method to the backend API probably, as now the maintainability is abysmal here.
def categoryFromType(workoutType: str):
    types = {
        'Squat': 'Strength',
        'Abduction': 'Strength',
        'Adduction': 'Strength',
        'BenchPress': 'Strength',
        'CalfExtensions': 'Strength',
        'HackSquat': 'Strength',
        'LegPress': 'Strength',
        'ShoulderPress': 'Strength',
        'DumbbellPress': 'Strength',
        'DumbbellCurl': 'Strength',
        'ClosePullUp': 'Reps',
        'WidePullUp': 'Reps',
        'DiamondPushUp': 'Reps',
        'ClosePushUp': 'Reps',
        'WidePushUp': 'Reps',
        'Planking': 'TimeEndurance',
        'JumpingJacks': 'TimeEndurance',
        'JumpingRope': 'TimeEndurance',
        'Walking': 'TimeAndDistanceEndurance',
        'Running': 'TimeAndDistanceEndurance',
        'Cycling': 'TimeAndDistanceEndurance',
        'Bouldering': 'General'
    }
    return types[workoutType]


def getEmojiPerCategory(category):
    match category:
        case "Strength":
            return '🏋️'
        case "Reps":
            return '💪'
        case "TimeEndurance":
            return '⏱'
        case "TimeAndDistanceEndurance":
            return '🚀'
        case "General":
            return '💫'


def tidyUpString(string):
    tidiedString = re.sub(r'(?<![A-Z\W])(?=[A-Z])', ' ', string).lower().lstrip()
    return tidiedString.capitalize()


async def dontBeAnIdiot(interaction: discord.Interaction, idiotReason: str, insult: str):
    await interaction.response.send_message(idiotReason, ephemeral=True)
    await asyncio.sleep(2)
    await interaction.followup.send(insult, ephemeral=True)
