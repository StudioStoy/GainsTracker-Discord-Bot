import discord
from discord import app_commands


class GainsTrackerClient(discord.Client):
    def __init__(self, *, intents: discord.Intents, guild_ids: list[str]):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.guild_ids = guild_ids

    async def setup_hook(self):
        # This copies the global commands over to the guilds set in the environment property GUILDS.
        for guild_id in self.guild_ids:
            self.tree.copy_global_to(guild=discord.Object(id=guild_id))
            await self.tree.sync(guild=discord.Object(guild_id))
