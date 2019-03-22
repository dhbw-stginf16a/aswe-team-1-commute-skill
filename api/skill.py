#!/usr/bin/env python3

import logging
import requests
import json
logger = logging.getLogger(__name__)

from app import PREFSTORE_CLIENT

class Route:
    def __init__(self, method, route, duration):
        self.method = method
        self.route = route
        self.duration = duration

def getEarliestAppointmentOnDay(user, date):
    raise BaseException("Not yet implemented") # TODO Erik (Ask Thore)

def existsPollen():
    raise BaseException("Not yet implemented") # TODO Andy

def isItRaining(date):
    raise BaseException("Not yet implemented") # TODO Erik

def getWork(user):
    preferences = PREFSTORE_CLIENT.get_user_prefs(user)
    if preferences['work'] is None: # TODO check name of this preference
        raise BaseException("Not yet implemented") # TODO think how to escalate to watson
    return preferences['work']

def getHome(user):
    preferences = PREFSTORE_CLIENT.get_user_prefs(user)
    if preferences['home'] is None: # TODO check name of this preference
        raise BaseException("Not yet implemented") # TODO think how to escalate to watson
    return preferences['home']

def getRouteCycling(user, start_from=None, destination=None):
    if start_from is None:
        start_from = getHome(user)
    if destination is None:
        destination = getWork(user)
    raise BaseException("Not yet implemented") # TODO Andy

def getRoutePublicTransport(user, start_from=None, destination=None):
    if start_from is None:
        start_from = getHome(user)
    if destination is None:
        destination = getWork(user)
    raise BaseException("Not yet implemented") # TODO Andy

def getRouteCar(user, start_from=None, destination=None):
    if start_from is None:
        start_from = getHome(user)
    if destination is None:
        destination = getWork(user)
    raise BaseException("Not yet implemented") # TODO Andy

#def get_user_prefs(user, keys):
#    print("request")
#    p = PREFSTORE_CLIENT.get_user_prefs(user)
#    print("response")
#    if len(keys) == 0:
#        return p
#    else:
#        fp = dict()
#        for key in keys:
#            if key in p:
#                fp[key] = p[key]
#
#        return fp
#
#def set_user_prefs(user, prefs):
#    PREFSTORE_CLIENT.set_user_prefs(user, prefs)
#    return { "success": True }
def work_route(user, date):
    timeOfArrival = getEarliestAppointmentOnDay(user, date)
    if timeOfArrival is None:
        return { "success": True, "noAppointments" : True }, 200
    preferences = PREFSTORE_CLIENT.get_user_prefs(user)

    methods = [
        getRouteCycling(user),
        getRoutePublicTransport(user),
        getRouteCar(user)
    ]
    if preferences['preferred_method'] is None:
        sorted(methods, key=lambda route: route.duration)
        return { "success": True, "method": methods[0].method, "route": methods[0].route}, 200
        # return { "success": False, "error" : "missingPreferredMethod" }, 200
    # TODO maybe add missing preferences
    pollen = False
    if date is None and preferences['allergies'] is not None:
        pollen = existsPollen()

    raining = isItRaining(date)

    if preferences['preferrred_method'] is "car" or pollen or raining:
        return { "success": True, "method": "car", "route": getRouteCar(user).route}, 200
    if preferences['preferrred_method'] is "publicTransport":
        return { "success": True, "method": "publicTransport", "route": getRoutePublicTransport(user).route}, 200
    if preferences['preferrred_method'] is "Cycling":
        return { "success": True, "method": "Cycling", "route": getRouteCycling(user).route}, 200

    raise BaseException("What are you doing here. This is not expected...")


def request(body):
    print("Skill request: {}".format(body))
    if body["type"] == "commute_work_route":
        return work_route(body["user"], body["payload"]["date"])
    elif body["type"] == "commute_route":
        raise BaseException("Not yet implemented")
    elif body["type"] == "commute_latest_leaving":
        raise BaseException("Not yet implemented")

