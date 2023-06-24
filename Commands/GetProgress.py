from Infrastructure.BaseCommand import BaseCommand
from Common.Constants import BASE_URL
from Common.Methods import checkStatusCode, getDataFromResponse
from Views.WorkoutDropDownView import WorkoutDropDownView


class GetProgressCommand(BaseCommand):

    def __init__(self, interaction, logger):
        super().__init__(interaction, logger)
        self.workouts = []

    async def execute(self):
        session = await self.get_session()
        workoutsResponse = session.get(f"{BASE_URL}/catalog/workout")

        if not self.responsePositive(workoutsResponse):
            await checkStatusCode(workoutsResponse, interaction=self.interaction)
            return

        self.workouts = getDataFromResponse(workoutsResponse)
        logWorkoutView = WorkoutDropDownView(self.workouts, mutateWorkoutCallback=self.createNewWorkoutCallback)
        await self.replyToCommand(logWorkoutView)
        # await interaction

    async def createNewWorkoutCallback(self, selectedDict, interaction=None):
        await interaction.response.defer()
        await self.replyToCommand("ello :D")
