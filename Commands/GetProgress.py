import re

import discord
import requests
from discord.ui import View, Button

from BaseCommand import BaseCommand
from Common.Constants import BASE_URL
from Common.Methods import checkStatusCode, getDataFromResponse
from Views.PageUtils import getEmoji, tidyUpString


class GetProgressCommand(BaseCommand):
    def __init__(self):
        self.pages = []
        self.currentPage = 0

    def getView(self, pagePosition):
        buttons = [
            Button(emoji="⏮️", label=' ', style=discord.ButtonStyle.blurple, custom_id='nav_first'),
            Button(emoji="⬅️", label=' ', style=discord.ButtonStyle.blurple, custom_id='nav_back'),
            Button(emoji="➡️", label=' ', style=discord.ButtonStyle.blurple, custom_id='nav_next'),
            Button(emoji="⏭️", label=' ', style=discord.ButtonStyle.blurple, custom_id='nav_last')
        ]
        view = View()

        # set navigation callback to buttons and add them to the view
        for button in buttons:
            if button.custom_id == "nav_first" or button.custom_id == "nav_back":
                button.disabled = pagePosition <= 0
            elif button.custom_id == "nav_last" or button.custom_id == "nav_next":
                button.disabled = pagePosition >= len(self.pages) - 1

            button.callback = self.page_navigation
            view.add_item(button)

        return view

    async def page_navigation(self, interaction: discord.Interaction):
        match interaction.data["custom_id"]:
            case "nav_first":
                self.currentPage = 0
            case "nav_next":
                self.currentPage += 1
            case "nav_back":
                self.currentPage -= 1
            case "nav_last":
                self.currentPage = len(self.pages) - 1

        await interaction.message.edit(embed=self.pages[self.currentPage], view=self.getView(self.currentPage))

        await interaction.response.defer()  # Even if the compiler thinks it doesn't exist, .defer() does.

    async def execute(self):
        response = self.session.get(f"{BASE_URL}/gains/workout")
        if self.responsePositive(response):
            workouts = getDataFromResponse(response)
            categories = []
            if len(workouts) is 0:
                await self.sendMessage("Add some workouts first gainer!")
                return

            for workout in workouts:
                if workout["category"] not in categories:
                    categories.append(workout["category"])

            for category in categories:
                embed = discord.Embed(
                    title=getEmoji(category) + " " + tidyUpString(category),
                    colour=discord.Colour.green()
                )
                self.pages.append(embed)

            for workout in workouts:
                for page in self.pages:
                    if tidyUpString(workout["category"]) in page.title:
                        workoutName = tidyUpString(workout["type"])
                        match tidyUpString(page.title)[2:]:
                            case "reps":
                                pb = "Reps: " + str(workout["personalBest"]["data"]["Reps"])
                                page.add_field(
                                    name=workoutName.capitalize(),
                                    value=f'```{pb}```', inline=True
                                )
                            case "strength":
                                pb = "Weight: " + str(workout["personalBest"]["data"]["Weight"]) + " " + \
                                     str(workout["personalBest"]["data"]["WeightUnit"]) + "\n" + "Reps: " + \
                                     str(workout["personalBest"]["data"]["TotalReps"])
                                page.add_field(
                                    name=workoutName.capitalize(),
                                    value=f'```{pb}```', inline=True
                                )
                            case "time endurance":
                                pb = "Time: " + str(workout["personalBest"]["data"]["Time"]) + " " + \
                                     str(workout["personalBest"]["data"]["TimeUnit"])
                                page.add_field(
                                    name=workoutName.capitalize(),
                                    value=f'```{pb}```', inline=True
                                )
                            case "time and distance endurance":
                                pb = "Time: " + str(workout["personalBest"]["data"]["Time"]) + " " + \
                                     str(workout["personalBest"]["data"]["TimeUnit"]) + "\n" + "Distance: " + \
                                     str(workout["personalBest"]["data"]["Distance"]) + " " + \
                                     str(workout["personalBest"]["data"]["DistanceUnit"])
                                page.add_field(
                                    name=workoutName.capitalize(),
                                    value=f'```{pb}```', inline=True
                                )
            i = 0
            await self.message.channel.send(embed=self.pages[i], view=self.getView(self.currentPage))

        else:
            await checkStatusCode(response, self.message.channel)

        return response
