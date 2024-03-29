import asyncio
import json
import logging
import re
from datetime import datetime, timedelta

import discord

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(message)s')


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


def totalSecondsFromTime(time):
    # yup this is great code, amazing even
    if time.isdigit() or (time.startswith('-') and time[1:].isdigit()):
        return int(time)

    elif time.count(':') == 2:
        time_format = "%H:%M:%S"
    elif time.count(':') == 1:
        time_format = "%M:%S"
    else:
        time_format = "%S"

    time_object = datetime.strptime(time, time_format)
    total_seconds = (time_object.hour * 3600) + (time_object.minute * 60) + time_object.second
    logger.info(f"total seconds: {total_seconds}")

    return total_seconds


def timeStringFromTotalSeconds(total_seconds):
    return str(timedelta(seconds=total_seconds))

