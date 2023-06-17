import discord

from BaseCommand import BaseCommand
from Common.Constants import GAINS_VERSION


class HelpCommand(BaseCommand):
    async def execute(self):
        await self.sendMessage(embed)


embed = discord.Embed(title="Help menu", description="A list of possible commands", colour=discord.Colour.green()) \
    .set_thumbnail(
    url="https://cdn.discordapp.com/attachments/1105061248242032661/1105796933664112661/GAINS_app_logo.png") \
    .set_author(name="Website: Studio Stoy", url="https://www.studiostoy.nl") \
    .set_footer(text=f"Version {GAINS_VERSION}")

logNewWorkoutExample = '''new workout'''
embed.add_field(name="- **Add new workout**\n_Select a new workout from the available workouts._",
                value=f'```json\n{logNewWorkoutExample}\n```', inline=False)

logWorkoutExample = '''log'''
embed.add_field(name="- **Log data to workout**\n_Log a new measurement for an existing workout_",
                value=f'```json\n{logWorkoutExample}\n```', inline=False)

pbExample = '''pbs'''
embed.add_field(name="- **Personal Bests** \n_Get a list of all workouts per category with your PBs._",
                value=f'```json\n{pbExample}\n```', inline=False)
