import discord

from BaseCommand import BaseCommand
from Common.Constants import BASE_URL
from Common.Methods import getDataFromResponse, checkStatusCode
from Views.LogWorkoutModal import LogWorkoutModal
from Views.WorkoutDropDownView import WorkoutDropDownView


# This command, "/log", is for existing workouts. The command "/new" is for workouts that haven't been added yet.
class LogWorkoutCommand(BaseCommand):
    async def execute(self):
        workoutsResponse = self.session.get(f"{BASE_URL}/gains/workout")

        if not self.responsePositive(workoutsResponse):
            await checkStatusCode(workoutsResponse, self.message.channel)

        workouts = getDataFromResponse(workoutsResponse)
        if len(workouts) <= 0:
            await self.replyToCommand(f"You have no workouts yet! Use the `/new` command to set a new workout.")
            return

        logWorkoutView = WorkoutDropDownView(workouts, mutateWorkoutCallback=self.workoutSelectCallback)
        await self.replyToCommand(logWorkoutView)

    async def workoutSelectCallback(self, selectedDict, interaction: discord.Interaction = None):
        workoutModal = LogWorkoutModal(selectedDict, session=self.session)
        await interaction.response.send_modal(workoutModal)
