from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.conf import settings
from django import template
from re import sub
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
