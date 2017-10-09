#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import datetime
import threading
import logging
from requests import get

class Data:
    Model = {}
    Rooms = ["A1","A2"]
    Valid = None

def _getDepartments():
    try:
        return json.loads(get("https://www.kth.se/api/kopps/v2/departments.sv.json").text)
    except json.JSONDecodeError:
        return []
    except Exception as e:
        logging.error("Exception in _getDepartments")
        logging.error(e)
        return []

def _getCourses(depCode):
    try:
        return json.loads(get("https://www.kth.se/api/kopps/v2/courses/{0}.json".format(depCode)).text)["courses"]
    except json.JSONDecodeError:
        return []
    except Exception as e:
        logging.error("Exception in _getCourses, department " + depCode)
        logging.error(e)
        return []

def _getEntries(courseCode):
    try:
        return json.loads(get("https://www.kth.se/api/schema/v2/course/{0}".format(courseCode)).text)
    except json.JSONDecodeError:
        return json.loads('{"entries":[]}')
    except Exception as e:
        logging.error("Exception in _getEntries, course " + courseCode)
        logging.error(e)
        return []

def _getRooms():
    try:
        rooms = []
        data = json.loads(get("https://www.kth.se/api/places/v2/places").text)
        for room in data:
            rooms.append(room["name"])
        return rooms
    except json.JSONDecodeError:
        return []
    except Exception as e:
        logging.error("Exception in _getRooms")
        logging.error(e)
        return []

def init():
    logging.info("Initiating dataHandler.")
    thread = threading.Thread(target=_setModel)
    thread.start()

def _setTimer():
    now = datetime.datetime.now()
    nextRun = datetime.datetime(now.year,now.month,now.day,0,1,0) + datetime.timedelta(days = 1)

    secondsLeft = (nextRun - now).seconds

    logging.info("Setting new model in {0} seconds".format(str(secondsLeft)))

    t = threading.Timer(secondsLeft,_setModel)
    t.start()

def _setModel():

    logging.info("Setting new model")

    deps = _getDepartments()
    rooms = _getRooms()

    now = datetime.datetime.now()

    model = {}
    for h in range(now.hour,23):
        model[h] = rooms[:]

    for dep in deps:
        courses = _getCourses(dep["code"])
        for course in courses:
            entries = (_getEntries(course["code"]))["entries"]
            for entry in entries:
                start = datetime.datetime.strptime(entry["start"], "%Y-%m-%d %H:%M:%S")
                end = datetime.datetime.strptime(entry["end"], "%Y-%m-%d %H:%M:%S")
                
                startE = start.date() == now.date()
                endE = end.date() == now.date()

                if startE is False or endE is False:
                    continue

                locations = entry["locations"]

                for hour in range(start.hour, end.hour):
                    if hour not in model:
                        continue
                    for location in locations:
                        if location["name"] in model[hour]:
                            model[hour].remove(location["name"])

    Data.Model = model
    Data.Rooms = rooms
    Data.Valid = now.date()

    logging.info("Model set.")
    _setTimer()

def FreeRooms(fromHour, toHour):
    
    rooms = None

    while rooms is None and fromHour < toHour:
        if fromHour in Data.Model.keys():
            rooms = Data.Model[fromHour][:]
        else:
            fromHour += 1

    if rooms is None:
        return sorted(Data.Rooms[:])

    for hour in range(fromHour + 1, toHour):
        for room in rooms:
            if not room in Data.Model[hour]:
                rooms.remove(room)

    return {
        "valid": Data.Valid,
        "rooms": sorted(rooms)
    }