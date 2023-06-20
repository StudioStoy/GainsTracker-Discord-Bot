import os

import discord
import requests

from Common.Constants import BASE_URL
from Common.Methods import checkStatusCode


class LoginCommand:
    def __init__(self, userId: int, interaction: discord.Interaction, session: requests.Session):
        self.userId = userId
        self.interaction = interaction
        self.session = session

    async def execute(self) -> requests.Response:
        loginPayload = {
            "userHandle": userIdAndName[self.userId],
            "password": os.getenv('EPIC_PASS')
        }

        try:
            response = self.session.post(f"{BASE_URL}/auth/login", json=loginPayload)
            if not response.status_code == 204 and not response.status_code == 200:
                await checkStatusCode(response, self.interaction.channel, userIdAndName[self.userId])

            return response

        except requests.exceptions.RequestException as e:
            await self.interaction.followup.send("**Darn**, could not connect to the server.", ephemeral=True)
            raise RuntimeError


userIdAndName = {
    563746765153501202: "stije",
    381080197153292309: "joyo",
    174924013238353921: "bino",
    186892240994566145: "soep",
    689447242842898456: "eef",
    722046797270220880: "jordt",
    388157910238101514: "sanda",
    323484846955692032: "naoh"
}
