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
        'LatPullDown': 'Strength',
        'BicepPullDown': 'Strength',
        'PectoralFly': 'Strength',
        'LowRows': 'Strength',
        'DeadLift': 'Strength',
        'HammerCurl': 'Strength',
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
