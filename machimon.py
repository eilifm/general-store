import requests
import uuid
import sys
import json
import logging
from logging.handlers import TimedRotatingFileHandler

import os
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = TimedRotatingFileHandler('machimon.log', when="m", interval=10, backupCount=10) #logging.FileHandler('hello.log')
handler.setLevel(logging.INFO)



# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)


stream = logging.StreamHandler()
stream.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)
# logger.addHandler(stream)


class GeneralStoreAPI(object):
    def __init__(self, url_prefix, username, password):
        self.url_prefix = url_prefix
        self.username = username
        self.password = password

        self.r_session = requests.Session()
        self.auth = self.login()
        logger.info(self.auth)
        self.access_token = self.auth['access_token']
        self.last_refresh = time.time()


    @staticmethod
    def register(url_prefix):
        body = {
            "username": os.environ['GENERAL_STORE_USERNAME'],
            "password": os.environ['GENERAL_STORE_PASSWORD']
        }
        r = requests.post(url_prefix+"/registration", data=body)
        return r.text

    def login(self):
        body = {
            "username": self.username,
            "password": self.password
        }
        r = self.r_session.post(self.url_prefix+ "/login", data=body)
        return r.json()

    # def refresh(self):
    #     r = requests.post(self.url_prefix + "/token/refresh", self.refresh_token)
    #     return r.json

    def chk_refresh(self):
        if time.time() - self.last_refresh >= 250:
            self.auth = self.login()
            self.access_token = self.auth['access_token']
            self.last_refresh = time.time()


    def get(self, url):
        self.chk_refresh()
        header = {
            'Authorization': "Bearer " + self.access_token
        }
        r = self.r_session.get(url, headers=header)

        return r.json()

    def put(self, id, otype, data):
        logger.info(data)
        self.chk_refresh()
        header = {
            'Authorization': "Bearer " + self.access_token
        }

        body = {
            'o_type': otype,
            'data': data
        }

        r = self.r_session.put(self.url_prefix+"/db/"+id, headers=header, json=body)

        return r.text

    def delete(self, id):
        self.chk_refresh()
        header = {
            'Authorization': "Bearer " + self.access_token
        }

        r = self.r_session.delete(self.url_prefix+"/db/"+id, headers=header)

        return r.text

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

def run():
    status = generate_status()
    retries = 0
    id = str(uuid.uuid4())
    r = api.put(id , str(sys.argv[3])+'_monitoring', status)

if __name__ == "__main__":
    api = GeneralStoreAPI('https://general-store.foxkid.io', os.environ['GENERAL_STORE_USERNAME'],
                          os.environ['GENERAL_STORE_PASSWORD'])
    for i in range(int(sys.argv[1])):
        try:
            run()
            time.sleep(float(sys.argv[2]))
        except Exception as e:
            logger.exception(e, exc_info=True)
            time.sleep(30)
            continue
