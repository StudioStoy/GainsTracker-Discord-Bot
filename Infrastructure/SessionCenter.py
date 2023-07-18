import os

import discord
import requests

from Common.Constants import BASE_URL
from Common.Methods import getDataFromResponse

sessions = {}  # This list is static for the whole runtime of the app.
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


class SessionCenter:
    def __init__(self, interaction: discord.Interaction):
        self.interaction = interaction

    async def get_session(self, userId: int = None, refresh=False) -> requests.Session:
        user_id = self.interaction.user.id if userId is None else userId

        if refresh:
            sessions[user_id] = await self.create_session(user_id)

        if user_id not in sessions:
            sessions[user_id] = await self.create_session(user_id)

        return sessions[user_id]

    async def create_session(self, user_id):
        # NOTE: I hate the word sesh
        sesh = requests.session()
        sesh.headers = {
            'Content-type': 'application/json',
            "accept": "application/json",
        }

        response = await self.login(user_id)
        sesh.headers["Authorization"] = getDataFromResponse(response)

        return sesh

    async def login(self, userId: int):
        try:
            loginPayload = {
                "userHandle": userIdAndName[userId],
                "password": os.getenv('EPIC_PASS')
            }

            response = requests.post(f"{BASE_URL}/auth/login", json=loginPayload)
            if not response.status_code == 204 and not response.status_code == 200:
                await self.interaction.channel.send("Could not authenticate user.")

            return response
        except requests.exceptions.RequestException as e:
            await self.interaction.followup.send("**Darn**, could not connect to the server.", ephemeral=True)
            raise RuntimeError
