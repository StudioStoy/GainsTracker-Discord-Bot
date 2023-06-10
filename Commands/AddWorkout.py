import requests


async def addWorkout(jsonWorkoutData, session=requests.session()):
    return session.post("http://aperture:420/gains/workout", json=jsonWorkoutData)
