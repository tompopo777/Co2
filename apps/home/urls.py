# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.conf.urls import url
from django.urls import path, re_path
from apps.home import views, csv, count
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
                  path("extinguisher_add/", views.extinguisher_add),
                  path("personnel_inventory_add/", views.personnel_inventory_add),
                  path("employee_add/", views.employee_add),
                  path("waste_water_add/", views.waste_water_add),
                  path("waste_sludge_add/", views.waste_sludge_add),
                  path("solvent_aerosol_emission_sources_add/", views.solvent_aerosol_emission_sources_add),
                  path("VOCs_one_add/", views.VOCs_one_add),
                  path("VOCs_two_add/", views.VOCs_two_add),
                  path("electricity_add/", views.electricity_add),
                  path("upstream_transportation_add/", views.upstream_transportation_add),
                  path("downstream_transportation_add/", views.downstream_transportation_add),
                  path("employee_commute_add/", views.employee_commute_add),
                  path("employee_business_trip_add/", views.employee_business_trip_add),
                  path("waste_add/", views.waste_add),
                  path("pipe_wastewater_add/", views.pipe_wastewater_add),
                  path("purchase_material_add/", views.purchase_material_add),
                  path("product_indirect_emissions_add/", views.product_indirect_emissions_add),
                  # ajax傳質
                  path("ajax/process", views.load_process, name='loadprocess'),
                  path("ajax/device", views.load_device, name='loaddevice'),
                  path("ajax/table", views.load_table, name='loadtable'),
                  path("ajax/title", views.add_title, name='loadtitle'),
                  path("edit_device/", views.edit_device, name='loadedit'),
                  path("chemical_dropdowm/", views.chemical_dropdowm, name='chemical_dropdowm'),
                  path("loadchemical/", views.load_chemical, name='loadchemical'),
                  path("copy_last_year_data/", views.copy_last_year_data, name='copy_last_year_data'),
                  # Excel
                  path("export_excel/", csv.export_excel, name='export_excel'),
                  path('import_excel/', csv.import_excel, name='import_excel'),
                  # 新增設備轉跳
                  path("new_device/", views.add_page, name='loadadd'),
                  # 編輯設備
                  path('update_device/<int:single_dataID>', views.update_device, name='update_device'),
                  # 刪除設備
                  path('delete_device/', views.delete_device, name='delete_device'),
                  # 匯出總表
                  path("calculate_summary/", count.calculate_summary, name='calculate_summary'),
                  # Matches any html file
                  re_path(r'^.*\.*', views.pages, name='pages'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
