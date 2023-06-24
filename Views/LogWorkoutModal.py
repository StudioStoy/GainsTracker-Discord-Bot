import re
from datetime import datetime

import discord
import requests
from discord.ui import Modal

from Common.Constants import BASE_URL
from Common.Methods import checkStatusCode, categoryFromType, tidyUpString, dontBeAnIdiot
from Views.WorkoutDropDownView import getEmojiPerCategory
from Views.WorkoutInputs import inputsPerCategory


class LogWorkoutModal(Modal):
    def __init__(self, selectedWorkoutData, session: requests.Session = None):
        super().__init__(
            title=f"{getEmojiPerCategory(categoryFromType(selectedWorkoutData['type'])) + tidyUpString(selectedWorkoutData['type'])}")

        self.timeout = None
        self.session = session
        self.workoutData = selectedWorkoutData
        self.createInputFields(self.workoutData)
        self.on_submit = self.submitDataCallback

    def createInputFields(self, workoutData: dict):
        category = categoryFromType(workoutData['type'])

        for textInput in inputsPerCategory[category]:
            textInput: discord.ui.TextInput

            # TODO: Create better way to set placeholders for specific workout types.
            if textInput.custom_id == "generalInput" and workoutData['type'] == "Bouldering":
                textInput.label = "Boulder level"
                textInput.placeholder = '5a+'
                textInput.max_length = 3
                textInput.style = discord.TextStyle.short

            self.add_item(textInput)

    async def submitDataCallback(self, interaction: discord.Interaction):
        data: dict = {}
        try:
            match categoryFromType(self.workoutData["type"]):
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
                    await timeInputValidation(timeInput, interaction)

                    data = {
                        "Time": timeInput,
                    }
                case "TimeAndDistanceEndurance":
                    timeInput = str(tryAndFindInputFromModal(interaction.data, "timeInput"))
                    await timeInputValidation(timeInput, interaction)

                    data = {
                        "Time": timeInput,
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
            "category": categoryFromType(self.workoutData["type"]),
            "data": data
        }

        response = self.session.post(url=f"{BASE_URL}/gains/workout/{self.workoutData['id']}/measurement",
                                     json=requestData)

        if not response.status_code == 204 or not response.status_code == 200:
            await checkStatusCode(response, interaction)

        await interaction.response.send_message("GAINZZZZZZZZ (successfully added)", ephemeral=True)


def tryAndFindInputFromModal(interactionData, inputName):
    for comp in interactionData["components"]:
        textInput = comp["components"][0]
        if textInput["custom_id"] == inputName:
            return textInput["value"]


async def timeInputValidation(timeInput: str, interaction: discord.Interaction = None):
    pattern = re.compile(r"[0-9]?[0-9]?:?[0-9]?[0-9]?:?[0-9]?[0-9]", re.IGNORECASE)
    isValid = pattern.match(timeInput)

    if interaction is None:
        return isValid

    if totalSecondsFromTime(timeInput) < 0:
        await dontBeAnIdiot(interaction=interaction,
                            idiotReason="...",
                            insult="Really?")
        raise RuntimeError("No incorrect time inputs bro.")

    if not isValid:
        await dontBeAnIdiot(interaction=interaction,
                            idiotReason="Bro. Please only log the time in `hours (00:00:00)`, `minutes (00:00)` or `seconds (00)`.",
                            insult="Bro.")
        raise RuntimeError("No incorrect time inputs bro.")
    elif totalSecondsFromTime(timeInput) == 0:
        await dontBeAnIdiot(interaction=interaction,
                            idiotReason="Damn bro, only zero seconds bro? Watch out, you'll go negative next!",
                            insult="Go do a little more bro.")
        raise RuntimeError("No incorrect time inputs bro.")


def totalSecondsFromTime(time):
    # yup this is great code, amazing even
    if time.isdigit() or (time.startswith('-') and time[1:].isdigit()):
        return int(time)

    time_format = "%H:%M:%S" if time.count(':') == 2 else "%H:%M"
    time_object = datetime.strptime(time, time_format)
    total_seconds = (time_object.hour * 3600) + (time_object.minute * 60) + time_object.second
    return total_seconds
