import discord
from discord.ui import Modal, TextInput


class LogWorkoutModal(Modal):
    def __init__(self, selectedWorkoutData):
        super().__init__(title=f"{selectedWorkoutData['emoji'] + selectedWorkoutData['type']}")
        self.createInputFields(selectedWorkoutData)

    def createInputFields(self, workoutData: dict):
        for textInput in inputsPerCategory[workoutData['category']]:
            self.add_item(textInput)


repsInputs = [
    TextInput(
            label="Amount of reps:",
            placeholder='0',
            max_length=3,
            required=True,
            style=discord.TextStyle.short
    )
]

strengthInputs = [
    TextInput(
        label="Amount of weight:",
        placeholder='0',
        max_length=3,
        required=True,
        style=discord.TextStyle.short
    ),
    TextInput(
        label="Weight unit:",
        placeholder='kilograms/grams',
        max_length=9,
        required=True,
        style=discord.TextStyle.short
    ),
    TextInput(
        label="Amount of reps:",
        placeholder='0',
        max_length=3,
        required=True,
        style=discord.TextStyle.short
    )
]

timeEnduranceInputs = [
    TextInput(
            label="Time:",
            placeholder='00:00:00',
            max_length=8,
            required=True,
            style=discord.TextStyle.short
    )
]

timeAndDistanceEnduranceInputs = [
    TextInput(
            label="Time:",
            placeholder='00:00:00',
            max_length=8,
            required=True,
            style=discord.TextStyle.short
    ),
    TextInput(
        label="Distance:",
        placeholder='0',
        max_length=6,
        required=True,
        style=discord.TextStyle.short
    ),
    TextInput(
        label="Distance unit:",
        placeholder='kilometers/meters',
        max_length=10,
        required=True,
        style=discord.TextStyle.short
    )
]

inputsPerCategory = {
    "Reps": repsInputs,
    "Strength": strengthInputs,
    "TimeAndDistanceEndurance": timeEnduranceInputs,
    "DistanceEndurance": timeAndDistanceEnduranceInputs
}
