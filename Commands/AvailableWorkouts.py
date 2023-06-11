import requests

from BaseCommand import BaseCommand
from Common.Constants import BASE_URL
from Common.Methods import checkStatusCode, getDataFromResponse


class AvailableWorkoutsCommand(BaseCommand):
    async def execute(self) -> requests.Response:
        response = self.session.get(f"{BASE_URL}/catalog/workout/available")

        if self.responsePositive(response):
            workouts = getDataFromResponse(response)
            await self.sendMessage(workouts)
        else:
            await checkStatusCode(response, self.message.channel)

        return response
