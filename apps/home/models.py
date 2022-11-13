# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User, UserManager


# Create your models here.
class section_one(models.Model):
    cp_id = models.IntegerField(primary_key=True)
    c_name = models.IntegerField
    p_name = models.CharField(max_length=30)
class section_two(models.Model):
    d_id = models.IntegerField(primary_key=True)
    d_name = models.CharField(max_length=30)
    cp_id = models.ForeignKey(section_one, on_delete=models.CASCADE)
#
# class GalaxyUser(models.Model):
#     id = models.IntegerField(primary_key=True)
#     create_time = models.DateTimeField(null=True, blank=True)
#     update_time = models.DateTimeFi
#     email = models.CharField(max_length=765)
#     password = models.CharField(max_length=120)
#     external = models.IntegerField(null=True, blank=True)
#     deleted = models.IntegerField(null=True, blank=True)
#     purged = models.IntegerField(null=True, blank=True)
#     username = models.CharField(max_length=765, blank=True)
#     form_values_id = models.IntegerField(null=True, blank=True)
#     disk_usage = models.DecimalField(null=True, max_digits=16, decimal_places=0, blank=True)
#
#     objects = UserManager()
#
#     class Meta:
#         db_table = u'galaxy_user'


class emergency_generators(models.Model):
    id = models.IntegerField(primary_key=True,)
    d_id = models.ForeignKey(section_two, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=30)
    period_starttime = models.DateField()
    period_endttime = models.DateField()
    device_capacity = models.CharField(max_length=30)
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

    def _str_(self):
        return self.device_id
