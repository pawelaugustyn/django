import datetime

from django.db import models
from django.utils import timezone


class Vehicle(models.Model):
    line_number = models.CharField(max_length=10)
    brigade = models.IntegerField()
    last_updated = models.DateTimeField('last updated date')
    lat = models.FloatField()
    lon = models.FloatField()

    def is_moving(self):
        return self.last_updated > (timezone.now() - datetime.timedelta(seconds=30))

    def __str__(self):
        return str(self.line_number)+" ("+str(self.last_updated)+")"
