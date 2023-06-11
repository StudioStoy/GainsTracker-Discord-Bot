from abc import abstractmethod

import requests


class BaseCommand:
    message = None
    session = requests.session()

    @classmethod
    def setSession(cls, session):
        cls.session = session

    @classmethod
    def setMessage(cls, messageInstance):
        cls.message = messageInstance

    async def sendMessage(self, message, isEmbed=False):
        if isEmbed:
            await self.message.channel.send(embed=message)
        else:
            await self.message.channel.send(message)

    @staticmethod
    def responsePositive(response):
        return response.status_code == 200 or response.status_code == 204

    @abstractmethod
    async def execute(self) -> requests.Response:
        # Implement this function like the one in the LoginCommand. Like so:
        #   response = session.action
        #   if self.responsePositive(response):
        #       succes logic
        #   else:
        #       checkStatusCode(params) // or something else that raises an exception.
        pass
