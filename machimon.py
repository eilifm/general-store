import requests
import uuid
import sys


def refresh(refresh_token):
    r = requests.post(sys.argv[4]+"/token/refresh", )

def login(username, password):
    body = {
        "username": username,
        "password": password
    }

    r = requests.post(sys.argv[4]+"/login", data=body)
    return r.json()


def get(access_token, url):
    header = {
        'Authorization': "Bearer " + access_token
    }
    r = requests.get(url, headers=header)
    return r


def put(access_token, id, otype, data):

    header = {
        'Authorization': "Bearer " + access_token
    }

    body = {
        'o_type': otype,
        'data': data
    }

    print(json.dumps(body))
    r = requests.put(sys.argv[4]+"/db/"+id, headers=header, json=body)

    return r


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

if __name__ == "__main__":
    body = {
    "username": "server",
    "password": "test"
    }
    retries = 0
    while retries <= 1000:
        try:
            r = requests.post(sys.argv[4]+"/registration", data=body)

            auth = login('test3', 'test')
            print(auth)
            break
        except Exception as e:
            print(e)
            retries += 1
            time.sleep(60)



    start = time.time()
    count = 0
    import json
    last = 0
    for i in range(int(sys.argv[1])):

        status = generate_status()

        retries = 0
        while retries <= 100:
            try:
                if count % 100 == 0:
                    auth = login('server', 'test')
                    print(count/(time.time() - start))
                    print(auth)
                id = str(uuid.uuid4())

                r = put(auth['access_token'], id , str(sys.argv[3])+'_monitoring', status)
                # print( r.text.strip() + " - " + str(r.status_code))
                print(sys.argv[4]+"/db/"+id)
                break
            except Exception as e:
                print(e)
                retries += 1
                time.sleep(60)

            # r = get(auth['access_token'], sys.argv[4]+"/db/"+id)

        time.sleep(float(sys.argv[2]))
        # print(get(auth['access_token'], sys.argv[4]+"/db/d36dab4c-48ca-4c2d-8cd4-78cde0c1009c"))
        count += 1
