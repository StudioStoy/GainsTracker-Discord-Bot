import asyncio

import requests

from BaseCommand import BaseCommand
from Common.Constants import BASE_URL
from Common.Methods import checkStatusCode


class LoginCommand(BaseCommand):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    async def execute(self) -> requests.Response:
        loginPayload = {
            "userHandle": self.username,
            "password": self.password
        }

        response = self.session.post(f"{BASE_URL}/auth/login", json=loginPayload)

        if self.responsePositive(response):
            await self.sendMessage(f"Successfully authenticated user {self.username}.")
            await asyncio.sleep(2)
            await self.sendMessage(f"**Let the gains begin!**")
        else:
            await checkStatusCode(response, self.message.channel, self.username)

        return response
