import requests
import uuid
import sys


body = {
    "username": "test3",
    "password": "test"
}

r = requests.post("http://localhost:5000/registration", data=body)


def refresh(refresh_token):
    r = requests.post("http://localhost:5000/token/refresh", )


def login(username, password):
    body = {
        "username": username,
        "password": password
    }

    r = requests.post("http://localhost:5000/login", data=body)
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

    r = requests.put("http://localhost:5000/db/"+id, headers=header, json=body)

    return r.text

auth = login('test3', 'test')
print(auth)

import time
import random


# print(put(auth['access_token'], "d36dab4c-48ca-4c2d-8cd4-78cde0c1009c", 'test', "lol"))
for i in range(int(sys.argv[1])):

    # Build your data payload
    d = {
        'sensor_if': 1,
        'temp': random.random()*10,
        'co2': random.choice([random.random()*100, None])
    }

    namespace = 'env_sensors'
    print(put(auth['access_token'], str(uuid.uuid4()), namespace, d))
    time.sleep(float(sys.argv[2]))
    # print(get(auth['access_token'], "http://localhost:5000/db/d36dab4c-48ca-4c2d-8cd4-78cde0c1009c"))

