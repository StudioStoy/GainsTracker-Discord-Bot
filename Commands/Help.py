import discord

from BaseCommand import BaseCommand


class HelpCommand(BaseCommand):
    async def execute(self):
        await self.sendMessage(embed)


embed = discord.Embed(title="Help menu", description="A list of possible commands", colour=discord.Colour.green())\
    .set_thumbnail(url="https://cdn.discordapp.com/attachments/1105061248242032661/1105796933664112661/GAINS_app_logo.png")\
    .set_author(name="Website: Studio Stoy", url="https://www.studiostoy.nl")\
    .set_footer(text="Version 0.5")

loginExample = '''login: <username> <password>'''
embed.add_field(name="- **login** \n_Login with your username and password_.",
                value=f'```json\n{loginExample}\n```', inline=False)

workoutDataExample = '''workouts'''
embed.add_field(name="- **workouts** \n_Get a list of all workouts not yet added by the user._",
                value=f'```json\n{workoutDataExample}\n```', inline=False)

logNewWorkoutExample = '''log new workout'''
embed.add_field(name="- **add workout**\n_Select a new workout from the available workouts._",
                value=f'```json\n{logNewWorkoutExample}\n```', inline=False)

logWorkoutExample = '''log workout'''
embed.add_field(name="- **add workout**\n_Log a new measurement for an existing workout_",
                value=f'```json\n{logWorkoutExample}\n```', inline=False)
