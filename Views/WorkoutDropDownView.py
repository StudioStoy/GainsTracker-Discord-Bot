import json

import discord
from discord import SelectOption
from discord.ui import Select
from discord.ui import View

from Common.Methods import categoryFromType


class WorkoutDropDownView(View):
    def __init__(self, workoutOptions, mutateWorkoutCallback=None):
        super().__init__()
        self.workoutOptions = workoutOptions
        self.mutateSelectedWorkoutCallback = mutateWorkoutCallback
        self.add_item(self.createWorkoutSelect())

    def createWorkoutSelect(self):
        selectOptions = []

        optionCount = 0
        for workout in self.workoutOptions:
            try:
                id = workout["id"]
            except:
                id = ""

            jsonData = {
                "type": workout["type"],
                "id": id
            }

            selectOptions.append(SelectOption(label=workout["type"],
                                              value=json.dumps(jsonData),
                                              emoji=emojiPerCategory[categoryFromType(workout['type'])],
                                              default=False))
            optionCount += 1

        select = Select(placeholder="Select a workout!", options=selectOptions)

        async def dropDownSelectCallback(interaction: discord.Interaction):
            selectionDictionary = json.loads(select.values[0])

            if self.mutateSelectedWorkoutCallback is None:
                await interaction.message.channel.send(
                    f"epic i like the {selectionDictionary['type']} too :sunglasses:")
                await interaction.response.defer()
            else:
                await self.mutateSelectedWorkoutCallback(selectedDict=selectionDictionary, interaction=interaction)

        select.callback = dropDownSelectCallback
        return select


emojiPerCategory = {
    "Strength": '🏋️',
    "Reps": '💪',
    "TimeEndurance": '⏱',
    "TimeAndDistanceEndurance": '🚀'
}
