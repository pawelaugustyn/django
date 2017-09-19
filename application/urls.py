from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'mapdata/stops/(?P<tram_id>[0-9A-Za-z]+)/(?P<stop_nr>[0-9]{6})/$', views.get_stop_coords, name='get_tram_stops_per_line'),
    url(r'mapdata/stops/(?P<tram_id>[0-9A-Za-z]+)/$', views.get_tram_stations_per_line, name='get_tram_stops_per_line'),
    url(r'mapdata/timetable/(?P<stop_id>[0-9]+)/$', views.get_closest_incoming_trams_per_stop),
    url(r'mapdata/directions/(?P<tram_id>[0-9A-Za-z]+)/$', views.get_available_directions, name='get_tram_directions_per_line'),
    url(r'mapdata/trams/(?P<tram_id>[0-9A-Za-z]+)/$', views.get_trams_per_line, name='get_tram_stops_per_line'),
    url(r'mapdata/predict/(?P<coordx>[0-9.]+)/(?P<coordy>[0-9.]+)/(?P<tramid>[0-9.]+)/(?P<brigade>[0-9]+)/$', views.get_predicted_arrival_time),
    url(r'$', views.index, name='index'),
]