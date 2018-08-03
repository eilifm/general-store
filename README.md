# general-store
"Just a semi-structured place to put things"

I spend a lot of time thinking up projects that all need a small amount of state managed
in a loosly structured way. GeneralStore is my evolving answer to these needs. 

I acknowledge that there are a variety of other databases do many of the things that
GeneralStore is designed to do. With this in mind, I have still been frustrated by the
complexity of purpose built solutions. GeneralStore will not be an efficient datastore for 
every use case but it should have features that make "just fine" for personal projects that 
just need to work. 

For personal projects or use cases just around data collection, MongoDB and Redis are great
to stand things up quickly. When I use these I find myself with lots of stored data and barriers 
to understanding them. This API handles data collection brilliantly. 


# Deployment 
See `deploy/app` for application deployment/config info
See `deploy/postgres` for some assistance getting postgres set up on your instance of choice

## Config


```python
SECRET_KEY = 'some-secret-string'
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
```

# Examples

Maybe you can use it as simple IoT data store

```python
import requests
import uuid

data = {
    "sensor1": "values",
    "sensor2": "values",
    "sensor3": "values",
}

body = {
    "o_type": "my-iot",
    "data": data
}

headers = {}
base_url = ""
id = str(uuid.uuid4())

r = requests.put(base_url + '/db/'+ id, headers=headers, json=data)

```

# Product Definition

## User Stories
1. Most of the time it can simply be a key-value store
2. Sometimes I want to mark a key as belonging to type/table/collectio/namespace
3. Objects may be linked to their parents
4. Records in a namespace may be retrieved in timestamp order.
5. Web endpoint should follow standard patterns and be entirely JSON.
6. I'll take care of parsing/executing on the data stored in my project's application, don't worry about massive amounts of context.
7. SQL support to make analysis on this data seamless with ETL. 
8. I want to be able to spin up a new on of these databases and relink an app that needs more database horsepower. 
9. A given record can have a geographic reference
10. Stateless web server. Fast enough that a single instance is probably fine but horizontal scaling
is possible and painless. 

## Some Use Cases
1. Store semi-structured personal data like exports from Mint, PG&E, rent.
2. Personal IoT (Arduino, deployed RaspberryPis)
3. Store of jobs for a scheduler
4. Hacky pub-sub

## Given the Requirements...
1. Written in Python because 

https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html

A postgres backed thing that meets the above requirements

# Additional Discussion

https://blog.timescale.com/scaling-partitioning-data-postgresql-10-explained-cd48a712a9a1
