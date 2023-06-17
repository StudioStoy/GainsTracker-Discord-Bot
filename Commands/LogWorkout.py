import discord

from BaseCommand import BaseCommand
from Common.Constants import BASE_URL, GAINS_BOT
from Common.Methods import getDataFromResponse, checkStatusCode
from Views.LogWorkoutModal import LogWorkoutModal
from Views.WorkoutDropDownView import WorkoutDropDownView


# This command, "log" is for existing workouts. "new workout" is for workouts that haven't been added yet.
class LogWorkoutCommand(BaseCommand):
    async def execute(self):
        workoutsResponse = self.session.get(f"{BASE_URL}/gains/workout")

        if not self.responsePositive(workoutsResponse):
            await checkStatusCode(workoutsResponse, self.message.channel)

        workouts = getDataFromResponse(workoutsResponse)
        if len(workouts) <= 0:
            await self.sendMessage(f"You have no workouts yet! Use {GAINS_BOT} `new workout` to set a new workout.")
            return

        logWorkoutView = WorkoutDropDownView(workouts, mutateWorkoutCallback=self.workoutSelectCallback)
        await self.message.channel.send(view=logWorkoutView)

    async def workoutSelectCallback(self, selectedDict, interaction: discord.Interaction = None):
        workoutModal = LogWorkoutModal(selectedDict, session=self.session)
        await interaction.response.send_modal(workoutModal)
