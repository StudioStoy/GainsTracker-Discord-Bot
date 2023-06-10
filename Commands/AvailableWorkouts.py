import requests


async def availableWorkouts(session=requests.session()):
    return session.get("http://aperture:420/catalog/workout/available")
