from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'mapdata/$', views.get_data, name='get_map_data'),
    url(r'$', views.index, name='index'),
]