import discord

from Infrastructure.BaseCommand import BaseCommand
from Common.Constants import BASE_URL
from Common.Methods import checkStatusCode, getDataFromResponse
from Views.LogWorkoutModal import LogWorkoutModal
from Views.WorkoutDropDownView import WorkoutDropDownView


class LogNewWorkoutCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.workouts = []

    async def execute(self):
        session = await self.get_session()
        workoutsResponse = session.get(f"{BASE_URL}/catalog/workout")

        if not self.responsePositive(workoutsResponse):
            await checkStatusCode(workoutsResponse, self.interaction)
            return

        self.workouts = getDataFromResponse(workoutsResponse)
        if len(self.workouts) <= 0:
            await self.replyToCommand("You have added ALL workouts! Are you making sure you have correct form??")

        logWorkoutView = WorkoutDropDownView(self.workouts, mutateWorkoutCallback=self.createNewWorkoutCallback)
        await self.replyToCommand(logWorkoutView)

    async def createNewWorkoutCallback(self, selectedDict, interaction: discord.Interaction = None):
        session = await self.get_session(interaction)

        response = session.post(f"{BASE_URL}/gains/workout", json={"workoutType": selectedDict["type"]})
        selectedDict["id"] = getDataFromResponse(response)

        if self.responsePositive(response):
            workoutModal = LogWorkoutModal(selectedDict, session=session)
            await self.replyToCommand(workoutModal, staticInteraction=interaction)

            await self.replyToCommand("Successfully added workout. Let's put the _fit_ around f**ict**!",
                                      staticInteraction=interaction)
        else:
            if response.status_code == 409:
                await self.replyToCommand("This workout is already added to your account!",
                                          staticInteraction=interaction)
                raise RuntimeError
            else:
                await checkStatusCode(response, self.interaction)
