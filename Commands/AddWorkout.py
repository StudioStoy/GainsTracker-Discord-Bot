import requests


async def addWorkout(jsonWorkoutData):
    response = requests.post("http://aperture:420/gains/workout", jsonWorkoutData)

