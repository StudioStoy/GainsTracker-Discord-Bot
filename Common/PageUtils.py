import discord
from discord import Embed
from Common.Constants import GAINS_VERSION


def createBasicPage(title="Gainer time") -> discord.Embed:
    page = Embed(title=title, description="", color=0xffae00)
    page.set_author(name="CocMaster64")
    page.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/1105061248242032661/1105796933664112661/GAINS_app_logo.png"
    )
    page.set_author(name="Studio Stoy", url="https://www.gainstracker.studiostoy.nl")
    page.set_footer(text=f"version {GAINS_VERSION}")

    return page
