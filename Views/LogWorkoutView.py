import discord
from discord import SelectOption
from discord.ui import Select
from discord.ui import View


class LogWorkoutView(View):
    def __init__(self, workoutOptions):
        super().__init__()
        self.workoutOptions = workoutOptions
        self.add_item(self.createWorkoutSelect())

    def createWorkoutSelect(self):
        selectOptions = []

        optionCount = 0
        for workout in self.workoutOptions:
            selectOptions.append(SelectOption(label=workout["workoutType"],
                                              value=workout["category"] + "-" + str(optionCount),
                                              emoji=emojiPerCategory[workout["category"]],
                                              default=False))
            optionCount += 1

        select = Select(placeholder="Select a workout", options=selectOptions)

        async def selectCallback(interaction: discord.Interaction):
            await interaction.message.channel.send(f"epic i like the category {select.values[0]} too :sunglasses:")

        select.callback = selectCallback

        return select


emojiPerCategory = {
    "Strength": '🏋️',
    "Reps": '💪',
    "TimeEndurance": '⏱',
    "TimeAndDistanceEndurance": '🚀'
}
