import logging
from abc import abstractmethod

import discord
import requests

from Infrastructure.SessionCenter import SessionCenter

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(message)s')


class BaseCommand:
    def __init__(self, interaction: discord.Interaction):
        self.interaction = interaction
        self.sessionCenter = SessionCenter(interaction=interaction)

    # Checks the type(s) of the given argument(s) and uses the corresponding method to send the message to the user.
    # noinspection PyUnresolvedReferences
    async def replyToCommand(self, message=None, staticInteraction=None, view=None, userOnly=True):
        interaction = staticInteraction if staticInteraction is not None else self.interaction

        logger.info("Replying to command.")

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
            logger.warning("[WARNING] Already responded to interaction.")

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
        #       self.checkStatusCode(params) // or something else that raises an exception.
        pass

    async def checkStatusCode(self, response: requests.Response, param=""):
        message = ""
        logger.warning(f"Something went wrong. Status code: {response.status_code}")

        match response.status_code:
            case 400:
                message = "Ai Caramba that's a bad request if I ever saw one."
            case 401:
                logger.info(f"401 response. Might be expired token.")
                await self.sessionCenter.refreshToken(user_id=self.interaction.user.id)
            case 403:
                message = f"User {param} not authorized for this action."
            case 404:
                message = f"{param} not found."
            case 409:
                message = f"Conflict: {param} already exists/was already added."
            case 500:
                message = "Something went wrong, my bad g"
            case _:
                return

        logger.warning(f"[WARNING]: {response.content}")

        if message != "":
            print(f"something went wrong. response: {response.status_code}")
            await self.interaction.channel.send(message)
            raise Exception
