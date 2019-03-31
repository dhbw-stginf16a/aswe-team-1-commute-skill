#!/usr/bin/env python3

import time

import logging
logger = logging.getLogger(__name__)

import connexion
from flask_cors import CORS

import requests
from requests.exceptions import ConnectionError

import os

CENTRAL_NODE_BASE_URL = os.environ["CENTRAL_NODE_BASE_URL"]
OUR_URL = os.environ["OWN_URL"]

class PrefStoreClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_user_prefs(self, user):
        r = requests.get("{}/preferences/user/{}".format(self.base_url, user))
        assert r.status_code == 200
        return r.json()

    def set_user_prefs(self, user, prefs):
        r = requests.patch("{}/preferences/user/{}".format(self.base_url, user), json = prefs)
        assert r.status_code == 200

class ConcernClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def getConcern(self, user, monitor, request_type, payload):
        data = {
            "user": user,
            "type": request_type,
            "payload": payload
        }
        resp = requests.patch("{}/monitoring/{}".format(self.base_url, monitor), json=data).json()
        assert r.status_code == 200
        logger.debug(resp[0]['payload'])
        return resp[0].setdefault('payload', {})


PREFSTORE_CLIENT = PrefStoreClient(CENTRAL_NODE_BASE_URL)
CONCERN_CLIENT = PrefStoreClient(CENTRAL_NODE_BASE_URL)


app = connexion.App(__name__, specification_dir='openapi/')
app.add_api('openapi.yml')

# Set CORS headers
CORS(app.app)

# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

while True:
    print("Attempt registration")
    try:
        r = requests.post("{}/skill".format(CENTRAL_NODE_BASE_URL), json = { "name": "commute", "endpoint": OUR_URL, "interests": ["time"]})  # TODO add more interests
        if r.status_code == 204:
            print("Registered")
            break
    except ConnectionError:
        logger.error('Failed to register at central node')
        pass

    time.sleep(2)

logger.info('App initialized')
