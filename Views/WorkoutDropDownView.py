import discord
from discord import SelectOption
from discord.ui import Select
from discord.ui import View


class WorkoutDropDownView(View):
    def __init__(self, workoutOptions, isNew=False, workoutSelectCallback=None):
        super().__init__()
        self.workoutOptions = workoutOptions
        self.workoutSelectCallback = workoutSelectCallback
        self.add_item(self.createWorkoutSelect(isNew))

    def createWorkoutSelect(self, isNew):
        selectOptions = []

        optionCount = 0
        for workout in self.workoutOptions:
            typeValue = workout["type"] if isNew else workout["category"]

            selectOptions.append(SelectOption(label=workout["type"],
                                              value=str(typeValue) + "-" + str(optionCount),
                                              emoji=emojiPerCategory[workout["category"]],
                                              default=False))
            optionCount += 1

        select = Select(placeholder="Select a workout", options=selectOptions)

        async def workoutSelectCallback(interaction: discord.Interaction):
            value = select.values[0].split("-")[0]
            await interaction.response.defer()

            if self.workoutSelectCallback is None:
                await interaction.message.channel.send(f"epic i like the {value} too :sunglasses:")
            else:
                await self.workoutSelectCallback(selected=value)

        select.callback = workoutSelectCallback
        return select


emojiPerCategory = {
    "Strength": '🏋️',
    "Reps": '💪',
    "TimeEndurance": '⏱',
    "TimeAndDistanceEndurance": '🚀'
}
