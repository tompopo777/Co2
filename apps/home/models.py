# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class section_one(models.Model):
    cp_id = models.AutoField(primary_key=True)
    c_name = models.IntegerField()
    p_name = models.CharField(max_length=30)
class section_two(models.Model):
    d_id = models.AutoField(primary_key=True)
    d_name = models.CharField(max_length=30)
    cp_id = models.ForeignKey(section_one, on_delete=models.CASCADE)
class emergency_generators(models.Model):
    id = models.AutoField(primary_key=True,)
    d_id = models.ForeignKey(section_two, on_delete=models.CASCADE, default=1)
    device_id = models.CharField(max_length=30)
    period_starttime = models.DateField()
    period_endttime = models.DateField()
    device_capacity = models.IntegerField(max_length=10)
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
    image_path = models.CharField(max_length=100)


