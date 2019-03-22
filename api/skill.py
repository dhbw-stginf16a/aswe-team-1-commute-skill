#!/usr/bin/env python3

import logging
import requests
import json
logger = logging.getLogger(__name__)

from app import PREFSTORE_CLIENT

def get_user_prefs(user, keys):
    print("request")
    p = PREFSTORE_CLIENT.get_user_prefs(user)
    print("response")
    if len(keys) == 0:
        return p
    else:
        fp = dict()
        for key in keys:
            if key in p:
                fp[key] = p[key]

        return fp

def set_user_prefs(user, prefs):
    PREFSTORE_CLIENT.set_user_prefs(user, prefs)
    return { "success": True }

def request(body):
    print("Skill request: {}".format(body))
    if body["type"] == "get_user_prefs":
        return get_user_prefs(body["user"], body["payload"]["keys"])
    elif body["type"] == "set_user_prefs":
        return set_user_prefs(body["user"], body["payload"])
