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
    # path("edit_device/<int:datasheet_id>/<int:single_dataID>", views.edit_device, name='loadedit'),
    path("edit_device/", views.edit_device, name='loadedit'),
    # Excel
    path("csv_view/", csv.csv_view, name='csv_view'),
    # 編輯設備
    path('update_device/<str:id>', views.update_device, name='update_device'),
    # path("update_device/", views.emergency_generators_update),
    # path("combustion_equipment_update/", views.combustion_equipment_update),
    # path("official_car_update/", views.official_car_update),
    path("material_update/", views.material_update),
    # path("process_update/", views.process_update),
    # path("refrigerator_update/", views.refrigerator_update),
    # path("airconditioner_update/", views.airconditioner_update),
    # path("vehicle_update/", views.vehicle_update),
    # path("water_dispenser_update/", views.water_dispenser_update),
    # path("ice_water_dispenser_update/", views.ice_water_dispenser_update),
    # path("ice_maker_update/", views.ice_maker_update),
    # path("other_device_update/", views.other_device_update),
    # path("refrigerant_total_table_update/", views.refrigerant_total_table_update),
    # path("extinguisher_update/", views.extinguisher_update),
    # path("personnel_inventory_update/", views.personnel_inventory_update),
    # path("security_update/", views.security_update),
    # path("electricity_update/", views.electricity_update),
    # path("upstream_transportation_update/", views.upstream_transportation_update),
    # path("downstream_transportation_update/", views.downstream_transportation_update),
    # path("employee_commute_update/", views.employee_commute_update),
    # path("employee_business_trip_update/", views.employee_business_trip_update),
    # path("waste_update/", views.waste_update),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
