from abc import abstractmethod
from logging import Logger

import discord
import requests

from Infrastructure.Login import login
from Common.Methods import getDataFromResponse
from Infrastructure.SessionStuff import sessions


class BaseCommand:
    def __init__(self, interaction: discord.Interaction, logger: Logger):
        self.logger = logger
        self.interaction = interaction

    async def get_session(self, userId: int = None) -> requests.Session:
        user_id = self.interaction.user.id if userId is None else userId

        if user_id not in sessions:
            sessions[user_id] = await self.create_session(user_id)

        #     sessions[user_id] = {
        #         "token": await self.create_session(user_id, self.interaction),
        #         "startTime": datetime.now().strftime('%H:%M:%S')
        #     }
        #
        # if sessions[user_id]["startTime"] < (datetime.now() + timedelta(hours=9)).strftime('%H:%M:%S'):
        #     sessions[user_id] = {
        #         "token": await self.create_session(user_id, self.interaction),
        #         "startTime": datetime.now().strftime('%H:%M:%S')
        #     }

        return sessions[user_id]

    async def create_session(self, user_id):
        # NOTE: I hate the word sesh
        sesh = requests.session()
        sesh.headers = {
            'Content-type': 'application/json',
            "accept": "application/json",
        }

        response = await login(user_id, self.interaction)
        sesh.headers["Authorization"] = getDataFromResponse(response)

        return sesh

    async def sendMessage(self, message, view=None):
        if type(message) == discord.Embed:
            if view is not None:
                return await message.channel.send(embed=message, view=view)
            return await message.channel.send(embed=message)
        if view is not None:
            return await message.channel.send(message, view=view)
        return await message.channel.send(message)

    # Checks the type(s) of the given argument(s) and uses the corresponding method to send the message to the user.
    # noinspection PyUnresolvedReferences
    async def replyToCommand(self, message=None, staticInteraction=None, view=None, userOnly=True):
        interaction = staticInteraction if staticInteraction is not None else self.interaction

        try:
            if isinstance(message, discord.ui.Modal):
                return await interaction.response.send_modal(message)

            if type(message) == discord.Embed:
                if view is not None:
                    return await interaction.response.send_message(embed=message, view=view, ephemeral=userOnly)
                return await interaction.response.send_message(embed=message, ephemeral=userOnly)

            if isinstance(message, discord.ui.View):
                return await interaction.response.send_message(view=message, ephemeral=userOnly)

            if message is not None and view is not None:
                return await interaction.response.send_message(message, view=view, ephemeral=userOnly)

            return await interaction.response.send_message(message, ephemeral=userOnly)
        except discord.errors.InteractionResponded:
            self.logger.warning("[WARNING] Already responded to interaction.")

    @staticmethod
    def responsePositive(response):
        return response.status_code == 200 or response.status_code == 204

    @abstractmethod
    async def execute(self):
        # Implement this function like the one in the LoginCommand. Like so:
        #   response = session.action
        #   if self.responsePositive(response):
        #       success logic
        #   else:
        #       checkStatusCode(params) // or something else that raises an exception.
        pass
