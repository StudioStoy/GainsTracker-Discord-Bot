import json

import discord

from BaseCommand import BaseCommand
from Common.Constants import BASE_URL
from Common.Methods import checkStatusCode, getDataFromResponse


class AvailableMeasurementsCommand(BaseCommand):
    async def execute(self):
        response = self.session.get(f"{BASE_URL}/catalog/measurement")
        if self.responsePositive(response):
            measurements = getDataFromResponse(response)

            embed = discord.Embed(title="Available Measurements",
                                  description="A list of measurement data you can use to add to workouts.",
                                  colour=discord.Colour.green())

            inlineCount = 0
            for measurementType, measurementData in measurements.items():
                if inlineCount >= 2:
                    embed.add_field(name='\u200b', value='\u200b', inline=False)
                    inlineCount = 0

                embed.add_field(name=f"**{measurementType}**",
                                value=f'```json\n{json.dumps(measurementData, indent=4)}\n```', inline=True)
                inlineCount += 1

            await self.sendMessage(embed)
        else:
            await checkStatusCode(response, self.message.channel)
