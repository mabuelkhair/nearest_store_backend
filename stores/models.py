from django.contrib.gis.db import models


class Profile(models.Model):
    location = models.PointField(null=False, blank=False,
                                 srid=4326, verbose_name="Location")
