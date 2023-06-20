from abc import abstractmethod
from logging import Logger

import discord
import requests

from Commands.Login import LoginCommand
from Common.Methods import getDataFromResponse


# noinspection PyUnresolvedReferences
class BaseCommand:
    message: discord.Message = None
    session: requests.Session = requests.session()
    interaction: discord.Interaction = None
    logger: Logger
    userTokensInSession = {}

    @classmethod
    def setSession(cls, session):
        cls.session = session

    @classmethod
    def setLogger(cls, logger):
        cls.logger = logger

    @classmethod
    async def initialize(cls, interaction):
        cls.interaction = interaction

        userId = cls.interaction.user.id

        if userId not in cls.userTokensInSession:
            login = LoginCommand(userId, interaction, session=cls.session)
            response = await login.execute()
            cls.userTokensInSession[userId] = getDataFromResponse(response)

        if cls.userTokensInSession.__contains__(userId):
            cls.session.headers["Authorization"] = cls.userTokensInSession[userId]

    @classmethod
    def setMessage(cls, messageInstance):
        cls.message = messageInstance

    async def sendMessage(self, message, view=None):
        if type(message) == discord.Embed:
            if view is not None:
                return await self.message.channel.send(embed=message, view=view)
            return await self.message.channel.send(embed=message)
        if view is not None:
            return await self.message.channel.send(message, view=view)
        return await self.message.channel.send(message)

    # Checks the type(s) of the given argument(s) and uses the corresponding method to send the message to the user.
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
        #       succes logic
        #   else:
        #       checkStatusCode(params) // or something else that raises an exception.
        pass
