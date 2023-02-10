# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import json
from json import dumps

import pandas as pd
from django import template
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.db import models

import apps
from .forms import *
from apps.home.models import *


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


# 下拉選單第二層
@login_required(login_url="/login/")
def load_process(request):
    if request.method == 'GET':
        current_class = request.GET.get('currentClass', None)
        # print("000000000000000000000000000000000000000000000000000000")
        if current_class:
            # all = list(section_one.objects.all())
            # print("777777777777777777777777777777777777777777777",all)
            data = list(section_one.objects.filter(c_name=current_class).values("p_name", "cpid"))
            return JsonResponse(data, safe=False)


# 下拉選單第三層
@login_required(login_url="/login/")
def load_device(request):
    if request.method == 'GET':
        current_process = request.GET.get('currentProcess', None)
        if current_process:
            d_data = list(section_two.objects.filter(cpid=current_process).values("d_name", "did"))
            return JsonResponse(d_data, safe=False)


# 抓欄位(
@login_required(login_url="/login/")
def load_table(request):
    if request.method == 'GET':
        device_id = request.GET.get('deviceId', None)
        t_name = list(section_two.objects.filter(did=device_id).values("d_name"))
        # print("888888888", t_name)
        # 從db撈每張表要顯示的值
        for a in t_name:
            if a["d_name"] == "緊急發電機":
                t_data = []
                raw_data = emergency_generators.objects.values("id", "years", "device_id",
                                                               "device_capacity", "position", "department",
                                                               "january", "february", "march", "april",
                                                               "may", "june", "july", "august",
                                                               "september", "october", "november", "december")
                # 計算加油量合計
                for i in range(raw_data.count()):
                    consumption_total = raw_data[i].get("january") + raw_data[i].get("february") + raw_data[i].get("march") + raw_data[i].get("april") + \
                                        raw_data[i].get("may") + raw_data[i].get("june") + raw_data[i].get("july") + raw_data[i].get("august") + \
                                        raw_data[i].get("september") + raw_data[i].get("october") + raw_data[i].get("november") + raw_data[i].get("december")
                    # print("total::::::::::::::::::::::::::::::::::::::::", total)
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的加油量丟回字典
                    single_data["total"] = consumption_total
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "燃燒設備":
                t_data = []
                # 「合計」前後的資料分開抓
                raw_data = combustion_equipment.objects.values("id", "years", "device_name", "device_id", "fuel_type",
                                                               "fuel_january", "fuel_february", "fuel_march", "fuel_april", "fuel_may", "fuel_june",
                                                               "fuel_july", "fuel_august", "fuel_september", "fuel_october", "fuel_november", "fuel_december")
                heat_data = combustion_equipment.objects.values("heat_january", "heat_february", "heat_march", "heat_april", "heat_may", "heat_june",
                                                                "heat_july", "heat_august", "heat_september", "heat_october", "heat_november", "heat_december")
                # 計算使用量合計/熱值平均
                for i in range(raw_data.count()):
                    Total_fuel = raw_data[i].get("fuel_january") + raw_data[i].get("fuel_february") + raw_data[i].get("fuel_march") + raw_data[i].get("fuel_april") + \
                                 raw_data[i].get("fuel_may") + raw_data[i].get("fuel_june") + raw_data[i].get("fuel_july") + raw_data[i].get("fuel_august") + \
                                 raw_data[i].get("fuel_september") + raw_data[i].get("fuel_october") + raw_data[i].get("fuel_november") + raw_data[i].get("fuel_december")

                    Total_heat = heat_data[i].get("heat_january") + heat_data[i].get("heat_february") + heat_data[i].get("heat_march") + heat_data[i].get("heat_april") + \
                                 heat_data[i].get("heat_may") + heat_data[i].get("heat_june") + heat_data[i].get("heat_july") + heat_data[i].get("heat_august") + \
                                 heat_data[i].get("heat_september") + heat_data[i].get("heat_october") + heat_data[i].get("heat_november") + heat_data[i].get("heat_december")
                    avg_heat = Total_heat / 12
                    # print("fuel::::::::::::::::::::::::::::::::::::::::", Total_fuel)
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的「合計」丟回字典
                    single_data["Total_fuel"] = Total_fuel
                    for j in heat_data[i]:
                        # 「合計」後的資料(每月熱值)丟回字典
                        single_data[j] = heat_data[i].get(j)
                    # 將計算後的「平均熱值」丟回字典
                    single_data["avg_heat"] = round(avg_heat, 4)
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "公務車":
                t_data = []
                # 「合計」前後的資料分開抓
                raw_data = official_car.objects.values("id", "years", "vehicle_type", "device_id", "fuel_type", "department", "metering_method")
                oil = official_car.objects.values("oil_january", "oil_february", "oil_march", "oil_april",
                                                  "oil_may", "oil_june", "oil_july", "oil_august",
                                                  "oil_september", "oil_october", "oil_november", "oil_december")
                elec = official_car.objects.values("elec_january", "elec_february", "elec_march", "elec_april",
                                                   "elec_may", "elec_june", "elec_july", "elec_august",
                                                   "elec_september", "elec_october", "elec_november", "elec_december")
                km = official_car.objects.values("km_january", "km_february", "km_march", "km_april",
                                                 "km_may", "km_june", "km_july", "km_august",
                                                 "km_september", "km_october", "km_november", "km_december")
                urea_data = official_car.objects.values("urea_january", "urea_february", "urea_march", "urea_april",
                                                        "urea_may", "urea_june", "urea_july", "urea_august",
                                                        "urea_september", "urea_october", "urea_november", "urea_december")
                # 計算耗用量合計
                for i in range(raw_data.count()):
                    # print("yes>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", official_car.objects.values("metering_method")[i].get("metering_method"))
                    if official_car.objects.values("metering_method")[i].get("metering_method") == "油車":
                        consumption_data = oil
                    elif official_car.objects.values("metering_method")[i].get("metering_method") == "電動車":
                        consumption_data = elec
                    elif official_car.objects.values("metering_method")[i].get("metering_method") == "公里數":
                        consumption_data = km

                    single_data = raw_data[i]
                    consumption_total = 0
                    for j in consumption_data[i]:
                        # print("oil:::", consumption_data[i].get(j))
                        # 「逐一」將資料(耗用量)丟回字典
                        single_data[j] = consumption_data[i].get(j)
                        consumption_total += consumption_data[i].get(j)
                    # print("single_data11111", single_data)
                    # 將計算後的耗用量丟回字典
                    single_data["consumption_total"] = consumption_total
                    urea_total = 0
                    for k in urea_data[i]:
                        urea_total += urea_data[i].get(k)  # 如果有(尿素)，加總資料(尿素)

                    if urea_total == 0:
                        for n in urea_data[i]:
                            single_data[n] = None  # 「逐一」將資料(尿素)丟回字典
                        single_data["urea_total"] = None  # 如果沒有(尿素)，設為空值
                    else:
                        for e in urea_data[i]:
                            single_data[e] = urea_data[i].get(e)  # 「逐一」將資料(尿素)丟回字典
                        single_data["urea_total"] = urea_total  # 如果沒有(尿素)，設為空值
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "原物料使用":
                t_data = list(
                    material.objects.values("id", "years", "material_id", "material_type", "material_name",
                                            "process_add_name", "chemical_name", "chemical_formula",
                                            "january", "february", "march", "april",
                                            "may", "june", "july", "august",
                                            "september", "october", "november", "december"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "製程添加化學品":
                t_data = []
                raw_data = process.objects.values("id", "years", "process_stage", "material_id", "process_add_name",
                                                  "chemical_name", "chemical_formula", "CAS_NO", "burn", "VOCs",
                                                  "january", "february", "march", "april",
                                                  "may", "june", "july", "august",
                                                  "september", "october", "november", "december")
                unit = process.objects.values("unit")
                # 計算使用量合計
                for i in range(raw_data.count()):
                    consumption_total = raw_data[i].get("january") + raw_data[i].get("february") + raw_data[i].get("march") + raw_data[i].get("april") + \
                                        raw_data[i].get("may") + raw_data[i].get("june") + raw_data[i].get("july") + raw_data[i].get("august") + \
                                        raw_data[i].get("september") + raw_data[i].get("october") + raw_data[i].get("november") + raw_data[i].get("december")
                    # print("total::::::::::::::::::::::::::::::::::::::::", total)

                    single_data = raw_data[i]
                    # 將計算後的使用量丟回字典
                    single_data["total"] = consumption_total
                    # 將單位丟回字典
                    for j in unit[i]:
                        single_data[j] = unit[i].get(j)
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "冰箱清單":
                t_data = []
                raw_data = refrigerator.objects.values("id", "years", "device_id", "device_name", "brand_name", "model_type",
                                                       "position", "filling_volume", "refrigerant_type", "filling_fix_volume",
                                                       "effusion_rate")
                # 取單筆逸散量計算
                for i in range(raw_data.count()):
                    # 將要運算的值分別撈出(逸散率/填充量)
                    effusion_volume = raw_data[i].get("effusion_rate") * 0.01 * raw_data[i].get("filling_volume")
                    # print("effusion_volume::::::::::::::::::::::::::::::::::::::::", effusion_volume)
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    single_data["effusion_volume"] = round(effusion_volume, 4)
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "冷氣機清單":
                t_data = []
                raw_data = airconditioner.objects.values("id", "years", "device_id", "device_name", "brand_name", "model_type",
                                                         "position", "filling_volume", "refrigerant_type", "filling_fix_volume",
                                                         "effusion_rate")
                # 取單筆逸散量計算
                for i in range(raw_data.count()):
                    # 將要運算的值分別撈出(逸散率/填充量)
                    effusion_volume = raw_data[i].get("effusion_rate") * 0.01 * raw_data[i].get("filling_volume")
                    # print("effusion_volume::::::::::::::::::::::::::::::::::::::::", effusion_volume)
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    single_data["effusion_volume"] = round(effusion_volume, 4)
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "車輛清單":
                t_data = []
                raw_data = vehicle.objects.values("id", "years", "device_id", "device_name", "brand_name", "model_type",
                                                  "position", "filling_volume", "refrigerant_type", "filling_fix_volume",
                                                  "effusion_rate")
                # 取單筆逸散量計算
                for i in range(raw_data.count()):
                    # 將要運算的值分別撈出(逸散率/填充量)
                    effusion_volume = raw_data[i].get("effusion_rate") * 0.01 * raw_data[i].get("filling_volume")
                    # print("effusion_volume::::::::::::::::::::::::::::::::::::::::", effusion_volume)
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    single_data["effusion_volume"] = round(effusion_volume, 4)
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "飲水機清單":
                t_data = []
                raw_data = water_dispenser.objects.values("id", "years", "device_id", "device_name", "brand_name", "model_type",
                                                          "position", "filling_volume", "refrigerant_type", "filling_fix_volume",
                                                          "effusion_rate")
                # 取單筆逸散量計算
                for i in range(raw_data.count()):
                    # 將要運算的值分別撈出(逸散率/填充量)
                    effusion_volume = raw_data[i].get("effusion_rate") * 0.01 * raw_data[i].get("filling_volume")
                    # print("effusion_volume::::::::::::::::::::::::::::::::::::::::", effusion_volume)
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    single_data["effusion_volume"] = round(effusion_volume, 4)
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "冰水機清單":
                t_data = []
                raw_data = ice_water_dispenser.objects.values("id", "years", "device_id", "device_name", "brand_name", "model_type",
                                                              "position", "filling_volume", "refrigerant_type", "filling_fix_volume",
                                                              "effusion_rate")
                # 取單筆逸散量計算
                for i in range(raw_data.count()):
                    # 將要運算的值分別撈出(逸散率/填充量)
                    effusion_volume = raw_data[i].get("effusion_rate") * 0.01 * raw_data[i].get("filling_volume")
                    # print("effusion_volume::::::::::::::::::::::::::::::::::::::::", effusion_volume)
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    single_data["effusion_volume"] = round(effusion_volume, 4)
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "製冰機清單":
                t_data = []
                raw_data = ice_maker.objects.values("id", "years", "device_id", "device_name", "brand_name", "model_type",
                                                    "position", "filling_volume", "refrigerant_type", "filling_fix_volume",
                                                    "effusion_rate")
                # 取單筆逸散量計算
                for i in range(raw_data.count()):
                    # 將要運算的值分別撈出(逸散率/填充量)
                    effusion_volume = raw_data[i].get("effusion_rate") * 0.01 * raw_data[i].get("filling_volume")
                    # print("effusion_volume::::::::::::::::::::::::::::::::::::::::", effusion_volume)
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    single_data["effusion_volume"] = round(effusion_volume, 4)
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "其他設備清單":
                t_data = []
                raw_data = other_device.objects.values("id", "years", "device_id", "device_name", "brand_name", "model_type",
                                                       "position", "filling_volume", "refrigerant_type", "filling_fix_volume",
                                                       "effusion_rate")
                # 取單筆逸散量計算
                for i in range(raw_data.count()):
                    # 將要運算的值分別撈出(逸散率/填充量)
                    effusion_volume = raw_data[i].get("effusion_rate") * 0.01 * raw_data[i].get("filling_volume")
                    # print("effusion_volume::::::::::::::::::::::::::::::::::::::::", effusion_volume)
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    single_data["effusion_volume"] = round(effusion_volume, 4)
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "滅火器":
                t_data = list(
                    extinguisher.objects.values("id", "years", "extinguisher_name", "extinguisher_type", "device_id", "position", "extinguisher_vendor",
                                                "chemical_weight", "inventory", "using_amount", "monthly", "replace_filling_amount", "replace_filling_date"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "人天清冊":
                t_data = list(
                    personnel_inventory.objects.values("id", "years", "employee_number",
                                                       "WKhours_january", "WKhours_february", "WKhours_march", "WKhours_april", "WKhours_may", "WKhours_june",
                                                       "WKhours_july", "WKhours_august", "WKhours_september", "WKhours_october", "WKhours_november", "WKhours_december",
                                                       "WKnum_january", "WKnum_february", "WKnum_march", "WKnum_april", "WKnum_may", "WKnum_june",
                                                       "WKnum_july", "WKnum_august", "WKnum_september", "WKnum_october", "WKnum_november", "WKnum_december"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "委外人員清冊":
                t_data = list(
                    employee.objects.values("id", "years", "career",
                                            "employeeNum_january", "employeeNum_february", "employeeNum_march", "employeeNum_april", "employeeNum_may", "employeeNum_june",
                                            "employeeNum_july", "employeeNum_august", "employeeNum_september", "employeeNum_october", "employeeNum_november", "employeeNum_december",
                                            "WKdays_january", "WKdays_february", "WKdays_march", "WKdays_april", "WKdays_may", "WKdays_june", "WKdays_july", "WKdays_august",
                                            "WKdays_september", "WKdays_october", "WKdays_november", "WKdays_december",
                                            "WKhours_january", "WKhours_february", "WKhours_march", "WKhours_april", "WKhours_may", "WKhours_june", "WKhours_july",
                                            "WKhours_august", "WKhours_september", "WKhours_october", "WKhours_november", "WKhours_december"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "廢水":
                t_data = list(
                    waste_water.objects.values("id", "years", "waste_water_treatment_name", "waste_water_inflow_rate", "average_inlet_COD_concentration",
                                               "average_COD_removal_rate", "CH4_capture_system_rate", "combustion_equipment_efficiency"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "廢汙泥":
                t_data = list(
                    waste_sludge.objects.values("id", "years", "waste_sludge_treatment_name", "waste_sludge_inflow_rate", "average_inlet_MLSS_concentration",
                                                "CH4_capture_system_rate", "combustion_equipment_efficiency"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "溶劑、噴霧劑":
                t_data = list(
                    solvent_aerosol_emission_sources.objects.values("id", "years", "species_used", "fugitive_recharge", "global_warming_potential"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "用電量":
                t_data = []
                # 將要運算的值分別撈出(逸散率/填充量)
                raw_data = electricity.objects.values("id", "years", "EMI_id", "address",
                                                      "january", "february", "march", "april",
                                                      "may", "june", "july", "august",
                                                      "september", "october", "november", "december")
                # 計算當月用電量
                for i in range(raw_data.count()):
                    kw_hr = raw_data[i].get("january") + raw_data[i].get("february") + raw_data[i].get("march") + raw_data[i].get("april") + \
                            raw_data[i].get("may") + raw_data[i].get("june") + raw_data[i].get("july") + raw_data[i].get("august") + \
                            raw_data[i].get("september") + raw_data[i].get("october") + raw_data[i].get("november") + raw_data[i].get("december")
                    kkw_hr = kw_hr / 1000
                    # print("kw_hr::::::::::::::::::::::::::::::::::::::::", kw_hr)
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    single_data["kw_hr"] = kw_hr
                    single_data["kkw_hr"] = kkw_hr
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "上游運輸":
                t_data = list(
                    upstream_transportation.objects.values("id", "acceptance_receipt", "commodity_name", "weight", "commodity_NW",
                                                           "organizational_use_products", "customer", "supplier", "supplier_address",
                                                           "trade_term", "receiving_address", "delivery_address",
                                                           "transport_distance", "transport_country", "transport_type", "transport_fuel", "paid", "trips",
                                                           "overseas_transport_distance", "overseas_delivery", "overseas_arrive", "overseas_paid", "overseas_trips",
                                                           "special_transport_distance", "special_transport_country", "special_transport_type", "special_transport_fuel", "special_paid", "special_trips",
                                                           "air_transport_distance", "air_delivery", "air_arrive", "air_paid", "air_trips"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "下游運輸":
                t_data = list(
                    downstream_transportation.objects.values("id", "acceptance_receipt", "commodity_name", "weight", "commodity_NW", "customer", "supplier", "supplier_address",
                                                             "trade_term", "receiving_address", "delivery_address",
                                                             "transport_distance", "transport_country", "transport_type", "transport_fuel", "paid", "trips",
                                                             "overseas_transport_distance", "overseas_delivery", "overseas_arrive", "overseas_paid", "overseas_trips",
                                                             "special_transport_distance", "special_transport_country", "special_transport_type", "special_transport_fuel", "special_paid", "special_trips",
                                                             "air_transport_distance", "air_delivery", "air_arrive", "air_paid", "air_trips"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "員工通勤":
                t_data = []
                # 將要運算的值分別撈出(員工數/每日工時/每月工作天數/加班+補休時數/請假時數/休假時數)
                pre_data = employee_commute.objects.values("id", "years", "employee_id", "department", "employee_name")
                post_data = employee_commute.objects.values("city", "township", "address", "commute_distance", "work_days")
                for i in range(pre_data.count()):
                    single_data = pre_data[i]
                    id = pre_data[i].get("id")
                    transportation = transportation_way.objects.filter(commute=id).values("transportation")
                    if len(transportation) > 1:
                        transportation_first = transportation_way.objects.filter(commute=id).values("transportation").first()
                        single_data["transportation"] = transportation_first.get("transportation") + "*"
                    else:
                        for t in transportation:
                            single_data["transportation"] = t.get("transportation")
                    for j in post_data[i]:
                        single_data[j] = post_data[i].get(j)
                    # 計算單筆距離合計
                    total_distance = post_data[i].get("commute_distance") * post_data[i].get("work_days") * 2
                    # print("total_distance::::::::::::::::::::::::::::::::::::::::", total_distance)
                    # 抓單筆資料
                    # 將計算後的逸散量丟回字典
                    single_data["total_distance"] = total_distance
                    # print("single_data::::::::::::::::::::::::::::::::::::::::", single_data)
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "員工出差":
                t_data = []
                raw_data = employee_business_trip.objects.values("id", "business_trip_number", "employee_id", "department", "employee_name", "business_trip_location", "business_trip_date")
                for i in range(raw_data.count()):
                    single_data = raw_data[i]
                    id = raw_data[i].get("id")
                    section = trip_section.objects.filter(trip_id=id).values("transportation", "distance")
                    transportation_dic = {"自駕汽車": 0.0, "高鐵": 0.0, "火車": 0.0, "計程車": 0.0, "機車": 0.0, "捷運": 0.0, "飛機": 0.0, "船舶": 0.0}
                    for s in section:
                        way = s.get("transportation")
                        if way in transportation_dic:
                            transportation_dic[way] += s.get("distance")
                        for d in transportation_dic:
                            if transportation_dic.get(d) == 0:
                                single_data[d] = None
                            else:
                                single_data[d] = round(transportation_dic.get(d), 4)
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "廢棄物":
                t_data = []
                raw_data = waste.objects.values("id", "waste_name", "waste_weigh", "waste_date",
                                                "waste_location", "waste_disposal", "waste_disposal_vendor",
                                                "transport_type", "transport_fuel", "transport_distance")
                for i in range(raw_data.count()):
                    # 計算單筆距離合計
                    if (raw_data[i].get("transport_distance") == None):
                        Tkm = "-"
                    else:
                        Tkm = raw_data[i].get("waste_weigh") * raw_data[i].get("transport_distance")
                    # print("Tkm::::::::::::::::::::::::::::::::::::::::", Tkm)
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    single_data["total_distance"] = Tkm
                    # print("single_data::::::::::::::::::::::::::::::::::::::::", single_data)
                    t_data.append(single_data)
                # print("t_data:::::::::::::::::::::::::::::::::::::::::", t_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "VOCs_1":
                t_data = list(VOCs_one.objects.values("id", "years", "emission", "concentration_ch4"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "VOCs_2":
                t_data = list(VOCs_two.objects.values("id", "years", "disposal_volume", "concentration_ch4", "voc_capture_rate", "combustion_equipment_rate",
                                                      "concentration_entrance", "concentration_exit", "builtIn_rate", "custom_rate"))
                return JsonResponse(t_data, safe=False)


@login_required(login_url="/login/")
def emergency_generators_add(request):
    EG_add = EGform(request.POST, request.FILES)
    if request.method == "POST":
        # print("77777777777777777")
        # print("EG_add", EG_add)
        if EG_add.is_valid():
            EG_add.save()
            return redirect('/carbon-system/')
        else:
            print(EG_add.errors)
            return redirect('/new_device/', {'device.errors': EG_add.errors})
            # return render(request, new_device, {'EG_add.errors': EG_add.errors})

    else:
        return render(request, 'home/emergency-generator.html', {'EG_add': EG_add})


@login_required(login_url="/login/")
def combustion_equipment_add(request):
    CE_add = CEform(request.POST, request.FILES)
    if request.method == "POST":
        if CE_add.is_valid():
            CE_add.save()

            return redirect('/carbon-system/')
    else:
        return render(request, 'home/combustion-equipment.html', {'CE_add': CE_add})


@login_required(login_url="/login/")
def official_car_add(request):
    OffCar_add = OFform(request.POST, request.FILES)
    if request.method == "POST":
        if OffCar_add.is_valid():
            OffCar_add.save()

            return redirect('/carbon-system/')
    else:
        return render(request, 'home/official-car.html', {'OffCar_add': OffCar_add})


@login_required(login_url="/login/")
def material_add(request):
    MT_add = MTform(request.POST, request.FILES)
    if request.method == "POST":
        if MT_add.is_valid():
            MT_add.save()

            return redirect('/carbon-system/')
    else:
        return render(request, 'home/material.html', {'MT_add': MT_add})


@login_required(login_url="/login/")
def process_add(request):
    PC_add = PCform(request.POST, request.FILES)
    if request.method == "POST":
        if PC_add.is_valid():
            PC_add.save()

            return redirect('/carbon-system/')
    else:
        return render(request, 'home/process.html', {'PC_add': PC_add})


@login_required(login_url="/login/")
def refrigerator_add(request):
    RF_add = RFform(request.POST, request.FILES)
    if request.method == "POST":
        if RF_add.is_valid():
            RF_add.save()

            return redirect('/carbon-system/')
    else:
        return render(request, 'home/refrigerator.html', {'RF_add': RF_add})


@login_required(login_url="/login/")
def airconditioner_add(request):
    AC_add = ACform(request.POST, request.FILES)
    if request.method == "POST":
        if AC_add.is_valid():
            AC_add.save()

            return redirect('/carbon-system/')
    else:
        return render(request, 'home/airconditioner.html', {'AC_add': AC_add})


@login_required(login_url="/login/")
def vehicle_add(request):
    VC_add = VCform(request.POST, request.FILES)
    if request.method == "POST":
        if VC_add.is_valid():
            VC_add.save()

            return redirect('/carbon-system/')
    else:
        return render(request, 'home/vehicle.html', {'VC_add': VC_add})


@login_required(login_url="/login/")
def water_dispenser_add(request):
    WD_add = WDform(request.POST, request.FILES)
    if request.method == "POST":
        if WD_add.is_valid():
            WD_add.save()

            return redirect('/carbon-system/')
    else:
        return render(request, 'home/water-dispenser.html', {'WD_add': WD_add})


@login_required(login_url="/login/")
def ice_water_dispenser_add(request):
    IWD_add = IWDform(request.POST, request.FILES)
    if request.method == "POST":
        if IWD_add.is_valid():
            IWD_add.save()

            return redirect('/carbon-system/')
    else:
        return render(request, 'home/ice-water-dispenser.html', {'IWD_add': IWD_add})


@login_required(login_url="/login/")
def ice_maker_add(request):
    IM_add = IMform(request.POST, request.FILES)
    if request.method == "POST":
        if IM_add.is_valid():
            IM_add.save()

            return redirect('/carbon-system/')
    else:
        return render(request, 'home/ice-maker.html', {'IM_add': IM_add})


@login_required(login_url="/login/")
def other_device_add(request):
    OD_add = ODform(request.POST, request.FILES)
    if request.method == "POST":
        if OD_add.is_valid():
            OD_add.save()

            return redirect('/carbon-system/')
    else:
        return render(request, 'home/other-device.html', {'OD_add': OD_add})


@login_required(login_url="/login/")
def extinguisher_add(request):
    EX_add = EXform(request.POST, request.FILES)
    if request.method == "POST":
        if EX_add.is_valid():
            EX_add.save()

            return redirect('/carbon-system/')
    else:
        return render(request, 'home/extinguisher.html', {'EX_add': EX_add})


@login_required(login_url="/login/")
def personnel_inventory_add(request):
    PI_add = PIform(request.POST, request.FILES)
    if request.method == "POST":
        if PI_add.is_valid():
            PI_add.save()

            return redirect('/carbon-system/')
    else:
        return render(request, 'home/personnel-inventory.html', {'PI_add': PI_add})


@login_required(login_url="/login/")
def employee_add(request):
    EMP_add = EMPform(request.POST, request.FILES)
    if request.method == "POST":
        if EMP_add.is_valid():
            EMP_add.save()

            return redirect('/carbon-system/')
    else:
        return render(request, 'home/employee.html', {'EMP_add': EMP_add})


# 廢水
@login_required(login_url="/login/")
def waste_water_add(request):
    waste_water_add = WASTEWATERform(request.POST, request.FILES)
    if request.method == "POST":
        if waste_water_add.is_valid():
            waste_water_add.save()

            return redirect('/carbon-system/')
    else:
        return render(request, 'home/waste-water.html', {'waste_water_add': waste_water_add})


# 廢汙泥
@login_required(login_url="/login/")
def waste_sludge_add(request):
    waste_sludge_add = WasteSludgeForm(request.POST, request.FILES)
    if request.method == "POST":
        if waste_sludge_add.is_valid():
            waste_sludge_add.save()

            return redirect('/carbon-system/')
    else:
        return render(request, 'home/waste-sludge.html', {'waste_sludge_add': waste_sludge_add})


# 溶劑、噴霧劑
@login_required(login_url="/login/")
def solvent_aerosol_emission_sources_add(request):
    solvent_aerosol_emission_sources_add = SolventAerosolEmissionSourcesForm(request.POST, request.FILES)
    if request.method == "POST":
        if solvent_aerosol_emission_sources_add.is_valid():
            solvent_aerosol_emission_sources_add.save()

            return redirect('/carbon-system/')
    else:
        return render(request, 'home/solvent-aerosol-emission-sources.html', {'solvent_aerosol_emission_sources_add': solvent_aerosol_emission_sources_add})


# VOCs1表單儲存
@login_required(login_url="/login/")
def VOCs_one_add(request):
    VOCs_one_add = VOCsOneForm(request.POST, request.FILES)
    if request.method == "POST":
        if VOCs_one_add.is_valid():
            VOCs_one_add.save()
            return redirect('/carbon-system/')
    else:
        return render(request, 'home/VOCs-one.html', {'VOCs_one_add': VOCs_one_add})


# VOCs2表單儲存
@login_required(login_url="/login/")
def VOCs_two_add(request):
    VOCs_two_add = VOCsTwoForm(request.POST, request.FILES)
    if request.method == "POST":
        if VOCs_two_add.is_valid():
            VOCs_two_add.save()
            return redirect('/carbon-system/')
    else:
        return render(request, 'home/VOCs-two.html', {'VOCs_two_add': VOCs_two_add})


@login_required(login_url="/login/")
def electricity_add(request):
    ELEC_add = ELECform(request.POST, request.FILES)
    if request.method == "POST":
        if ELEC_add.is_valid():
            ELEC_add.save()
            return redirect('/carbon-system/')
    else:
        return render(request, 'home/electricity.html', {'ELEC_add': ELEC_add})


@login_required(login_url="/login/")
def upstream_transportation_add(request):
    UT_add = UTform(request.POST, request.FILES)
    if request.method == "POST":
        if UT_add.is_valid():
            UT_add.save()
            return redirect('/carbon-system/')
    else:
        return render(request, 'home/upstream-transportation.html', {'UT_add': UT_add})


@login_required(login_url="/login/")
def downstream_transportation_add(request):
    DT_add = DTform(request.POST, request.FILES)
    if request.method == "POST":
        if DT_add.is_valid():
            DT_add.save()
            return redirect('/carbon-system/')
    else:
        return render(request, 'home/downstream-transportation.html', {'DT_add': DT_add})


@login_required(login_url="/login/")
def employee_commute_add(request):
    EC_add = ECform(request.POST, request.FILES)
    if request.method == "POST":
        if EC_add.is_valid():
            commute = EC_add.save()
            Commute_formSet = CommuteFormSet(request.POST, request.FILES, instance=commute)
            if Commute_formSet.is_valid():
                Commute_formSet.save()
                return redirect('/carbon-system/')
            else:
                last_data = employee_commute.objects.last()
                last_data.delete()
                print("Commute_formSet>>>>>>>>>>>>>>>>>>>>\n", Commute_formSet)
                return render(request, 'home/employee-commute.html', {'EC_add': EC_add, 'CommuteFormSet': CommuteFormSet})
    else:
        return render(request, 'home/employee-commute.html', {'EC_add': EC_add, 'CommuteFormSet': CommuteFormSet})


@login_required(login_url="/login/")
def employee_business_trip_add(request):
    EBT_add = EBTform(request.POST, request.FILES)
    if request.method == "POST":
        # print(EBT_add, "\n")
        if EBT_add.is_valid():
            business = EBT_add.save()
            tripsection_formSet = TripSectionFormSet(request.POST, request.FILES, instance=business)
            if tripsection_formSet.is_valid():
                tripsection_formSet.save()
                return redirect('/carbon-system/')
            else:
                last_data = employee_business_trip.objects.last()
                last_data.delete()
                print("tripsection_formSet表單錯誤>>>>>>>>>>>>>>>>>>>>\n", tripsection_formSet)
                return render(request, 'home/employee-business-trip.html', {'EBT_add': EBT_add, 'TripSectionFormSet': TripSectionFormSet})
    else:
        return render(request, 'home/employee-business-trip.html', {'EBT_add': EBT_add, 'TripSectionFormSet': TripSectionFormSet})


@login_required(login_url="/login/")
def waste_add(request):
    WASTE_add = WASTEform(request.POST, request.FILES)
    if request.method == "POST":
        if WASTE_add.is_valid():
            WASTE_add.save()
            return redirect('/carbon-system/')
    else:
        return render(request, 'home/waste.html', {'WASTE_add': WASTE_add})


@login_required(login_url="/login/")
def carbon_system(request):
    # data = emergency_generators.objects.filter(id=5).values("image_path", "image_note")
    # context ={
    #     'data': data,
    # }
    # return render(request, "home/carbon-system.html", context)
    return render(request, "home/carbon-system.html", locals())


# 新增轉跳
@login_required(login_url="/login/")
def add_page(request, ):
    global device_function
    if request.method == "GET":
        device_id = request.GET.get('deviceId')
        # 建立字典
        function_dic = {
            "1": emergency_generators_add(request),
            "2": combustion_equipment_add(request),
            "3": official_car_add(request),
            "4": material_add(request),
            "5": process_add(request),
            "6": refrigerator_add(request),
            "7": airconditioner_add(request),
            "8": vehicle_add(request),
            "9": water_dispenser_add(request),
            "10": ice_water_dispenser_add(request),
            "11": ice_maker_add(request),
            "12": other_device_add(request),
            "13": extinguisher_add(request),
            "14": personnel_inventory_add(request),
            "15": employee_add(request),
            "16": waste_water_add(request),
            "17": waste_sludge_add(request),
            "18": solvent_aerosol_emission_sources_add(request),
            "19": VOCs_one_add(request),
            "20": VOCs_two_add(request),
            "21": electricity_add(request),
            "22": upstream_transportation_add(request),
            "23": downstream_transportation_add(request),
            "24": employee_commute_add(request),
            "25": employee_business_trip_add(request),
            "26": waste_add(request),
        }
        if function_dic.get(device_id):
            device_function = function_dic.get(device_id)
        print("device_function:", device_function)
        return device_function


# 編輯轉跳
@login_required(login_url="/login/")
def edit_device(request):
    datasheet_id = request.GET.get('datasheet')
    single_dataID = request.GET.get('single_dataID')
    modelName = {
        "1": emergency_generators,
        "2": combustion_equipment,
        "3": official_car,
        "4": material,
        "5": process,
        "6": refrigerator,
        "7": airconditioner,
        "8": vehicle,
        "9": water_dispenser,
        "10": ice_water_dispenser,
        "11": ice_maker,
        "12": other_device,
        "13": extinguisher,
        "14": personnel_inventory,
        "15": employee,
        "16": waste_water,
        "17": waste_sludge,
        "18": solvent_aerosol_emission_sources,
        "19": VOCs_one,
        "20": VOCs_two,
        "21": electricity,
        "22": upstream_transportation,
        "23": downstream_transportation,
        "24": employee_commute,
        "25": employee_business_trip,
        "26": waste,
    }
    formlName = {
        "1": EGform, "2": CEform, "3": OFform, "4": MTform, "5": PCform,
        "6": RFform, "7": ACform, "8": VCform, "9": WDform, "10": IWDform,
        "11": IMform, "12": ODform, "13": EXform, "14": PIform, "15": EMPform,
        "16": WASTEWATERform, "17": WasteSludgeForm, "18": SolventAerosolEmissionSourcesForm,
        "19": VOCsOneForm, "20": VOCsTwoForm, "21": ELECform, "22": UTform,
        "23": DTform, "24": ECform, "25": EBTform, "26": WASTEform
    }
    formsetName = {
        "24": CommuteFormSet, "25": TripSectionFormSet
    }
    if modelName.get(datasheet_id) and formlName.get(datasheet_id):
        dbName = modelName.get(datasheet_id)
        form = formlName.get(datasheet_id)
        formset = formsetName.get(datasheet_id)
        if request.method == 'GET':
            current_data = dbName.objects.get(id=single_dataID)
            update_from = form(instance=current_data)

            formUpdata_name = {
                'form': update_from,
                'datasheet_id': datasheet_id,
                'single_dataID': single_dataID,
            }
            try:
                if datasheet_id == "24" or "25":
                    update_formset = formset(instance=current_data)
                    formUpdata_name["update_formset"] = update_formset
            except:
                pass

            # 建立字典
            htmlName = {
                "1": "home/emergency-generator-edit.html",
                "2": "home/combustion-equipment-edit.html",
                "3": "home/official-car-edit.html",
                "4": "home/material-edit.html",
                "5": "home/process-edit.html",
                "6": "home/refrigerator-edit.html",
                "7": "home/airconditioner-edit.html",
                "8": "home/vehicle-edit.html",
                "9": "home/water-dispenser-edit.html",
                "10": "home/ice-water-dispenser-edit.html",
                "11": "home/ice-maker-edit.html",
                "12": "home/other-device-edit.html",
                "13": "home/extinguisher-edit.html",
                "14": "home/personnel-inventory-edit.html",
                "15": "home/employee-edit.html",
                "16": "home/waste-water-edit.html",
                "17": "home/waste-sludge-edit.html",
                "18": "home/solvent-aerosol-emission-sources-edit.html",
                "19": "home/VOCs-one-edit.html",
                "20": "home/VOCs-two-edit.html",
                "21": "home/electricity-edit.html",
                "22": "home/upstream-transportation-edit.html",
                "23": "home/downstream-transportation-edit.html",
                "24": "home/employee-commute-edit.html",
                "25": "home/employee-business-trip-edit.html",
                "26": "home/waste-edit.html",
            }
            if htmlName.get(datasheet_id):
                EditDevice_page = htmlName.get(datasheet_id)
                return render(request, EditDevice_page, formUpdata_name)


# 儲存更新後的資料
@login_required(login_url="/login/")
def update_device(request, datasheet_id, single_dataID):
    modelName = {
        "1": emergency_generators,
        "2": combustion_equipment,
        "3": official_car,
        "4": material,
        "5": process,
        "6": refrigerator,
        "7": airconditioner,
        "8": vehicle,
        "9": water_dispenser,
        "10": ice_water_dispenser,
        "11": ice_maker,
        "12": other_device,
        "13": extinguisher,
        "14": personnel_inventory,
        "15": employee,
        "16": waste_water,
        "17": waste_sludge,
        "18": solvent_aerosol_emission_sources,
        "19": VOCs_one,
        "20": VOCs_two,
        "21": electricity,
        "22": upstream_transportation,
        "23": downstream_transportation,
        "24": employee_commute,
        "25": employee_business_trip,
        "26": waste,
    }
    formName = {
        "1": EGform, "2": CEform, "3": OFform, "4": MTform, "5": PCform,
        "6": RFform, "7": ACform, "8": VCform, "9": WDform, "10": IWDform,
        "11": IMform, "12": ODform, "13": EXform, "14": PIform, "15": EMPform,
        "16": WASTEWATERform, "17": WasteSludgeForm, "18": SolventAerosolEmissionSourcesForm,
        "19": VOCsOneForm, "20": VOCsTwoForm, "21": ELECform, "22": UTform,
        "23": DTform, "24": ECform, "25": EBTform, "26": WASTEform
    }
    if modelName.get(datasheet_id) and formName.get(datasheet_id):
        dbName = modelName.get(datasheet_id)
        form = formName.get(datasheet_id)
        current_data = get_object_or_404(dbName, id=datasheet_id)
        # current_data = dbName.objects.get(id=single_dataID)
        print("current_data>>>>>>>>", current_data)
        if request.method == 'POST':
            # current_data = dbName.objects.get(id=single_dataID)
            update_from = form(request.POST, request.FILES, instance=current_data)
            # update_formset_trip = TripSectionFormSet(request.POST, request.FILES, instance=current_data)
            # print("update_from>>>>>>>>", update_from)
            # print("update_formset_trip>>>>>>>>", update_formset_trip)

            # if update_from.is_valid() and update_formset_trip.is_valid():
            #     print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            #     business = update_from.save()
            #     update_formset_trip.save()

            if update_from.is_valid():
                print("ok")
                business = update_from.save()
                update_formset_trip = TripSectionFormSet(request.POST, request.FILES, instance=business)
                # update_formset_trip = TripSectionFormSet(request.POST, request.FILES, instance=business)
                print("update_from>>>>>>>>>>>>>>>>>>>>>save")
                if update_formset_trip.is_valid():
                    update_formset_trip.save()
                    # print("formset_trip>>>>>>>>>>>>>>>>>>>save")
                #         return redirect('/carbon-system/', locals())
                #     return redirect('/carbon-system/', locals())
                    print("update_formset_trip>>>>>>>>>>>>>>>>>>>>>save")
                    return redirect('/carbon-system/', locals())
                else:
                    print("\n", update_formset_trip.errors)
                    # print("update_formset_trip>>>>>>>>錯誤\n", update_formset_trip)

        else:
            return render(request, 'home/index.html', locals())


# 刪除資料
@login_required(login_url="/login/")
def delete_device(request):
    if request.method == 'GET':
        datasheet_id = request.GET.get('datasheet_id')
        single_dataID = request.GET.get('single_dataID')
        modelName = {
            "1": emergency_generators,
            "2": combustion_equipment,
            "3": official_car,
            "4": material,
            "5": process,
            "6": refrigerator,
            "7": airconditioner,
            "8": vehicle,
            "9": water_dispenser,
            "10": ice_water_dispenser,
            "11": ice_maker,
            "12": other_device,
            "13": extinguisher,
            "14": personnel_inventory,
            "15": employee,
            "16": waste_water,
            "17": waste_sludge,
            "18": solvent_aerosol_emission_sources,
            "19": VOCs_one,
            "20": VOCs_two,
            "21": electricity,
            "22": upstream_transportation,
            "23": downstream_transportation,
            "24": employee_commute,
            "25": employee_business_trip,
            "26": waste,
        }
        if modelName.get(datasheet_id):
            dbName = modelName.get(datasheet_id)
            current_data = dbName.objects.get(id=single_dataID)
            current_data.delete()  # 刪除該筆資料
            # print("current_data::::::::::::::::::::::::", current_data)
            return JsonResponse(single_dataID, safe=False)


# 新增title
@login_required(login_url="/login/")
def add_title(request):
    if request.method == 'GET':
        device_id = request.GET.get('deviceId', None)
        # 選擇title要顯示的欄位
        htmlName = {
            "1": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "年度", "設備編號", "容量(𝓁)", "地點", "部門"],
                "加油量(單位:𝓁)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "合計"]
            },

            "2": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "年度", "名稱", "編號", "燃料種類"],
                "使用量": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "合計"],
                "熱值(Kcal/kg)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "平均"]
            },

            "3": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "年度", "類別", "編號", "燃料種類", "所屬單位", "計程方式"],
                "耗用量(單位:油車𝓁/電車kWh/公里數km)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "合計"],
                "尿素添加量(𝓁)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "合計"]
            },

            "4": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "年度", "原物料號", "原/物料", "名稱"],
                "是否為化學品": ["化學品名稱", "化學品名", "化學式"],
                "月用量(單位:公噸)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
            },

            "5": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "年度", "製程階段", "料號", "製程添加物", "化學品名", "化學式", "CAS NO", "是否燃燒", "VOCs"],
                "使用量(單位:公斤)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "總計", "使用量單位"]
            },
            # 冷媒(6~13)
            "6": {
                "編輯區": ["刪除", "修改"],
                "冰箱清單": ["序號", "年度", "編號", "名稱", "品牌", "型號", "位置", "規格填充量", "冷媒類型", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "7": {
                "編輯區": ["刪除", "修改"],
                "冷氣機清單": ["序號", "年度", "編號", "名稱", "品牌", "型號", "位置", "規格填充量", "冷媒類型", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "8": {
                "編輯區": ["刪除", "修改"],
                "車輛清單": ["序號", "年度", "編號", "名稱", "品牌", "型號", "位置", "規格填充量", "冷媒類型", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "9": {
                "編輯區": ["刪除", "修改"],
                "飲水機清單": ["序號", "年度", "編號", "名稱", "品牌", "型號", "位置", "規格填充量", "冷媒類型", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "10": {
                "編輯區": ["刪除", "修改"],
                "冰水機清單": ["序號", "年度", "編號", "名稱", "品牌", "型號", "位置", "規格填充量", "冷媒類型", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "11": {
                "編輯區": ["刪除", "修改"],
                "製冰機清單": ["序號", "年度", "編號", "名稱", "品牌", "型號", "位置", "規格填充量", "冷媒類型", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "12": {
                "編輯區": ["刪除", "修改"],
                "其他設備": ["序號", "年度", "編號", "名稱", "品牌", "型號", "位置", "規格填充量", "冷媒類型", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "13": {
                "編輯區": ["刪除", "修改"],
                "滅火器清單": ["序號", "年度", "滅火器名稱", "類型", "設備編號", "擺放位置(廠別)", "廠商", "藥劑重量(單位:kg)", "庫存量", "使用量數量", "使用月份", "更換/填充量", "更換/填充日期"]
            },

            "14": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "年度", "員工總數"],
                "時數": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
                "人數": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
            },

            "15": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "年度", "人員類別"],
                "員工人數": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
                "當月工作天數": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
                "每日工作時數": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
            },

            "16": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "年度", "廢水厭氧處理單元名稱 ", "廢水進流量(立方公尺/年)", "平均進流COD濃度(mg/L)", "平均進流COD濃度(mg/L)", u"CH\u2084捕集系統捕集率", "燃燒設備效率"],
            },

            "17": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "年度", "廢棄污泥厭氧處理單元名稱", "污泥進流量(立方公尺/年)", "平均進流MLSS濃度(mg/L)", u"CH\u2084捕集系統捕集率", "燃燒設備效率"],
            },

            "18": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "年度", "使用物種", "逸散 / 補充量(公噸/年)", "全球暖化潛勢(GWP-AR6)"],
            },

            "19": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "年度", "VOCs排放量(千立方公尺/年)", u"CH\u2084濃度(ppm)"],
            },

            "20": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "年度", "VOCs排放量(千立方公尺/年)", u'CH\u2084濃度', "VOCs設備補集率", "燃燒設備效率"],
                "VOCs濃度": ["入口濃度", "出口濃度"],
                u"CO\u2082排放係數": ["內設值", "自訂值"],
            },

            "21": {
                "編輯區": ["刪除", "修改"],
                "用電量": ["序號", "年度", "電表編號", "地址", "一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "小計(度)", "總計(千度)"]
            },

            "22": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "單號", "商品", "淨/毛重", "重量(噸)", "組織使用產品", "客戶", "供應商名稱", "供應商地址", "貿易條件", "接貨地點", "送貨地點"],
                "陸運": ["單趟運輸距離(km)", "運輸國家", "交通工具", "燃料", "支付方", "趟次"],
                "海運": ["海運距離(nm)", "出貨港口", "到達港口", "支付方", "趟次"],
                "陸運(特殊)": ["單趟運輸距離(km)", "運輸國家", "交通工具", "燃料", "支付方", "趟次"],
                "空運": ["單趟運輸距離(km)", "出貨機場", "到達機場", "支付方", "趟次"]
            },

            "23": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "單號", "商品", "淨/毛重", "重量(噸)", "客戶", "供應商名稱", "供應商地址", "貿易條件", "接貨地點", "送貨地點"],
                "陸運": ["單趟運輸距離(km)", "運輸國家", "交通工具", "燃料", "支付方", "趟次"],
                "海運": ["海運距離(nm)", "出貨港口", "到達港口", "支付方", "趟次"],
                "陸運(特殊)": ["單趟運輸距離(km)", "運輸國家", "交通工具", "燃料", "支付方", "趟次"],
                "空運": ["單趟運輸距離(km)", "出貨機場", "到達機場", "支付方", "趟次"]
            },

            "24": {
                "編輯區": ["刪除", "修改"],
                "員工通勤清冊": ["序號", "年度", "編號", "部門", "姓名", "交通方式", "居住城市", "鄉鎮市區", "行政區公家機關地址", "至公司距離(km)", "年工作天數", "距離合計"],
            },

            # 員工出差
            "25": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "出差單號", "員工編號", "部門", "姓名", "出差地點", "啟程日期"],
                "距離(pkm)": ["自駕汽車", "高鐵", "火車", "計程車", "機車", "捷運", "飛機", "船舶"],
            },

            "26": {
                "編輯區": ["刪除", "修改"],
                "廢棄物處理": ["序號", "名稱", "重量(噸)", "運送時間", "處置地點", "處理方式", "處理廠商名稱", "運輸方式", "運輸燃料", "運輸距離(km)", "T*km"],
            },
        }
        title = [htmlName.get(device_id)]
        return JsonResponse(title, safe=False)


def chemical_dropdowm(request):
    chemical_add = list(chemical_table.objects.values("chemical_add"))
    return JsonResponse(chemical_add, safe=False)


def load_chemical(request):
    chemical_add = request.GET.get("add_ch_name")
    chemical_data = list(chemical_table.objects.filter(chemical_add=chemical_add).values("chemical_name", "chemical_formula"))
    return JsonResponse(chemical_data, safe=False)

# def export_data(request):
#     if request.method == 'POST':
#         # Get selected option from form
#         file_format = request.POST['file-format']
#         emergency_generators_resource = EGResource()
#         dataset = emergency_generators_resource.export()
#         if file_format == 'CSV':
#             response = HttpResponse(dataset.csv, content_type='text/csv')
#             response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
#             return response
#         elif file_format == 'JSON':
#             response = HttpResponse(dataset.json, content_type='application/json')
#             response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
#             return response
#         elif file_format == 'XLS (Excel)':
#             response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
#             response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
#             return response
#
#     return redirect('/carbon-system/')
