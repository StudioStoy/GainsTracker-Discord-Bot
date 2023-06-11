import requests

from Common.Constants import BASE_URL


async def availableWorkouts(session=requests.session()):
    return session.get(f"{BASE_URL}/catalog/workout/available")
