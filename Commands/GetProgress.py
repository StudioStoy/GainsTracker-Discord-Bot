from BaseCommand import BaseCommand
from Common.Constants import BASE_URL
from Common.Methods import checkStatusCode, getDataFromResponse
from Views.WorkoutDropDownView import WorkoutDropDownView


class GetProgressCommand(BaseCommand):

    def __init__(self):
        self.workouts = []

    async def execute(self):
        workoutsResponse = self.session.get(f"{BASE_URL}/catalog/workout")

        if not self.responsePositive(workoutsResponse):
            await checkStatusCode(workoutsResponse, self.message.channel)
            return

        self.workouts = getDataFromResponse(workoutsResponse)
        logWorkoutView = WorkoutDropDownView(self.workouts, mutateWorkoutCallback=self.createNewWorkoutCallback)
        await self.message.channel.send(view=logWorkoutView)
        # await interaction

    async def createNewWorkoutCallback(self, selectedDict, interaction=None):
        await interaction.response.defer()
        await self.sendMessage("ello :D")
