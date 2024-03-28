import logging
import discord

from Infrastructure.BaseCommand import BaseCommand
from Common.Constants import GAINS_URL
from Common.Methods import getDataFromResponse
from Views.LogWorkoutModal import LogWorkoutModal
from Views.WorkoutDropDownView import WorkoutDropDownView

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(message)s')


# This command, "/log", is for existing workouts. The command "/new" is for workouts that haven't been added yet.
class LogWorkoutCommand(BaseCommand):
    def __init__(self, interaction, workoutSearchName: str):
        super().__init__(interaction)
        self.workoutSearchName = workoutSearchName

    async def execute(self):
        session = await self.sessionCenter.get_session()
        workoutsResponse = session.get(f"{GAINS_URL}/gains/workout")

        if not self.responsePositive(workoutsResponse):
            await self.checkStatusCode(workoutsResponse)

        workouts = getDataFromResponse(workoutsResponse)
        if len(workouts) <= 0:
            await self.replyToCommand(f"You have no workouts yet! Use the `/new` command to set a new workout.")
            return

        if self.workoutSearchName != "":
            workout = next((item for item in workouts if item['type'].lower() == self.workoutSearchName.lower()), None)

            if workout is None:
                await self.replyToCommand(message="Can't find that workout bro. Please only select the ones displayed!")

            await self.workoutSelectCallback({
                "t": workout["type"],
                "i": workout["id"],
                "c": workout["category"]
            }, self.interaction)
        else:
            logWorkoutView = WorkoutDropDownView(workouts, mutateWorkoutCallback=self.workoutSelectCallback)
            await self.replyToCommand(logWorkoutView)

    async def workoutSelectCallback(self, selectedDict, interaction: discord.Interaction = None):
        session = await self.sessionCenter.get_session()
        workoutModal = LogWorkoutModal(selectedDict, session=session)
        await interaction.response.send_modal(workoutModal)
