import asyncio

from BaseCommand import BaseCommand
from Common.Constants import BASE_URL
from Common.Methods import checkStatusCode, getDataFromResponse
from Views.WorkoutDropDownView import WorkoutDropDownView


class LogNewWorkoutCommand(BaseCommand):
    async def execute(self):
        workoutsResponse = self.session.get(f"{BASE_URL}/catalog/workout")

        if not self.responsePositive(workoutsResponse):
            await checkStatusCode(workoutsResponse, self.message.channel)
            return

        workouts = getDataFromResponse(workoutsResponse)

        logWorkoutView = WorkoutDropDownView(workouts, isNew=True, workoutSelectCallback=self.workoutSelectCallback)
        await self.message.channel.send(view=logWorkoutView)

    async def workoutSelectCallback(self, selected):
        response = self.session.post(f"{BASE_URL}/gains/workout", json={"workoutType": selected})

        if self.responsePositive(response):
            await self.sendMessage("Successfully added workout. Let's put the _fit_ around f**ict**!")
            await asyncio.sleep(4)
            await self.sendMessage("Still doesn't really roll of the tongue that well..")
        else:
            if response.status_code == 409:
                await self.sendMessage("This workout is already added to your account!")
                raise Exception
            else:
                await checkStatusCode(response, self.message.channel)
