import asyncio

import discord
import requests
from discord.ui import Modal, TextInput

from Common.Constants import BASE_URL
from Common.Methods import checkStatusCode, categoryFromType, tidyUpString
from Views.WorkoutDropDownView import emojiPerCategory


class LogWorkoutModal(Modal):
    def __init__(self, selectedWorkoutData, session: requests.Session = None):
        super().__init__(
            title=f"{emojiPerCategory[categoryFromType(selectedWorkoutData['type'])] + tidyUpString(selectedWorkoutData['type'])}")

        self.timeout = None
        self.session = session
        self.workoutData = selectedWorkoutData
        self.createInputFields(self.workoutData)
        self.on_submit = self.submitDataCallback

    def createInputFields(self, workoutData: dict):
        for textInput in inputsPerCategory[categoryFromType(workoutData['type'])]:
            self.add_item(textInput)

    async def submitDataCallback(self, interaction: discord.Interaction):
        data = {}
        try:
            match categoryFromType(self.workoutData["type"]):
                case "Strength":
                    data = {
                        "Weight": float(tryAndFindInputFromModal(interaction.data, "weightInput")),
                        "WeightUnit": "Kilograms",
                        "Reps": int(tryAndFindInputFromModal(interaction.data, "repsInput"))
                    }
                case "Reps":
                    data = {
                        "Reps": int(tryAndFindInputFromModal(interaction.data, "repsInput"))
                    }
                case "TimeEndurance":
                    data = {
                        "Time": str(tryAndFindInputFromModal(interaction.data, "timeInput"))
                    }
                case "TimeAndDistanceEndurance":
                    data = {
                        "Time": str(tryAndFindInputFromModal(interaction.data, "timeInput")),
                        "Distance": float(tryAndFindInputFromModal(interaction.data, "distanceInput")),
                        "DistanceUnit": "Kilometers"
                    }
        except ValueError:
            await interaction.channel.send(
                "Please make sure you only input numbers or text where applicable, not mixed.")
            await asyncio.sleep(2)
            await interaction.channel.send("You peanut.")

        requestData = {
            "category": categoryFromType(self.workoutData["type"]),
            "data": data
        }

        response = self.session.post(url=f"{BASE_URL}/gains/workout/{self.workoutData['id']}/measurement",
                                     json=requestData)
        if not response.status_code == 204 or not response.status_code == 200:
            await checkStatusCode(response, interaction.channel)

        await interaction.channel.send("GAINZZZZZZZZ (success)")
        await interaction.response.defer()


def tryAndFindInputFromModal(interactionData, inputName):
    for comp in interactionData["components"]:
        textInput = comp["components"][0]
        if textInput["custom_id"] == inputName:
            return textInput["value"]


repsInputs = [
    TextInput(
        custom_id='repsInput',
        label="Amount of reps:",
        placeholder='0',
        max_length=3,
        required=True,
        style=discord.TextStyle.short
    )
]

strengthInputs = [
    TextInput(
        custom_id='weightInput',
        label="Amount of weight in kg:",
        placeholder='0',
        max_length=3,
        required=True,
        style=discord.TextStyle.short
    ),
    TextInput(
        custom_id='repsInput',
        label="Amount of reps:",
        placeholder='0',
        max_length=3,
        required=True,
        style=discord.TextStyle.short
    )
]

timeEnduranceInputs = [
    TextInput(
        custom_id='timeInput',
        label="Time:",
        placeholder='00:00:00',
        max_length=8,
        required=True,
        style=discord.TextStyle.short
    )
]

timeAndDistanceEnduranceInputs = [
    TextInput(
        custom_id='timeInput',
        label="Time:",
        placeholder='00:00:00',
        max_length=8,
        required=True,
        style=discord.TextStyle.short
    ),
    TextInput(
        custom_id='distanceInput',
        label="Distance in km:",
        placeholder='0',
        max_length=6,
        required=True,
        style=discord.TextStyle.short
    )
]

inputsPerCategory = {
    "Reps": repsInputs,
    "Strength": strengthInputs,
    "TimeAndDistanceEndurance": timeAndDistanceEnduranceInputs,
    "TimeEndurance": timeEnduranceInputs
}
