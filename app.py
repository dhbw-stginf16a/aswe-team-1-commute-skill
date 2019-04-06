#!/usr/bin/env python3

import time

import logging
import connexion
from flask_cors import CORS

import requests
from requests.exceptions import ConnectionError

import os
from api.RegistrationThread import RegistrationThread
logger = logging.getLogger(__name__)


CENTRAL_NODE_BASE_URL = os.environ.setdefault('CENTRAL_NODE_BASE_URL', 'http://localhost:8080/api/v1')
OUR_URL = os.environ.setdefault('OWN_URL', 'http://localhost:5000')

class PrefStoreClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_user_prefs(self, user):
        r = requests.get("{}/preferences/user/{}".format(self.base_url, user))
 #       assert r.status_code == 200
        return r.json()

 #   def set_user_prefs(self, user, prefs):
 #       r = requests.patch("{}/preferences/user/{}".format(self.base_url, user), json = prefs)
 #       assert r.status_code == 200

class ConcernClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def getConcern(self, user, monitor, request_type, payload):
        data = {
            "user": user,
            "type": request_type,
            "payload": payload
        }
        resp = requests.post("{}/monitoring/{}".format(self.base_url, monitor), json=data).json()
#        assert resp.status_code == 200#
        logger.debug(resp[0]['payload'])
        return resp[0].setdefault('payload', {})


PREFSTORE_CLIENT = PrefStoreClient(CENTRAL_NODE_BASE_URL)
CONCERN_CLIENT = ConcernClient(CENTRAL_NODE_BASE_URL)


app = connexion.App(__name__, specification_dir='openapi/')
app.add_api('openapi.yml')

# Set CORS headers
CORS(app.app)

# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

logger.info('App initialized')

app.registerThread = RegistrationThread(CENTRAL_NODE_BASE_URL, OUR_URL)
app.registerThread.start()
