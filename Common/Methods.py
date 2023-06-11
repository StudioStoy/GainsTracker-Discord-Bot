import json


async def checkStatusCode(response, channel, param=""):
    message = ""
    match response.status_code:
        case 400:
            message = "Ai Caramba that's a bad request if I ever saw one."
        case 401:
            message = "Could not authenticate user."
        case 403:
            message = f"User {param} not authorized for this action."
        case 404:
            message = f"{param} not found."
        case 409:
            message = f"Conflict: {param} already exists/was already added."
        case _:
            return

    if message != "":
        await channel.send(message)
        raise Exception


def getDataFromResponse(response):
    return json.loads(response.content)
