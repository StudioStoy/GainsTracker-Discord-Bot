import json
import re


async def checkStatusCode(response, channel, param=""):
    message = ""
    match response.status_code:
        case 400:
            message = "Ai Caramba that's a bad request if I ever saw one."
        case 401:
            message = "Could not authenticate user."
        case 403:
            message = f"User {param} not authorized for this action."
        case 404:
            message = f"{param} not found."
        case 409:
            message = f"Conflict: {param} already exists/was already added."
        case _:
            return

    if message != "":
        await channel.send(message)
        raise Exception


def getDataFromResponse(response) -> json:
    return json.loads(response.content)


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
        'Cycling': 'TimeAndDistanceEndurance'
    }
    return types[workoutType]


def tidyUpString(string):
    tidiedString = re.sub(r'(?<![A-Z\W])(?=[A-Z])', ' ', string).lower().lstrip()
    return tidiedString.capitalize()
