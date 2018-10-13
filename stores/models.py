from django.contrib.gis.db import models


class Store(models.Model):
    location = models.PointField(null=False, blank=False,
                                 srid=4326, verbose_name="Location")
    name = models.CharField(max_length=100)
