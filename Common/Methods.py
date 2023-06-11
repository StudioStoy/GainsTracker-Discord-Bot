import json


async def checkStatusCode(response, channel, param=""):
    if response.status_code == 400:
        await channel.send(f"Ai Caramba that's a bad request if i ever saw one.")
    elif response.status_code == 401:
        await channel.send(f"Could not authenticate user.")
    elif response.status_code == 403:
        await channel.send(f"User {param} not authorized.")
    elif response.status_code == 404:
        await channel.send(f"{param} not found.")
    elif response.status_code == 409:
        await channel.send(f"Conflict: {param} already exists.")


def getDataFromResponse(response):
    return json.loads(response.content)
