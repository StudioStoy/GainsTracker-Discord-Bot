import discord
from discord import app_commands

SS = discord.Object(id=729715726386069644)
BIG_BRAINS = discord.Object(id=776795247815557152)


class GainsTrackerClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # Instead of specifying a guild to every command, we copy over our global commands to one guild instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=SS)
        self.tree.copy_global_to(guild=BIG_BRAINS)
        await self.tree.sync(guild=SS)
        await self.tree.sync(guild=BIG_BRAINS)
