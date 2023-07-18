import logging

from Infrastructure.BaseCommand import BaseCommand
from Common.Constants import BASE_URL
from Common.Methods import getDataFromResponse
from Views.WorkoutDropDownView import WorkoutDropDownView

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(message)s')


class GetProgressCommand(BaseCommand):

    def __init__(self, interaction):
        super().__init__(interaction)
        self.workouts = []

    async def execute(self):
        session = await self.sessionCenter.get_session()
        workoutsResponse = session.get(f"{BASE_URL}/catalog/workout")

        if not self.responsePositive(workoutsResponse):
            await self.checkStatusCode(workoutsResponse)
            return

        self.workouts = getDataFromResponse(workoutsResponse)
        logWorkoutView = WorkoutDropDownView(self.workouts, mutateWorkoutCallback=self.createNewWorkoutCallback)
        await self.replyToCommand(logWorkoutView)
        # await interaction

    async def createNewWorkoutCallback(self, selectedDict, interaction=None):
        await interaction.response.defer()
        await self.replyToCommand("ello :D")
