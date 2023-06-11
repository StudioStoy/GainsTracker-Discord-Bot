import requests

from Common.Constants import BASE_URL


async def loginUser(username, password, session=requests.session()):
    loginPayload = {
        "userHandle": username,
        "password": password
    }

    return session.post(f"{BASE_URL}/auth/login", json=loginPayload)

