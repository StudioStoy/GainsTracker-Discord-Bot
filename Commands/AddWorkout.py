import asyncio
import json

import requests

from BaseCommand import BaseCommand
from Common.Constants import BASE_URL
from Common.Methods import checkStatusCode


class AddWorkoutCommand(BaseCommand):
    def __init__(self, workoutType: str):
        self.workoutType = workoutType

    async def execute(self) -> requests.Response:
        addWorkoutPayload = {"workoutType": self.workoutType}

        response = self.session.post(f"{BASE_URL}/gains/workout", json=addWorkoutPayload)

        if self.responsePositive(response):
            await self.sendMessage("Successfully added workout. Let's put the _fit_ around f**ict**!")
            await asyncio.sleep(4)
            await self.sendMessage("Still doesn't really roll of the tongue that well..")
        else:
            if response.status_code == 409:
                await self.sendMessage("This workout is already added to your account!")
                raise Exception
            else:
                await checkStatusCode(response, self.message.channel, self.workoutType)

        return response
