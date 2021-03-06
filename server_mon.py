import requests
import uuid
import sys


body = {
    "username": "server",
    "password": "test"
}

r = requests.post("http://127.0.0.1:5000/registration", data=body)


def refresh(refresh_token):
    r = requests.post("http://127.0.0.1:5000/token/refresh", )


def login(username, password):
    body = {
        "username": username,
        "password": password
    }

    r = requests.post("http://127.0.0.1:5000/login", data=body)
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

    r = requests.put("http://127.0.0.1:5000/db/"+id, headers=header, json=body)

    return r.text

auth = login('test3', 'test')
print(auth)
# print(get(auth['access_token'], "http://127.0.0.1:5000/secret"))



# for i in range(10000):
#     print(put(auth['access_token'], "d36dab4c-48ca-4c2d-8cd4-78cde0c1009c", 'test', d))

import time
import random

import psutil

def cpu_dict():
    cpu_output = {
        "cores": psutil.cpu_count(),
        "usage": psutil.cpu_percent()
    }
    return cpu_output


def memory_dict():
    mem_data = psutil.virtual_memory()
    monitor_dict = {
        "total_memory": mem_data[0],
        "total_available": mem_data[1],
        "memory_percent": mem_data[2],
        "used": mem_data[3],
        "free": mem_data[4],
        "active": mem_data[5]
    }
    return monitor_dict


def generate_status():
    status = {
        "cpu": cpu_dict(),
        "memory": memory_dict()
    }
    return status

# print(put(auth['access_token'], "d36dab4c-48ca-4c2d-8cd4-78cde0c1009c", 'test', "lol"))
for i in range(int(sys.argv[1])):

    print(put(auth['access_token'], str(uuid.uuid4()), 'server_monitoring', generate_status()))
    time.sleep(float(sys.argv[2]))
    # print(get(auth['access_token'], "http://127.0.0.1:5000/db/d36dab4c-48ca-4c2d-8cd4-78cde0c1009c"))

