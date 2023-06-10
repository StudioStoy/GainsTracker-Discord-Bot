import requests


async def availableWorkouts():
    response = requests.get("http://aperture:420/catalog/workout/available")
    print(response)
    print(response.content)
