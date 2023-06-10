import json

import requests


async def loginUser(username, password):
    loginPayload = {
        'userHandle': username,
        'password': password
    }

    test = json.dumps(str(loginPayload))

    jwt = requests.post("http://aperture:420/auth/login", data=test)
    print(jwt.content)

    requests.session().headers["Authorization"] = str(jwt)


