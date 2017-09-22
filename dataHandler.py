from requests import get
import json
import datetime
import threading

_model = {}
_rooms = ["A1","A2"]

def _getDepartments():
    try:
        return json.loads(get("https://www.kth.se/api/kopps/v2/departments.sv.json").text)
    except json.JSONDecodeError:
        return []

def _getCourses(depCode):
    try:
        return json.loads(get("https://www.kth.se/api/kopps/v2/courses/{0}.json".format(depCode)).text)["courses"]
    except json.JSONDecodeError:
        return []

def _getEntries(courseCode):
    try:
        return json.loads(get("https://www.kth.se/api/schema/v2/course/{0}".format(courseCode)).text)
    except json.JSONDecodeError:
        return json.loads('{"entries":[]}')

def _getRooms():
    try:
        return json.loads(get("https://www.kth.se/api/places/v2/places").text)
    except json.JSONDecodeError:
        return []

def init():
    _setTimer()
    thread = threading.Thread(target=_setModel)
    thread.start()

def _setTimer():
    now = datetime.datetime.now()
    nextRun = datetime.datetime(now.year,now.month,now.day,0,1,0) + datetime.timedelta(days = 1)

    secondsLeft = (nextRun - now).seconds

    print("Setting new model in {0} seconds".format(str(secondsLeft)))

    t = threading.Timer(secondsLeft,_setModel)
    t.start()

def _setModel():

    print("Setting new model")

    deps = _getDepartments()
    rooms = _getRooms()

    now = datetime.datetime.now()

    model = {}
    for h in range(now.hour,23):
        model[h] = [];
        for room in rooms:
            model[h].append(room["name"])

    for dep in deps:
        courses = _getCourses(dep["code"])
        for course in courses:
            entries = (_getEntries(course["code"]))["entries"]
            for entry in entries:
                start = datetime.datetime.strptime(entry["start"], "%Y-%m-%d %H:%M:%S")
                end = datetime.datetime.strptime(entry["end"], "%Y-%m-%d %H:%M:%S")
                
                if start.date() != now.date() or end.date != now.date():
                    continue

                locations = entry["locations"]

                for hour in range(start.hour, end.hour - 1):
                    for location in locations:
                        model[hour].remove(location["name"])

    _model = model
    _rooms = rooms

    print("Model set.")
    _setTimer()

def FreeRooms(fromHour, toHour):
    
    rooms = None;
    
    while rooms == None and fromHour < toHour:
        if fromHour in _model.keys():
            rooms = _model[fromHour]
        else:
            fromHour += 1

    if rooms == None:
        return _rooms

    for hour in range(fromHour + 1, endHour - 1):
        for room in rooms:
            if not room in _model[hour]:
                rooms.remove(room)

    return rooms