import asyncio
import json
import logging
import re
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
