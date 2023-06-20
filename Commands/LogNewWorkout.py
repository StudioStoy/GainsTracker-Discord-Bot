from BaseCommand import BaseCommand
from Common.Constants import BASE_URL
from Common.Methods import checkStatusCode, getDataFromResponse
from Views.LogWorkoutModal import LogWorkoutModal
from Views.WorkoutDropDownView import WorkoutDropDownView


class LogNewWorkoutCommand(BaseCommand):
    def __init__(self):
        self.workouts = []

    async def execute(self):
        workoutsResponse = self.session.get(f"{BASE_URL}/catalog/workout")

        if not self.responsePositive(workoutsResponse):
            await checkStatusCode(workoutsResponse, self.interaction.channel)
            return

        self.workouts = getDataFromResponse(workoutsResponse)
        if len(self.workouts) <= 0:
            await self.replyToCommand("You have added ALL workouts! Are you making sure you have correct form??")

        logWorkoutView = WorkoutDropDownView(self.workouts, mutateWorkoutCallback=self.createNewWorkoutCallback)
        await self.replyToCommand(logWorkoutView)

    async def createNewWorkoutCallback(self, selectedDict, interaction=None):
        response = self.session.post(f"{BASE_URL}/gains/workout", json={"workoutType": selectedDict["type"]})
        selectedDict["id"] = getDataFromResponse(response)

        if self.responsePositive(response):
            workoutModal = LogWorkoutModal(selectedDict, session=self.session)
            await self.replyToCommand(workoutModal, staticInteraction=interaction)

            await self.replyToCommand("Successfully added workout. Let's put the _fit_ around f**ict**!",
                                      staticInteraction=interaction)
        else:
            if response.status_code == 409:
                await self.replyToCommand("This workout is already added to your account!",
                                          staticInteraction=interaction)
                raise RuntimeError
            else:
                await checkStatusCode(response, self.interaction.channel)
