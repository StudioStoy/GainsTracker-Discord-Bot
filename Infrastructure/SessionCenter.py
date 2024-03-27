import logging
import os

import discord
import requests

from Common.Constants import GAINS_URL
from Common.Methods import getDataFromResponse

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(message)s')

sessions = {}  # This list is static for the whole runtime of the app.
userIdAndName = {
    563746765153501202: "stije",
    381080197153292309: "joyo",
    174924013238353921: "bino",
    186892240994566145: "soep",
    689447242842898456: "eef",
    722046797270220880: "jordt",
    388157910238101514: "sanda",
    323484846955692032: "naoh",
    260796157880434708: "dyllo",
    108248158512885760: "arv",
    324907773408182272: "japser"
}


class SessionCenter:
    def __init__(self, interaction: discord.Interaction):
        self.interaction = interaction

    async def get_session(self, userId: int = None) -> requests.Session:
        user_id = self.interaction.user.id if userId is None else userId

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

        if response.status_code != 200 or response.status_code != 204:
            await self.interaction.response.send_message("I was just finishing my set.. Please try again. Bro.", ephemeral=True)
            logger.error(f"Session cannot be created for user {user_id}: {response.status_code}")

        sesh.headers["Authorization"] = getDataFromResponse(response)

        return sesh

    async def login(self, userId: int):
        try:
            loginPayload = {
                "userHandle": userIdAndName[userId],
                "password": os.getenv('EPIC_PASS')
            }

            response = requests.post(f"{GAINS_URL}/auth/login", json=loginPayload)
            if not response.status_code == 204 and not response.status_code == 200:
                await self.interaction.response.send_message("Could not authenticate user.", ephemeral=True)

            return response
        except requests.exceptions.RequestException as e:
            await self.interaction.followup.send("**Darn**, could not connect to the server.", ephemeral=True)
            raise RuntimeError

    async def refreshToken(self, user_id):
        logger.info(f"Trying to refresh token...")

        sessions[user_id] = await self.create_session(user_id)
