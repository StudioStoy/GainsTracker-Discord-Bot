import logging
import re

import discord
import requests
from discord.ui import Modal

from Common.Constants import GAINS_URL
from Common.Methods import tidyUpString, dontBeAnIdiot, totalSecondsFromTime
from Views.WorkoutDropDownView import getEmojiPerCategory
from Views.WorkoutInputs import inputsPerCategory

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(message)s')


class LogWorkoutModal(Modal):
    def __init__(self, selectedWorkoutData, session: requests.Session = None):
        super().__init__(
            title=f"{getEmojiPerCategory(selectedWorkoutData['c']) + tidyUpString(selectedWorkoutData['t'])}")

        logger.info(selectedWorkoutData)

        self.timeout = None
        self.session = session
        self.workoutData = selectedWorkoutData
        self.createInputFields(self.workoutData)
        self.on_submit = self.submitDataCallback

    def createInputFields(self, workoutData: dict):
        category = workoutData['c']

        for textInput in inputsPerCategory[category]:
            textInput: discord.ui.TextInput

            if textInput.custom_id == "generalInput":
                match workoutData['t']:
                    case "Bouldering":
                        textInput.label = "Boulder level"
                        textInput.placeholder = '5a+'
                        textInput.max_length = 3
                        textInput.style = discord.TextStyle.short

            self.add_item(textInput)

    async def submitDataCallback(self, interaction: discord.Interaction):
        data: dict = {}
        try:
            match self.workoutData["c"]:
                case "Strength":
                    data = {
                        "Weight": float(tryAndFindInputFromModal(interaction.data, "weightInput")),
                        "WeightUnit": "Kilograms",
                        "Reps": int(tryAndFindInputFromModal(interaction.data, "repsInput")),
                    }
                case "Reps":
                    data = {
                        "Reps": int(tryAndFindInputFromModal(interaction.data, "repsInput")),
                    }
                case "TimeEndurance":
                    timeInput = str(tryAndFindInputFromModal(interaction.data, "timeInput"))
                    data = {
                        "Time": await timeInputValidation(timeInput, interaction),
                    }
                case "TimeAndDistanceEndurance":
                    timeInput = str(tryAndFindInputFromModal(interaction.data, "timeInput"))
                    data = {
                        "Time": await timeInputValidation(timeInput, interaction),
                        "Distance": float(tryAndFindInputFromModal(interaction.data, "distanceInput")),
                        "DistanceUnit": "Kilometers",
                    }
                case "General":
                    data = {
                        "GeneralAchievement": str(tryAndFindInputFromModal(interaction.data, "generalInput")),
                    }
            data["Notes"] = str(tryAndFindInputFromModal(interaction.data, "notesInput"))
        except ValueError:
            await dontBeAnIdiot(interaction=interaction,
                                idiotReason="Please make sure you only input numbers or text where applicable, not both at the same time.",
                                insult="You peanut.")
            raise RuntimeError

        requestData = {
            "category": self.workoutData["c"],
            "data": data
        }

        response = self.session.post(url=f"{GAINS_URL}/gains/workout/{self.workoutData['i']}/measurement",
                                     json=requestData)

        if response.status_code == 200 or response.status_code == 204:
            await interaction.response.send_message("💪GAINS🏋️ (successfully added)", ephemeral=True)
        else:
            await interaction.response.send_message("Oopsie daisy something went wrong. Try again later bro.",
                                                    ephemeral=True)


def tryAndFindInputFromModal(interactionData, inputName):
    for comp in interactionData["components"]:
        textInput = comp["components"][0]
        if textInput["custom_id"] == inputName:
            return textInput["value"]


async def timeInputValidation(timeInput: str, interaction: discord.Interaction = None):
    pattern = re.compile(r"[0-9]?[0-9]?:?[0-9]?[0-9]?:?[0-9]?[0-9]", re.IGNORECASE)
    isValid = pattern.match(timeInput)

    seconds = totalSecondsFromTime(timeInput)

    if interaction is None:
        return isValid

    if seconds < 0:
        await dontBeAnIdiot(interaction=interaction,
                            idiotReason="...",
                            insult="Really?")
        return

    if not isValid:
        await dontBeAnIdiot(interaction=interaction,
                            idiotReason="Bro. Please only log the time in `hours (00:00:00)`, `minutes (00:00)` or `seconds (00)`.",
                            insult="Bro.")
        return

    elif seconds == 0:
        await dontBeAnIdiot(interaction=interaction,
                            idiotReason="Damn bro, only zero seconds bro? Watch out, you'll go negative next!",
                            insult="Go do a little more bro.")
        return

    return seconds
