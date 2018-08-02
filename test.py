import requests
import uuid

body = {
    "username": "test3",
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

d = {'first_name': 'Eilif', 'last_name': 'Mikkelsen'}

print(put(auth['access_token'], "d36dab4c-48ca-4c2d-8cd4-78cde0c1009c", 'test', d))

# print(put(auth['access_token'], "d36dab4c-48ca-4c2d-8cd4-78cde0c1009c", 'test', "lol"))
for i in range(10000):
    print(put(auth['access_token'], str(uuid.uuid4()), 'test', d))
    # print(get(auth['access_token'], "http://127.0.0.1:5000/db/d36dab4c-48ca-4c2d-8cd4-78cde0c1009c"))



# {"message": "User test1 was created", "access_token": "", "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1MzMxNzk0OTgsIm5iZiI6MTUzMzE3OTQ5OCwianRpIjoiMzIxYTgxMjctMjgyYi00ZjQ2LWIwNzgtODBhZWU0OTg1YTk5IiwiZXhwIjoxNTM1NzcxNDk4LCJpZGVudGl0eSI6InRlc3QxIiwidHlwZSI6InJlZnJlc2gifQ.m6qVoKu2g0ea0KmkynBaA4wNzKunZtKT9ZW60eFOUy4"}