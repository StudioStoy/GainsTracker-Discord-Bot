import discord

from Infrastructure.BaseCommand import BaseCommand
from Common.Constants import BASE_URL
from Common.Methods import getDataFromResponse, checkStatusCode
from Views.LogWorkoutModal import LogWorkoutModal
from Views.WorkoutDropDownView import WorkoutDropDownView


# This command, "/log", is for existing workouts. The command "/new" is for workouts that haven't been added yet.
class LogWorkoutCommand(BaseCommand):
    async def execute(self):
        session = await self.get_session()
        workoutsResponse = session.get(f"{BASE_URL}/gains/workout")

        if not self.responsePositive(workoutsResponse):
            await checkStatusCode(workoutsResponse, self.interaction.channel)

        workouts = getDataFromResponse(workoutsResponse)
        if len(workouts) <= 0:
            await self.replyToCommand(f"You have no workouts yet! Use the `/new` command to set a new workout.")
            return

        logWorkoutView = WorkoutDropDownView(workouts, mutateWorkoutCallback=self.workoutSelectCallback)
        await self.replyToCommand(logWorkoutView)

    async def workoutSelectCallback(self, selectedDict, interaction: discord.Interaction = None):
        session = await self.get_session()
        workoutModal = LogWorkoutModal(selectedDict, session=session)
        await interaction.response.send_modal(workoutModal)
