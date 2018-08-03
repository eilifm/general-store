# general-store
"Just a semi-structured place to put things"

I spend a lot of time thinking up projects that all need a small amount of state managed
in a loosly structured way. GeneralStore is my evolving answer to these needs. 

1. Most of the time it can simply be a key-value store
2. Sometimes I want to mark a key as belonging to type/table/collection
3. Sometimes I want to link objects to their parents
4. Sometimes I want objects to just be events and I want to get them in order
5. I just want to throw JSON at the endpoint and have it handle the rest
6. I'll take care of parsing/executing on the data stored in my project's application, don't worry about massive amounts of context.
7. I want the underlying data storage to support a SQL query engine to support deeper analysis of whatever I decide to store without any ETL BS. 
8. I want to be able to spin up a new on of these databases and relink an app that needs more database horsepower. 

https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html

A postgres backed thing that meets the above requirements

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

