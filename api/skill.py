#!/usr/bin/env python3

import logging
import requests
import json
import datetime
import re
import dateutil.parser
import calendar
logger = logging.getLogger(__name__)

from app import PREFSTORE_CLIENT, CONCERN_CLIENT, CENTRAL_NODE_BASE_URL

class Route:
    def __init__(self, method, route, duration):
        self.method = method
        self.route = route
        self.duration = duration

def getEarliestAppointmentOnDay(user, date):
    # dateIso = dateutil.parser.parse("2019-04-07T00:11:19+00:00").isoformat
    # print(f"{dateIso}") # Temp

    payload = {
        "date": "2019-04-07T20:11:19+00:00",
        "user": user
    }
    data = CONCERN_CLIENT.getConcern(user, "calendar", "event_date", payload)
    event = min(data.setdefault('events', []), key=lambda x: dateutil.parser.parse(x['begin']))
    logger.debug("First Event of date is: " + str(event))
    startTime = dateutil.parser.parse(event['begin'])
    return calendar.timegm(startTime.utctimetuple())

def existsPollen(preferences):
    # set allergies to true if they're set in the preferences
    allergies = preferences['pollen'].split(';')
    pollen = { allergy: 'true' for allergy in allergies }

    # Define request body
    body = {
        'type': 'current_pollination',
        'payload': {
            "region": "Hohenlohe/mittlerer Neckar/Oberschwaben",
            "day": "today",
            "pollen": pollen
        }
    }
    # Request pollination information using user preferences
    resp = requests.post(f'{CENTRAL_NODE_BASE_URL}/monitoring/pollination', json=body).json()
    logger.debug(resp[0].setDefault['payload'], "payload Key Not Found in response")
    if resp[0].setdefault('payload', None) is not None:
        pollinationResp = resp[0]['payload'].setdefault('pollination', None)
        # Iterate over every allergy, if at least one is active (> 0), return a positive match
        for allergy in allergies:
           exposure = pollinationResp.setdefault(allergy, None)
           if exposure is not None and exposure is not "0":
               return True
    # if pollen preferences aren't set, ignore
    return False

def isItRaining(time, location):
    payload = {
        "location": "Stuttgart, de",
        "time": time
    }
    data = CONCERN_CLIENT.getConcern("", "weather", "weather_forecast", payload)
    rainingCodes = re.compile("[4236]..")  # Look at https://openweathermap.org/weather-conditions for more details
    for item in data['data']['weather']:
        if rainingCodes.fullmatch(str(item['id'])):
            return True
    return False

def getWork(user):
    preferences = PREFSTORE_CLIENT.get_user_prefs(user)
    if preferences['work_address'] is None:
        raise BaseException("Not yet implemented") # TODO think how to escalate to watson
    return preferences['work_address']

def getHome(user):
    preferences = PREFSTORE_CLIENT.get_user_prefs(user)
    if preferences['home_address'] is None:
        raise BaseException("Not yet implemented") # TODO think how to escalate to watson
    return preferences['home_address']

def getRoute(user, start_from=None, destination=None, traveltype='driving'):
    if start_from is None:
        start_from = getHome(user)
    if destination is None:
        destination = getWork(user)

    payload = {
        "location": start_from,
        "destination": destination,
        "travelmode": [traveltype]
    }
    data = CONCERN_CLIENT.getConcern(user, "traffic", "traffic_route", payload)
    logger.debug(data.setdefault('routes', "routes Key Not Found in response"))
    routes = data.setdefault('routes', None)
    if routes is not None:
        return routes
    else:
        raise BaseException("This shouldn't happen. No route was returned")

def getRouteCycling(user, start_from=None, destination=None):
    return getRoute(user, start_from, destination, "bicycling")

def getRoutePublicTransport(user, start_from=None, destination=None):
    return getRoute(user, start_from, destination, "transit")

def getRouteCar(user, start_from=None, destination=None):
    return getRoute(user, start_from, destination, "driving")

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
    if preferences['traffic_mode'] is None:
        sorted(methods, key=lambda route: route['duration'])
        return { "success": True, "method": methods[0]['method'], "route": methods[0]['route']}, 200
        # return { "success": False, "error" : "missingPreferredMethod" }, 200
    # TODO maybe add missing preferences
    pollen = False
    if date is None and preferences.setdefault('pollen', None) is not None:
        pollen = existsPollen(preferences['pollen'])

    raining = isItRaining(timeOfArrival, getHome(user))

    logger.error("trafficMode:" + repr(preferences['traffic_mode']))
    logger.error("pollen: " + repr(pollen))
    logger.error("raining: " + repr(raining))
    if preferences['traffic_mode'] == "bicycling" and not (raining or pollen):
        return { "success": True, "method": "bicycling", "route": getRouteCycling(user)}, 200
    if preferences['traffic_mode'] == "driving" or pollen:
        return { "success": True, "method": "driving", "route": getRouteCar(user)}, 200
    if preferences['traffic_mode'] == "transit":
        return { "success": True, "method": "transit", "route": getRoutePublicTransport(user)}, 200

    logger.error("Failed to determine method of transportation.")
    return { "success": False, "error": "Failed to decide which method of transportation is right for you. Have you set your preferences" }, 200


def request(body):
    print("Skill request: {}".format(body))
    if body["type"] == "commute_work_route":
        return work_route(body["user"], body["payload"]["date"])
    elif body["type"] == "commute_route":
        raise BaseException("Not yet implemented")
    elif body["type"] == "commute_latest_leaving":
        raise BaseException("Not yet implemented")

