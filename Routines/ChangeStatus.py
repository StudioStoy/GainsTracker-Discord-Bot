import asyncio
import random

import discord


async def changeStatus(client):
    while True:
        gymBroQuote = discord.Activity(
            type=discord.ActivityType.custom,
            name="Custom Status",  # Does nothing, but is required.
            state=gymBroQuotes[random.randint(0, len(gymBroQuotes) - 1)]
        )
        await client.change_presence(activity=gymBroQuote)
        await asyncio.sleep(300.0)


gymBroQuotes = [
    "Train your chest to be the best! 🏋️",
    "Lift together, get big together! 🏋️🏋️",
    "You have to row, to stay in the flow! 🚣",
    "Pick up the pace to win the race! 🏅",
    "Form is temporary, broken back is forever! 🏋️",
    "Suns out, guns out! ☀",
    "Cardio's before the party hoes! 🏃",
    "If the bar ain't bending, you're just pretending! 🏋️",
    "Bench press to impress! 🏋️",
    "Don’t limit your challenges, challenge your limits! 🏃",
    "It never gets easier, you just get better! 📈",
    "In the gym you commit, you will be fit! 🏃",
    "The body achieves, what the mind believes! 💪",
    "Lifting weights and getting dates! 💖",
    "Train insane or remain the same! 🏋️",
    "Hustle for the muscle☀",
    "Curls get the girls! 💪 (or boys, if that's what you're into) 💪",
    "Swole is the goal, size is the prize! 🏅"
]
