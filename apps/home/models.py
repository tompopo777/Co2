# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class SectionOne(models.Model):
    CP_id = models.IntegerField(primary_key=True)
    C_name = models.CharField(max_length=30)
    P_name = models.CharField(max_length=30)

class SectionTwo(models.Model):
    D_id = models.IntegerField(primary_key=True)
    D_name = models.CharField(max_length=30)
    CP_id = models.ForeignKey(SectionOne, on_delete=models.CASCADE)

class EmergencyGenerators(models.Model):
    id = models.IntegerField(primary_key=True)
    D_id = models.ForeignKey(SectionTwo, on_delete=models.CASCADE)
    period_starttime = models.DateField
    period_endttime = models.DateField
    device_id = models.CharField(max_length=30)
    device_capacity = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    department = models.CharField(max_length=30)
    total = models.FloatField
    image_path = models.CharField
    image_note = models.CharField
    january = models.FloatField
    february = models.FloatField
    march = models.FloatField
    april = models.FloatField
    may = models.FloatField
    june = models.FloatField
    july = models.FloatField
    august = models.FloatField
    september = models.FloatField
    october = models.FloatField
    november = models.FloatField
    december = models.FloatField
    def _str_(self):
        return self.id
