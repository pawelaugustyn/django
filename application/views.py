from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.conf import settings
from django import template
from re import sub
import datetime
from os.path import isfile as isFileAvailable
import urllib.request
import json


def index(request):
    data = urllib.request.urlopen(getattr(settings, "API_WARSAW_URL_TRAMS"))

    toparse = json.load(data)
    trams_lines_list = []
    trams_list = {}
    tramIndex = 0
    vehicles_online = []
    if "result" in toparse:
        trams_data = toparse["result"]
        for tram in trams_data:
            number = int(tram["Lines"])
            tram["index"] = tramIndex
            tramIndex += 1
            vehicles_online.append(tram)
            if number in trams_lines_list:
                continue
            trams_lines_list.append(number)

        """if request.method == "POST":
            if "line" in request.POST:
                try:
                    line = int(request.POST["line"])
                    for tram in trams_data:
                        if line != int(tram["Lines"]):
                            continue
                        tram["id"] = len(vehicles_online)
                        vehicles_online.append(tram)
                except ValueError:
                    pass"""

    trams_lines_list.sort()
    trams_lines_list = [str(x) for x in trams_lines_list]

    context = {
        'google_maps_api_key': getattr(settings, "GOOGLE_MAPS_API_KEY", None),
        'lat': getattr(settings, "GOOGLE_MAPS_CENTER_LAT", None),
        'long': getattr(settings, "GOOGLE_MAPS_CENTER_LONG", None),
        'trams_lines': trams_lines_list,
        'trams': trams_list,
        'vehicles_online': vehicles_online,
        'trams_amount': tramIndex
    }
    return render(request, 'application/index.html', context)

def get_closest_incoming_trams_per_stop(request, stop_id):
    BASE_DIR = getattr(settings, "BASE_DIR")
    file_directory = BASE_DIR+"/application/timetable/"+stop_id+".json"
    #file_directory = BASE_DIR+"/application/static/tramstations.json"
    if not isFileAvailable(file_directory):
        raise Http404("Something went wrong!")
    file = open(file_directory, 'r')

    d = datetime.datetime.now()

    weekday = d.isoweekday()
    if weekday == 6:
        getDay = 1
    elif weekday == 7:
        getDay = 2
    else:
        getDay = 0

    toparse = json.load(file)
    if str(getDay) not in toparse:
        raise Http404("Something went wrong!")

    results = toparse[str(getDay)]

    try:
        currentTime = float(datetime.datetime.now().time().strftime("%H.%M"))
    except ValueError:
        raise Http404("Wrong response from the server")

    upcoming_departures = []
    departures = []

    for result in results:
        result[0] = float(result[0])
        if result[0] < currentTime:
            continue
        upcoming_departures.append(result)

    upcoming_departures.sort()
    directions = open(BASE_DIR+"/application/static/directions.json")
    directions = json.load(directions)
    upcoming_departures = [[str(x[0]), str(x[1]), str(x[2])] for x in upcoming_departures]
    elems = 5
    for departure in upcoming_departures:
        if elems == 0:
            break
        if len(departure[0].split(".")[1]) == 1:
            departure[0]=departure[0]+"0"
        departure[0] = ":".join(departure[0].split("."))
        if directions[departure[2]]:
            for direction in directions[departure[2]]:
                if direction["Symbol"] == departure[1][:6]:
                    departure[1] = direction["Direction"]
        departures.append(departure)
        elems -= 1

    context = {
        'upcoming_departures': departures
    }

    return render(request, 'application/timetable.html', context)


def get_trams_per_line(request, tram_id):
    data = urllib.request.urlopen(getattr(settings, "API_WARSAW_URL_TRAMS"))
    toparse = json.load(data)
    trams_list = dict()
    trams_list['result'] = []
    for tram in toparse['result']:
        if tram['Lines'] == tram_id:
            trams_list['result'].append(tram)
    return HttpResponse(json.dumps(trams_list))


def get_tram_stations_per_line(request, tram_id):
    data = open('application/static/tramstations.json', 'r')
    toparse = json.load(data)
    if tram_id not in toparse:
        raise Http404('Something went wrong!')
    to_return = dict()
    to_return['result'] = toparse[tram_id]
    return HttpResponse(json.dumps(to_return))


def get_stop_coords(request, tram_id, stop_nr):
    data = open('application/static/tramstations.json', 'r')
    toparse = json.load(data)
    loaded_stop = None
    if tram_id not in toparse:
        raise Http404('Something went wrong!')
    toparse = toparse[tram_id]
    for stop in toparse:
        if stop['Number'] == stop_nr:
            loaded_stop = dict()
            loaded_stop['result'] = stop
            break
    if loaded_stop is not None:
        return HttpResponse(json.dumps(loaded_stop))
    else:
        Http404('That train doesn\'t stop on specified station.')


def get_available_directions(request, tram_id):
    data = open('application/static/directions.json', 'r')
    toparse = json.load(data)
    if tram_id not in toparse:
        raise Http404('Something went wrong!')
    to_return = dict()
    to_return['result'] = toparse[tram_id]
    return HttpResponse(json.dumps(to_return))
