import logging

import discord
from discord.ui import View, Button

from Infrastructure.BaseCommand import BaseCommand
from Common.Constants import GAINS_URL
from Common.Methods import getDataFromResponse, tidyUpString, categoryFromType, getEmojiPerCategory

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(message)s')


class GetPBsCommand(BaseCommand):
    def __init__(self, interaction, share):
        super().__init__(interaction)

        self.pages = []
        self.currentPage = 0
        self.share = share

    def getView(self, pagePosition):
        buttons = [
            Button(emoji="⏮️", label=' ', style=discord.ButtonStyle.green, custom_id='nav_first'),
            Button(emoji="⬅️", label=' ', style=discord.ButtonStyle.green, custom_id='nav_back'),
            Button(emoji="➡️", label=' ', style=discord.ButtonStyle.green, custom_id='nav_next'),
            Button(emoji="⏭️", label=' ', style=discord.ButtonStyle.green, custom_id='nav_last')
        ]
        view = View(timeout=None)

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
        await interaction.response.defer()  # Silly compiler, .defer() does exist.

    async def execute(self):
        session = await self.sessionCenter.get_session()
        response = session.get(url=f"{GAINS_URL}/gains/workout")

        if self.responsePositive(response):
            logger.info("Retrieved user's workouts.")

            workouts = getDataFromResponse(response)
            categories = []

            if len(workouts) == 0:
                await self.replyToCommand(f"Add some workouts first gainer! Use the `/new` command "
                                          "to log your first workout.")
                return

            for workout in workouts:
                if categoryFromType(workout['type']) not in categories:
                    categories.append(categoryFromType(workout['type']))

            for category in categories:
                embed = discord.Embed(
                    title=getEmojiPerCategory(category) + " " + tidyUpString(category),
                    colour=discord.Colour.green()
                )
                self.pages.append(embed)

            inlineCount = 0
            for page in self.pages:
                page: discord.Embed

                for workout in workouts:
                    if workout["personalBest"] is None:
                        continue

                    if tidyUpString(categoryFromType(workout['type'])) in page.title:
                        workoutName = tidyUpString(workout["type"])

                        if inlineCount >= 2:
                            page.add_field(name='', value='', inline=False)
                            inlineCount = 0

                        pb = ""
                        match tidyUpString(page.title)[2:].strip():
                            case "reps":
                                pb = "Reps: " + str(workout["personalBest"]["data"]["Reps"])
                            case "strength":
                                pb = "Weight: " + str(workout["personalBest"]["data"]["Weight"]) + " " + \
                                     str(workout["personalBest"]["data"]["WeightUnit"]) + "\nReps: " + \
                                     str(workout["personalBest"]["data"]["Reps"])
                            case "time endurance":
                                pb = "Time: " + str(workout["personalBest"]["data"]["Time"])
                            case "time and distance endurance":
                                pb = "Time: " + str(workout["personalBest"]["data"]["Time"]) + "\nDistance: " + \
                                     str(workout["personalBest"]["data"]["Distance"]) + " " + \
                                     str(workout["personalBest"]["data"]["DistanceUnit"])
                            case "general":
                                pb = "achievement: " + str(workout["personalBest"]["data"]["GeneralAchievement"])

                        notes = workout['personalBest']['notes']
                        if notes != "":
                            pb += f"\nNotes: {notes}"

                        page.add_field(
                            name=workoutName.capitalize(),
                            value=f'```{pb}```', inline=True
                        )
                        inlineCount += 1
            i = 0

            logger.info("Created pages.")

            await self.replyToCommand(self.pages[i], view=self.getView(self.currentPage), userOnly=not self.share)

        else:
            await self.checkStatusCode(response)

        return response
