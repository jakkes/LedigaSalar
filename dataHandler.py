from requests import get
import json

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
        return []

def _getRooms():
    try:
        return json.loads(get("https://www.kth.se/api/places/v2/places").text)
    except json.JSONDecodeError:
        return []

def _setModel():
    deps = _getDepartments()
    for dep in deps:
        courses = _getCourses(dep["code"])
        for course in courses:
            entries = getEntries(course["code"])
            for entry in entries:

            print(_getEntries(course["code"]))

def _getData():
    deps = _getDepartments()
    allLocs = []
    for dep in deps:
        courses = _getCourses(dep["code"])
        for course in courses:
            entries = getEntries(course["code"])
            for entry in entries:
