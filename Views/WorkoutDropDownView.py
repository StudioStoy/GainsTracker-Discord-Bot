import json
import logging

import discord
from discord import SelectOption
from discord.ui import Select
from discord.ui import View

from Common.Methods import categoryFromType, tidyUpString, getEmojiPerCategory

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(message)s')


class WorkoutDropDownView(View):
    def __init__(self, workoutOptions, mutateWorkoutCallback=None):
        super().__init__(timeout=None)
        self.workoutOptions = workoutOptions
        self.mutateSelectedWorkoutCallback = mutateWorkoutCallback
        self.add_item(self.createWorkoutSelect())

    def createWorkoutSelect(self):
        selectOptions = []

        logger.info(f"Options amount: {len(self.workoutOptions)}")
        optionCount = 0
        for workout in self.workoutOptions:
            # Because of Discord limitation, only 25 options can show in the select view.
            # So here I filter out less important ones.
            if workout["type"] in ["DeadLift", "DiamondPushUp", "JumpingRope", "ChestPress", "DumbbellPress"]:
                continue

            try:
                workoutId = workout["id"]
            except KeyError:
                workoutId = ""

            jsonData = {
                "type": workout["type"],
                "id": workoutId
            }

            selectOptions.append(SelectOption(label=tidyUpString(workout["type"]),
                                              value=json.dumps(jsonData),
                                              emoji=getEmojiPerCategory(categoryFromType(workout['type'])),
                                              default=False))
            optionCount += 1

        select = Select(placeholder="Select a workout!", options=selectOptions)

        async def dropDownSelectCallback(interaction: discord.Interaction):
            selectionDictionary = json.loads(select.values[0])

            if self.mutateSelectedWorkoutCallback is None:
                await interaction.message.channel.send(f"epic i like {selectionDictionary['type']} too :sunglasses:")
                await interaction.response.defer()
            else:
                await self.mutateSelectedWorkoutCallback(selectedDict=selectionDictionary, interaction=interaction)

        logger.info("Selection created.")

        select.callback = dropDownSelectCallback
        return select
