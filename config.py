# This file reads a config.json file that contains the db credentials, auth token etc.

import json

with open('config.json') as json_file:
    data = json.load(json_file)

# Define database credentials
db = {
    "host": data.get('db').get('host'),
    "username": data.get('db').get('username'),
    "password": data.get('db').get('password'),
    "db": data.get('db').get('db')
}

# User id from seas-nve.dk
user_id = data.get('user_id')

# Auth from seas-nve.dk
auth = data.get('auth').get('token')

# Timestamp of last update of auth token.
last_update_of_auth = data.get('auth').get('updated')