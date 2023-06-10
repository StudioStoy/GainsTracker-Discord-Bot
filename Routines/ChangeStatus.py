import asyncio
import random

import discord


async def changeStatus(client):
    while True:
        randInt = random.randint(0, len(gymBroQuotes) - 1)

        await client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=gymBroQuotes[randInt]))

        await asyncio.sleep(300.0)

gymBroQuotes = [
    "Train your chest to be the best",
    "Lift together, get big together",
    "May your weight feel light and your prs tall",
    "You gotta row, to stay in the flow",
    "If you don’t pick up the pace you won’t win the race",
    "You need to sweat to become a threat",
    "Form is temporary, broken back is forever",
    "Suns out, guns out",
    "Cardios before the party hoes",
    "If the bar ain't bending, you're just pretending",
    "Bench press for dropping that dress",
    "Power shrugs for shower hugs",
    "Don’t limit your challenges, challenge your limits",
    "It never gets easier, you just get better",
    "The goal is fit, the gym where you commit",
    "Met de fiets ga je niet voor niets",
    "The body achieves, what the mind believes",
    "Lifting weights and getting dates",
    "No pecs, no sex",
    "Train insane or remain the same",
    "Bench press to impress",
    "Hustle for the muscle",
    "Curls get the girls",
    "Swole is the goal, size is the price"
]
