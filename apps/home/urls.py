# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.conf.urls import url
from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path("carbon-system/", views.carbon_system),
    path("emergency_generator/", views.emergency_generator),
    path("emergency_generators_add/", views.emergency_generators_add),
    path("combustion_equipment_add/", views.combustion_equipment_add),
    path("ajax/process", views.load_process, name='loadprocess'),
    path("ajax/device", views.load_device, name='loaddevice'),
    path("ajax/table", views.load_table, name='loadtable'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
