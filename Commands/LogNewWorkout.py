import asyncio

import discord

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
            await checkStatusCode(workoutsResponse, self.message.channel)
            return

        self.workouts = getDataFromResponse(workoutsResponse)

        logWorkoutView = WorkoutDropDownView(self.workouts, mutateWorkoutCallback=self.createNewWorkoutCallback)
        await self.message.channel.send(view=logWorkoutView)

    async def createNewWorkoutCallback(self, selectedDict, interaction=None):
        response = self.session.post(f"{BASE_URL}/gains/workout", json={"workoutType": selectedDict["type"]})
        selectedDict["id"] = getDataFromResponse(response)

        if self.responsePositive(response):
            epicMessage = await self.sendMessage("Successfully added workout. Let's put the _fit_ around f**ict**!")
            workoutModal = LogWorkoutModal(selectedDict, session=self.session)
            await interaction.response.send_modal(workoutModal)
            await asyncio.sleep(4)
            await epicMessage.edit(content="Successfully added workout. Let's put the _fit_ around f**ict**!\n\n"
                                           "Still doesn't really roll of the tongue that well..")

        else:
            await interaction.response.defer()
            if response.status_code == 409:
                await self.sendMessage("This workout is already added to your account!")
                raise Exception
            else:
                await checkStatusCode(response, self.message.channel)

    # async def workoutSelectCallback(self, selectedDict, interaction: discord.Interaction = None):
    #     workoutModal = LogWorkoutModal(selectedDict)
    #     await interaction.response.send_modal(workoutModal)
