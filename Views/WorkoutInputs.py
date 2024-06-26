import discord
from discord.ui import TextInput

repsInputs = [
    TextInput(
        custom_id='repsInput',
        label="Amount of reps:",
        placeholder='0',
        max_length=8,
        required=True,
        style=discord.TextStyle.short
    ),
    TextInput(
        custom_id='notesInput',
        label="Notes:",
        placeholder='Hell yeah bro',
        max_length=100,
        required=False,
        style=discord.TextStyle.paragraph
    )
]

strengthInputs = [
    TextInput(
        custom_id='weightInput',
        label="Amount of weight in kg (use dots as comma's):",
        placeholder='0',
        max_length=8,
        required=True,
        style=discord.TextStyle.short
    ),
    TextInput(
        custom_id='repsInput',
        label="Amount of reps:",
        placeholder='0',
        max_length=10,
        required=True,
        style=discord.TextStyle.short
    ),
    TextInput(
        custom_id='notesInput',
        label="Notes:",
        placeholder='Hell yeah bro',
        max_length=100,
        required=False,
        style=discord.TextStyle.paragraph
    )
]

timeEnduranceInputs = [
    TextInput(
        custom_id='timeInput',
        label="Time (`9`, `1:05` or `23:30` is also valid):",
        placeholder='00:00:00',
        max_length=8,
        required=True,
        style=discord.TextStyle.short
    ),
    TextInput(
        custom_id='notesInput',
        label="Notes:",
        placeholder='Hell yeah bro',
        max_length=100,
        required=False,
        style=discord.TextStyle.paragraph
    )
]

timeAndDistanceEnduranceInputs = [
    TextInput(
        custom_id='timeInput',
        label="Time (`9`, `1:05` or `23:30` is also valid):",
        placeholder='00:00:00',
        max_length=8,
        required=True,
        style=discord.TextStyle.short
    ),
    TextInput(
        custom_id='distanceInput',
        label="Distance in km (use dots as comma's):",
        placeholder='0',
        max_length=8,
        required=True,
        style=discord.TextStyle.short
    ),
    TextInput(
        custom_id='notesInput',
        label="Notes:",
        placeholder='Hell yeah bro',
        max_length=100,
        required=False,
        style=discord.TextStyle.paragraph
    )
]

generalInputs = [
    TextInput(
        custom_id='generalInput',
        label="general",
        placeholder='',
        max_length=10,
        required=False,
        style=discord.TextStyle.paragraph
    ),
    TextInput(
        custom_id='notesInput',
        label="Notes:",
        placeholder='Hell yeah bro',
        max_length=100,
        required=False,
        style=discord.TextStyle.paragraph
    )
]

inputsPerCategory = {
    "Reps": repsInputs,
    "Strength": strengthInputs,
    "TimeAndDistanceEndurance": timeAndDistanceEnduranceInputs,
    "TimeEndurance": timeEnduranceInputs,
    "General": generalInputs
}
