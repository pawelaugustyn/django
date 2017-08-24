from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django import template
import urllib.request
import json


def index(request):
    data = urllib.request.urlopen(getattr(settings, "API_WARSAW_URL_TRAMS"))


    toparse = json.load(data)
    trams_lines_list = []
    trams_list = {}

    vehicles_online = []
    if "result" in toparse:
        trams_data = toparse["result"]
        for tram in trams_data:
            number = int(tram["Lines"])
            if number not in trams_list:
                trams_list[number] = []
            trams_list[number].append(tram)
            if number in trams_lines_list:
                continue
            trams_lines_list.append(number)

        if request.method == "POST":
            if "line" in request.POST:
                try:
                    line = int(request.POST["line"])
                    for tram in trams_data:
                        if line != int(tram["Lines"]):
                            continue
                        tram["id"] = len(vehicles_online)
                        vehicles_online.append(tram)
                except ValueError:
                    pass

    trams_lines_list.sort()
    trams_lines_list = [str(x) for x in trams_lines_list]

    context = {
        'google_maps_api_key': getattr(settings, "GOOGLE_MAPS_API_KEY", None),
        'lat': getattr(settings, "GOOGLE_MAPS_CENTER_LAT", None),
        'long': getattr(settings, "GOOGLE_MAPS_CENTER_LONG", None),
        'trams_lines': trams_lines_list,
        'trams': trams_list,
        'vehicles_online': vehicles_online
    }
    return render(request, 'application/index.html', context)

