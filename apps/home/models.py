# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class section_one(models.Model):
    cpid = models.AutoField(primary_key=True)
    c_name = models.IntegerField()
    p_name = models.CharField(max_length=30)
class section_two(models.Model):
    did = models.AutoField(primary_key=True)
    d_name = models.CharField(max_length=30)
    cpid = models.ForeignKey(section_one, on_delete=models.CASCADE)
class emergency_generators(models.Model):
    id = models.AutoField(primary_key=True,)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=1)
    device_id = models.CharField(max_length=30)
    period_starttime = models.DateField()
    period_endtime = models.DateField()
    device_capacity = models.IntegerField()
    position = models.CharField(max_length=30)
    department = models.CharField(max_length=100)
    january = models.FloatField()
    february = models.FloatField()
    march = models.FloatField()
    april = models.FloatField()
    may = models.FloatField()
    june = models.FloatField()
    july = models.FloatField()
    august = models.FloatField()
    september = models.FloatField()
    october = models.FloatField()
    november = models.FloatField()
    december = models.FloatField()
    image_note = models.CharField(max_length=30)
    # image_path = models.ImageField(upload_to='img/')

class combustion_equipment(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=2)
    device_name = models.CharField(max_length=50)
    device_id = models.CharField(max_length=30)
    fuel_type = models.CharField(max_length=10)
    period_starttime = models.DateField()
    period_endtime = models.DateField()
    fuel_january = models.FloatField()
    fuel_february = models.FloatField()
    fuel_march = models.FloatField()
    fuel_april = models.FloatField()
    fuel_may = models.FloatField()
    fuel_june = models.FloatField()
    fuel_july = models.FloatField()
    fuel_august = models.FloatField()
    fuel_september = models.FloatField()
    fuel_october = models.FloatField()
    fuel_november = models.FloatField()
    fuel_december = models.FloatField()
    heat_january = models.FloatField()
    heat_february = models.FloatField()
    heat_march = models.FloatField()
    heat_april = models.FloatField()
    heat_may = models.FloatField()
    heat_june = models.FloatField()
    heat_july = models.FloatField()
    heat_august = models.FloatField()
    heat_september = models.FloatField()
    heat_october = models.FloatField()
    heat_november = models.FloatField()
    heat_december = models.FloatField()
    image_note = models.CharField(max_length=30)
    image_path = models.CharField(max_length=100)



