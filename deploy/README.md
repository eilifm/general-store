# Build and deploy

Run the contents of this folder to build and deploy this app on any box running
CentOD 7 or Ubuntu 16.04

## `app`
Application deployment

### Simple uwsgi
from the root directory of this repo
`uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi --master --processes 2 --threads 2 --stats 127.0.0.1:91911`

Tuned
`YOURAPPLICATION_SETTINGS=./env.cfg uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi --processes 1  --threads 2 --enable-thread  --lazy-apps --disable-logging --stats 127.0.0.1:9191 #logger file:logfile=/tmp/uwsgi.log,maxsize=2000000`

`YOURAPPLICATION_SETTINGS=./env.cfg uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi --processes 1  --threads 2 --enable-thread  --gevent 2000 -l 1000  --lazy-apps --disable-logging --stats 127.0.0.1:9191 #logger file:logfile=/tmp/uwsgi.log,maxsize=2000000`

### Simple bjoern
`python ./bjoern_server_run.py`

### Nginx + uwsgi
TBD

## `postgres`

# Platforms
Common use case will probably include deploying this on a cloud provider. Generally, all that 
is required for deployment is an executing machine with SSH access to the target. 

Provisioning will rely on a combination of BASH and Ansible. 

## Digital Ocean
The author hosts his personal projects on DigitalOcean

## AWS 
### EC2

### EC2 + RDS
This is arguably simpler. Deploying the app is independent of the database.

Looking for someone to submit a PR. 

## Google Cloud Platform