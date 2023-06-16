import discord
from discord import SelectOption
from discord.ui import Select
from discord.ui import View


class WorkoutDropDownView(View):
    def __init__(self, workoutOptions, workoutSelectCallback=None):
        super().__init__()
        self.workoutOptions = workoutOptions
        self.workoutSelectCallback = workoutSelectCallback
        self.add_item(self.createWorkoutSelect())

    def createWorkoutSelect(self):
        selectOptions = []

        optionCount = 0
        for workout in self.workoutOptions:
            selectOptions.append(SelectOption(label=workout["type"],
                                              value=workout["category"] + "-" + str(optionCount),
                                              emoji=emojiPerCategory[workout["category"]],
                                              default=False))
            optionCount += 1

        select = Select(placeholder="Select a workout", options=selectOptions)

        async def workoutSelectCallback(interaction: discord.Interaction):
            if self.workoutSelectCallback is None:
                await interaction.message.channel.send(f"epic i like the category {select.values[0]} too :sunglasses:")
            else:
                await self.workoutSelectCallback(select.values[0])
            await interaction.response.defer()

        select.callback = workoutSelectCallback
        return select


emojiPerCategory = {
    "Strength": '🏋️',
    "Reps": '💪',
    "TimeEndurance": '⏱',
    "TimeAndDistanceEndurance": '🚀'
}
