from django.contrib.auth.models import User
from django.contrib.gis.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.PointField(null=False, blank=False,
                                 srid=4326, verbose_name="Location")
