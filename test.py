import requests
import uuid

body = {
    "username": "test3",
    "password": "test"
}

r = requests.post("http://10.8.0.3:5000/registration", data=body)


def refresh(refresh_token):
    r = requests.post("http://10.8.0.3:5000/token/refresh", )


def login(username, password):
    body = {
        "username": username,
        "password": password
    }

    r = requests.post("http://10.8.0.3:5000/login", data=body)
    return r.json()


def get(access_token, url):
    header = {
        'Authorization': "Bearer " + access_token
    }
    r = requests.get(url, headers=header)
    return r.json()


def put(access_token, id, otype, data):

    header = {
        'Authorization': "Bearer " + access_token
    }

    body = {
        'o_type': otype,
        'data': data
    }

    r = requests.put("http://10.8.0.3:5000/db/"+id, headers=header, json=body)

    return r.text

auth = login('test3', 'test')
print(auth)
# print(get(auth['access_token'], "http://10.8.0.3:5000/secret"))



# for i in range(10000):
#     print(put(auth['access_token'], "d36dab4c-48ca-4c2d-8cd4-78cde0c1009c", 'test', d))

import time
import random

# print(put(auth['access_token'], "d36dab4c-48ca-4c2d-8cd4-78cde0c1009c", 'test', "lol"))
for i in range(100):

    d = {
        'sensor_if': 1,
        'temp': random.random()*10,
        'co2': random.choice([random.random()*100, None])
    }

    print(put(auth['access_token'], str(uuid.uuid4()), 'env_sensors', d))
    time.sleep(.01)
    # print(get(auth['access_token'], "http://10.8.0.3:5000/db/d36dab4c-48ca-4c2d-8cd4-78cde0c1009c"))

