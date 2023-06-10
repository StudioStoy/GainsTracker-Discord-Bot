import requests


async def loginUser(username, password, session=requests.session()):
    loginPayload = {
        "userHandle": username,
        "password": password
    }

    return session.post("http://aperture:420/auth/login", json=loginPayload)

