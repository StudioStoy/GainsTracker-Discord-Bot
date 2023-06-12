import discord

from BaseCommand import BaseCommand


class HelpCommand(BaseCommand):
    async def execute(self):
        await self.sendMessage(embed, isEmbed=True)


embed = discord.Embed(title="Help menu", description="A list of possible commands", colour=discord.Colour.green())\
    .set_thumbnail(url="https://cdn.discordapp.com/attachments/1105061248242032661/1105796933664112661/GAINS_app_logo.png")\
    .set_author(name="Website: Studio Stoy", url="https://www.studiostoy.nl")\
    .set_footer(text="Version 0.3")

loginExample = '''
login: {
    "username": "yourName", 
    "password": "yourPassword"
}'''
embed.add_field(name="- **login** \n_Login with your username and password_.",
                value=f'```json\n{loginExample}\n```', inline=False)

workoutDataExample = '''workouts'''
embed.add_field(name="- **workouts** \n_Get a list of all workouts not yet added by the user._",
                value=f'```json\n{workoutDataExample}\n```', inline=False)

addWorkoutExample = '''add workout: workoutType'''
embed.add_field(name="- **add workout**\n_Add a workout from the available workouts with its workout type name_",
                value=f'```json\n{addWorkoutExample}\n```', inline=False)

measurementDataExample = '''measurements'''
embed.add_field(name="- **measurements** \n_Get a list of all measurement data to add to the corresponding workout._",
                value=f'```json\n{measurementDataExample}\n```', inline=False)
