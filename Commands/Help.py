import discord

from Infrastructure.BaseCommand import BaseCommand
from Common.Constants import GAINS_VERSION


class HelpCommand(BaseCommand):
    async def execute(self):
        await self.replyToCommand(embed, userOnly=False)


embed = discord.Embed(title="Help menu", description="An explanation of the commands", colour=discord.Colour.green()) \
    .set_thumbnail(
    url="https://cdn.discordapp.com/attachments/1105061248242032661/1105796933664112661/GAINS_app_logo.png") \
    .set_author(name="Website: Studio Stoy", url="https://www.studiostoy.nl") \
    .set_footer(text=f"Version 🏃{GAINS_VERSION}🏃")

logNewWorkoutExample = '''/new {optional: search for more workouts}'''
embed.add_field(name="**🏋️Add new workout🏋️**\n| __Select a new workout from the available workouts__ |\n💡_Tip! Use the optional field to search for one._",
                value=f'```json\n{logNewWorkoutExample}\n```', inline=False)

logWorkoutExample = '''/log {optional: search for more workouts}'''
embed.add_field(name="**📈Log data to workout📈**\n| __Log a new measurement for an existing workout__ |\n💡_Tip! Use the optional field to search for one._",
                value=f'```json\n{logWorkoutExample}\n```', inline=False)

pbExample = '''/pbs'''
embed.add_field(name="**🏅Personal Bests🏅** \n| __Get a list of all workouts per category with your PBs.__ |",
                value=f'```json\n{pbExample}\n```', inline=False)
