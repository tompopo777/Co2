# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.conf.urls import url
from django.urls import path, re_path
from apps.home import views,csv
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path("carbon-system/", views.carbon_system, name='carbon-system'),
    # 新增設備
    path("emergency_generators_add/", views.emergency_generators_add),
    path("combustion_equipment_add/", views.combustion_equipment_add),
    path("official_car_add/", views.official_car_add),
    path("material_add/", views.material_add),
    path("process_add/", views.process_add),
    path("refrigerator_add/", views.refrigerator_add),
    path("airconditioner_add/", views.airconditioner_add),
    path("vehicle_add/", views.vehicle_add),
    path("water_dispenser_add/", views.water_dispenser_add),
    path("ice_water_dispenser_add/", views.ice_water_dispenser_add),
    path("ice_maker_add/", views.ice_maker_add),
    path("other_device_add/", views.other_device_add),
    path("refrigerant_total_table_add/", views.refrigerant_total_table_add),
    path("extinguisher_add/", views.extinguisher_add),
    path("personnel_inventory_add/", views.personnel_inventory_add),
    path("security_add/", views.security_add),
    path("electricity_add/", views.electricity_add),
    path("upstream_transportation_add/", views.upstream_transportation_add),
    path("downstream_transportation_add/", views.downstream_transportation_add),
    path("employee_commute_add/", views.employee_commute_add),
    path("employee_business_trip_add/", views.employee_business_trip_add),
    path("waste_add/", views.waste_add),
    # ajax傳質
    path("ajax/process", views.load_process, name='loadprocess'),
    path("ajax/device", views.load_device, name='loaddevice'),
    path("ajax/table", views.load_table, name='loadtable'),
    path("ajax/title", views.add_title, name='loadtitle'),
    path("new_device/", views.add_page, name='loadadd'),
    path("edit_device/", views.edit_device, name='loadedit'),
    # Excel
    path("csv_view/", csv.csv_view, name='csv_view'),
    # 編輯設備
    path('update_device/<str:datasheet_id>&<int:single_dataID>', views.update_device, name='update_device'),
    # 刪除設備
    path('delete_device/', views.delete_device, name='delete_device'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
