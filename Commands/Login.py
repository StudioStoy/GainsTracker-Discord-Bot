import os

import requests

from BaseCommand import BaseCommand
from Common.Constants import BASE_URL
from Common.Methods import checkStatusCode


class LoginCommand(BaseCommand):
    def __init__(self, userId: str):
        self.userId = userId

    async def execute(self) -> requests.Response:
        loginPayload = {
            "userHandle": userIdAndName[str(self.userId)],
            "password": os.getenv('EPIC_PASS')
        }

        response = self.session.post(f"{BASE_URL}/auth/login", json=loginPayload)

        if not self.responsePositive(response):
            await checkStatusCode(response, self.message.channel, userIdAndName[self.userId])

        return response


userIdAndName = {
    "563746765153501202": "stije",
    "381080197153292309": "joyo",
    "174924013238353921": "bino",
    "186892240994566145": "soep",
    "689447242842898456": "eef",
    "722046797270220880": "jordt",
    "388157910238101514": "sanda",
    "323484846955692032": "naoh"
}
