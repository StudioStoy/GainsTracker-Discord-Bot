import requests

from Common.Constants import BASE_URL


async def addWorkout(jsonWorkoutData, session=requests.session()):
    return session.post(f"{BASE_URL}/gains/workout", json=jsonWorkoutData)
