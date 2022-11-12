# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class EmergencyGenerators(models.Model):
    device_id = models.CharField(max_length=30, null=False)
    period_startime = models.DateField(null=False)
    period_endtime = models.DateField(null=False)
    device_capacity = models.CharField(max_length=30, null=False)
    position = models.CharField(max_length=30, null=False)
    department = models.CharField(max_length=100, null=True)
    january = models.FloatField(null=False)
    february = models.FloatField(null=False)
    march = models.FloatField(null=False)
    april = models.FloatField(null=False)
    may = models.FloatField(null=False)
    june = models.FloatField(null=False)
    july = models.FloatField(null=False)
    august = models.FloatField(null=False)
    september = models.FloatField(null=False)
    october = models.FloatField(null=False)
    november = models.FloatField(null=False)
    december = models.FloatField(null=False)
    image_note = models.CharField(max_length=30, null=False)
    image_path = models.CharField(max_length=100, null=False)

    def _str_(self):
        return self.device_id
