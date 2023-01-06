# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from json import dumps

import pandas as pd
from django import template
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
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
            elif a["d_name"] == "冷媒總表":
                t_data = []
                raw_data = refrigerant_total_table.objects.values("id", "years", "device_id", "device_name", "brand_name", "model_type",
                                                                  "position", "filling_volume", "refrigerant_type", "filling_fix_volume",
                                                                  "effusion_rate")
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
                    extinguisher.objects.values("id", "device_id", "position", "extinguisher_name",
                                                "extinguisher_type", "extinguisher_vendor", "chemical_spec", "chemical_weight", "inventory", "using_date", "using_amount", "replace_filling_date", "replace_filling_amount"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "人天清冊":
                t_data = []
                # 將要運算的值分別撈出(員工數/每日工時/每月工作天數/加班+補休時數/請假時數/休假時數)
                raw_data = personnel_inventory.objects.values("id", "years", "monthly", "employee_number", "daily_hours",
                                                              "working_days", "overtime", "leave_hours",
                                                              "day_off_hours")
                for i in range(raw_data.count()):
                    # 計算單筆當月總工作時數
                    TotalWorkingHour_M = raw_data[i].get("employee_number") * raw_data[i].get("daily_hours") * raw_data[i].get("working_days") \
                                         + raw_data[i].get("overtime") - raw_data[i].get("leave_hours") - raw_data[i].get("day_off_hours")
                    # print("TotalWorkingHour_M::::::::::::::::::::::::::::::::::::::::", TotalWorkingHour_M)
                    # 計算單筆當月總工作人天
                    TotalWorkingDay_M = TotalWorkingHour_M / raw_data[i].get("daily_hours")
                    # print("TotalWorkingHour_M::::::::::::::::::::::::::::::::::::::::", TotalWorkingHour_M)
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    single_data["TotalWorkingHour_M"] = TotalWorkingHour_M
                    single_data["TotalWorkingDay_M"] = round(TotalWorkingDay_M, 4)
                    # print("single_data::::::::::::::::::::::::::::::::::::::::", single_data)
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "保全清單":
                t_data = []
                # 將要運算的值分別撈出(員工數/每日工時/每月工作天數/加班+補休時數/請假時數/休假時數)
                raw_data = security.objects.values("id", "years", "monthly", "security_number", "daily_hours", "working_days")
                # "working_days", "total_working_hours", "total_working_day")
                for i in range(raw_data.count()):
                    # 計算單筆當月總工作時數
                    TotalWorkingHour_M = raw_data[i].get("security_number") * raw_data[i].get("daily_hours") * raw_data[i].get("working_days")
                    # print("TotalWorkingHour_M::::::::::::::::::::::::::::::::::::::::", TotalWorkingHour_M)
                    # 計算單筆當月總工作人天
                    TotalWorkingDay_M = TotalWorkingHour_M / raw_data[i].get("daily_hours")
                    # print("TotalWorkingHour_M::::::::::::::::::::::::::::::::::::::::", TotalWorkingHour_M)
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    single_data["TotalWorkingHour_M"] = TotalWorkingHour_M
                    single_data["TotalWorkingDay_M"] = round(TotalWorkingDay_M, 4)
                    # print("single_data::::::::::::::::::::::::::::::::::::::::", single_data)
                    t_data.append(single_data)
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
                    upstream_transportation.objects.values("acceptance_receipt", "commodity_name", "commodity_NW",
                                                           "customer", "supplier", "supplier_address",
                                                           "trade_term", "receiving_address", "delivery_address", "transport_distance",
                                                           "transport_country", "transport_type", "vehicle_fuel", "trips",
                                                           "overseas_transport_type", "overseas_vehicle_fuel", "overseas_transport_distance", "overseas_trips",
                                                           "special_transport_distance", "special_transport_country", "special_transport_type", "special_vehicle_fuel", "special_trips"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "下游運輸":
                t_data = list(
                    downstream_transportation.objects.values("device_id", "period_starttime", "period_endtime",
                                                             "device_capacity", "position", "department",
                                                             "january", "february", "march", "april",
                                                             "may", "june", "july", "august",
                                                             "september", "october", "november", "december"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "員工通勤":
                t_data = []
                # 將要運算的值分別撈出(員工數/每日工時/每月工作天數/加班+補休時數/請假時數/休假時數)
                raw_data = employee_commute.objects.values("id", "employee_id", "department", "employee_name",
                                                           "transportation", "displacement", "city",
                                                           "township", "address", "commute_distance", "work_days")
                for i in range(raw_data.count()):
                    # 計算單筆距離合計
                    total_distance = raw_data[i].get("commute_distance") * raw_data[i].get("work_days") * 2
                    # print("total_distance::::::::::::::::::::::::::::::::::::::::", total_distance)
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    single_data["total_distance"] = total_distance
                    # print("single_data::::::::::::::::::::::::::::::::::::::::", single_data)
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "員工出差":
                t_data = list(
                    employee_business_trip.objects.values("id", "employee_id", "department", "employee_name",
                                                          "business_trip_location", "business_trip_date", "transportation",
                                                          "departure", "destination", "round_trip_distance"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "廢棄物":
                t_data = []
                # 將要運算的值分別撈出(員工數/每日工時/每月工作天數/加班+補休時數/請假時數/休假時數)
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


@login_required(login_url="/login/")
def emergency_generators_add(request):
    if request.method == "POST":
        EG_add = EGform(request.POST, request.FILES)
        if EG_add.is_valid():
            EG_add.save()
            return redirect('/carbon-system/')
    else:
        return redirect('/emergency_generator_add/')


@login_required(login_url="/login/")
def combustion_equipment_add(request):
    if request.method == "POST":
        CE_add = CEform(request.POST, request.FILES)
        if CE_add.is_valid():
            CE_add.save()

            return redirect('/carbon-system/')

    else:

        return redirect('/combustion_equipment_add/')


@login_required(login_url="/login/")
def official_car_add(request):
    if request.method == "POST":
        OffCar_add = OFform(request.POST, request.FILES)
        if OffCar_add.is_valid():
            OffCar_add.save()

            return redirect('/carbon-system/')

    else:

        return redirect('/official_car_add/')


@login_required(login_url="/login/")
def material_add(request):
    if request.method == "POST":
        MT_add = MTform(request.POST, request.FILES)
        if MT_add.is_valid():
            MT_add.save()

            return redirect('/carbon-system/')

    else:

        return redirect('/material_add/')


@login_required(login_url="/login/")
def process_add(request):
    if request.method == "POST":
        PC_add = PCform(request.POST, request.FILES)
        if PC_add.is_valid():
            PC_add.save()

            return redirect('/carbon-system/')

    else:

        return redirect('/material_add/')


@login_required(login_url="/login/")
def refrigerator_add(request):
    if request.method == "POST":
        RF_add = RFform(request.POST, request.FILES)
        if RF_add.is_valid():
            RF_add.save()

            return redirect('/carbon-system/')

    else:

        return redirect('/refrigerator_add/')


@login_required(login_url="/login/")
def airconditioner_add(request):
    if request.method == "POST":
        AC_add = ACform(request.POST, request.FILES)
        if AC_add.is_valid():
            AC_add.save()

            return redirect('/carbon-system/')

    else:

        return redirect('/airconditioner_add/')


@login_required(login_url="/login/")
def vehicle_add(request):
    if request.method == "POST":
        VC_add = VCform(request.POST, request.FILES)
        if VC_add.is_valid():
            VC_add.save()

            return redirect('/carbon-system/')

    else:

        return redirect('/vehicle_add/')


@login_required(login_url="/login/")
def water_dispenser_add(request):
    if request.method == "POST":
        WD_add = WDform(request.POST, request.FILES)
        if WD_add.is_valid():
            WD_add.save()

            return redirect('/carbon-system/')

    else:

        return redirect('/water_dispenser_add/')


@login_required(login_url="/login/")
def ice_water_dispenser_add(request):
    if request.method == "POST":
        IWD_add = IWDform(request.POST, request.FILES)
        if IWD_add.is_valid():
            IWD_add.save()

            return redirect('/carbon-system/')

    else:

        return redirect('/ice_water_dispenser_add/')


@login_required(login_url="/login/")
def ice_maker_add(request):
    if request.method == "POST":
        IM_add = IMform(request.POST, request.FILES)
        if IM_add.is_valid():
            IM_add.save()

            return redirect('/carbon-system/')

    else:

        return redirect('/ice_maker_add/')


@login_required(login_url="/login/")
def other_device_add(request):
    if request.method == "POST":
        OD_add = ODform(request.POST, request.FILES)
        if OD_add.is_valid():
            OD_add.save()

            return redirect('/carbon-system/')

    else:

        return redirect('/other_device_add/')


@login_required(login_url="/login/")
def refrigerant_total_table_add(request):
    if request.method == "POST":
        RTT_add = RTTform(request.POST, request.FILES)
        if RTT_add.is_valid():
            RTT_add.save()

            return redirect('/carbon-system/')

    else:

        return redirect('/refrigerant_total_table_add/')


@login_required(login_url="/login/")
def extinguisher_add(request):
    if request.method == "POST":
        EX_add = EXform(request.POST, request.FILES)
        if EX_add.is_valid():
            EX_add.save()

            return redirect('/carbon-system/')

    else:

        return redirect('/extinguisher_add/')


@login_required(login_url="/login/")
def personnel_inventory_add(request):
    if request.method == "POST":
        PI_add = PIform(request.POST, request.FILES)
        if PI_add.is_valid():
            PI_add.save()

            return redirect('/carbon-system/')

    else:

        return redirect('/personnel_inventory_add/')


@login_required(login_url="/login/")
def security_add(request):
    if request.method == "POST":
        SC_add = SCform(request.POST, request.FILES)
        if SC_add.is_valid():
            SC_add.save()

            return redirect('/carbon-system/')

    else:

        return redirect('/security_add/')


@login_required(login_url="/login/")
def electricity_add(request):
    if request.method == "POST":
        ELEC_add = ELECform(request.POST, request.FILES)
        if ELEC_add.is_valid():
            ELEC_add.save()

            return redirect('/carbon-system/')

    else:

        return redirect('/electricity_add/')


@login_required(login_url="/login/")
def upstream_transportation_add(request):
    if request.method == "POST":
        UT_add = UTform(request.POST, request.FILES)
        if UT_add.is_valid():
            UT_add.save()

            return redirect('/carbon-system/')

    else:

        return redirect('/upstream_transportation_add/')


@login_required(login_url="/login/")
def downstream_transportation_add(request):
    if request.method == "POST":
        DT_add = DTform(request.POST, request.FILES)
        if DT_add.is_valid():
            DT_add.save()

            return redirect('/carbon-system/')

    else:

        return redirect('/downstream_transportation_add/')


@login_required(login_url="/login/")
def employee_commute_add(request):
    if request.method == "POST":
        EC_add = ECform(request.POST, request.FILES)
        if EC_add.is_valid():
            EC_add.save()

            return redirect('/carbon-system/')

    else:

        return redirect('/employee_commute_add/')


@login_required(login_url="/login/")
def employee_business_trip_add(request):
    if request.method == "POST":
        EBT_add = EBTform(request.POST, request.FILES)
        if EBT_add.is_valid():
            EBT_add.save()

            return redirect('/carbon-system/')

    else:

        return redirect('/employee_business_trip_add/')


@login_required(login_url="/login/")
def waste_add(request):
    if request.method == "POST":
        WASTE_add = WASTEform(request.POST, request.FILES)
        if WASTE_add.is_valid():
            WASTE_add.save()

            return redirect('/carbon-system/')

    else:

        return redirect('/waste_add/')


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
def add_page(request):
    global NewDevice_page
    if request.method == "GET":
        device_id = request.GET.get('deviceId')
        # 建立字典
        htmlName = {
            "1": "home/emergency-generator.html",
            "2": "home/combustion-equipment.html",
            "3": "home/official-car.html",
            "4": "home/material.html",
            "5": "home/process.html",
            "6": "home/refrigerator.html",
            "7": "home/airconditioner.html",
            "8": "home/vehicle.html",
            "9": "home/water-dispenser.html",
            "10": "home/ice-water-dispenser.html",
            "11": "home/ice-maker.html",
            "12": "home/other-device.html",
            "13": "home/refrigerant-total-table.html",
            "14": "home/extinguisher.html",
            "15": "home/personnel-inventory.html",
            "16": "home/security.html",
            "17": "home/electricity.html",
            "18": "home/upstream-transportation.html",
            "19": "home/downstream-transportation.html",
            "20": "home/employee-commute.html",
            "21": "home/employee-business-trip.html",
            "22": "home/waste.html"
        }

        EG_add = EGform(request.POST)
        CE_add = CEform(request.POST)
        OffCar_add = OFform(request.POST)
        MT_add = MTform(request.POST)
        PC_add = PCform(request.POST)
        RF_add = RFform(request.POST)
        AC_add = ACform(request.POST)
        VC_add = VCform(request.POST)
        WD_add = WDform(request.POST)
        IWD_add = IWDform(request.POST)
        IM_add = IMform(request.POST)
        OD_add = ODform(request.POST)
        RTT_add = RTTform(request.POST)
        EX_add = EXform(request.POST)
        PI_add = PIform(request.POST)
        SC_add = SCform(request.POST)
        ELEC_add = ELECform(request.POST)
        UT_add = UTform(request.POST)
        DT_add = DTform(request.POST)
        EC_add = ECform(request.POST)
        EBT_add = EBTform(request.POST)
        WASTE_add = WASTEform(request.POST)

        if htmlName.get(device_id):
            NewDevice_page = htmlName.get(device_id)
        # print("NewDevice_page:", NewDevice_page)
    if request.method == "GET":
        return render(request, NewDevice_page, locals())


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
        "13": refrigerant_total_table,
        "14": extinguisher,
        "15": personnel_inventory,
        "16": security,
        "17": electricity,
        "18": upstream_transportation,
        "19": downstream_transportation,
        "20": employee_commute,
        "21": employee_business_trip,
        "22": waste
    }
    formlName = {
        "1": EGform, "2": CEform, "3": OFform, "4": MTform, "5": PCform,
        "6": RFform, "7": ACform, "8": VCform, "9": WDform, "10": IWDform,
        "11": IMform, "12": ODform, "13": RTTform, "14": EXform, "15": PIform,
        "16": SCform, "17": ELECform, "18": UTform, "19": DTform, "20": ECform,
        "21": EBTform, "22": WASTEform
    }
    if modelName.get(datasheet_id) and formlName.get(datasheet_id):
        dbName = modelName.get(datasheet_id)
        form = formlName.get(datasheet_id)
        if request.method == 'GET':
            current_data = dbName.objects.get(id=single_dataID)
            update_from = form(instance=current_data)

            formUpdata_name = {
                'form': update_from,
                'datasheet_id': datasheet_id,
                'single_dataID': single_dataID
            }
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
                "13": "home/refrigerant-total-table-edit.html",
                "14": "home/extinguisher-edit.html",
                "15": "home/personnel-inventory-edit.html",
                "16": "home/security-edit.html",
                "17": "home/electricity-edit.html",
                "18": "home/upstream-transportation-edit.html",
                "19": "home/downstream-transportation-edit.html",
                "20": "home/employee-commute-edit.html",
                "21": "home/employee-business-trip-edit.html",
                "22": "home/waste-edit.html"
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
        "13": refrigerant_total_table,
        "14": extinguisher,
        "15": personnel_inventory,
        "16": security,
        "17": electricity,
        "18": upstream_transportation,
        "19": downstream_transportation,
        "20": employee_commute,
        "21": employee_business_trip,
        "22": waste
    }
    formName = {
        "1": EGform, "2": CEform, "3": OFform, "4": MTform, "5": PCform,
        "6": RFform, "7": ACform, "8": VCform, "9": WDform, "10": IWDform,
        "11": IMform, "12": ODform, "13": RTTform, "14": EXform, "15": PIform,
        "16": SCform, "17": ELECform, "18": UTform, "19": DTform, "20": ECform,
        "21": EBTform, "22": WASTEform
    }
    if modelName.get(datasheet_id) and formName.get(datasheet_id):
        dbName = modelName.get(datasheet_id)
        form = formName.get(datasheet_id)
        if request.method == 'POST':
            current_data = dbName.objects.get(id=single_dataID)
            update_from = form(request.POST, request.FILES, instance=current_data)
            if update_from.is_valid():
                print("yyyyyyyyyyyyyy")
                update_from.save()
                return redirect('/carbon-system/', locals())
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
            "13": refrigerant_total_table,
            "14": extinguisher,
            "15": personnel_inventory,
            "16": security,
            "17": electricity,
            "18": upstream_transportation,
            "19": downstream_transportation,
            "20": employee_commute,
            "21": employee_business_trip,
            "22": waste
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
                "冷媒總表": ["序號", "年度", "編號", "名稱", "品牌", "型號", "位置", "規格填充量", "冷媒類型", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "14": {
                "編輯區": ["刪除", "修改"],
                "滅火器清單": ["序號", "編號", "位置", "名稱", "類型", "廠商", "藥劑規格(單位:磅)", "藥劑重量(單位:kg)", "庫存量", "使用日期", "使用量", "更換/填充日期", "更換/填充量"]
            },

            "15": {
                "編輯區": ["刪除", "修改"],
                "人天清冊": ["序號", "年份", "月份", "員工數", "每日工時", "每月工作天數", "加班+補修時數", "請假時數", "休假時數", "當月總工時", "當月總工作人天"]
            },

            "16": {
                "編輯區": ["刪除", "修改"],
                "保全清冊": ["序號", "年份", "月份", "保全人數", "每日工時", "每月工作天數", "當月工時", "當月工作人天"]
            },

            "17": {
                "編輯區": ["刪除", "修改"],
                "用電量": ["序號", "年度", "電表編號", "地址", "一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "小計(度)", "總計(千度)"]
            },

            "18": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "驗收單號", "商品", "淨重量(單位:噸)", "客戶", "供應商名稱", "供應商地址", "貿易條件", "接貨地點", "送貨地點"],
                "陸運": ["單趟運輸距離(km)", "運輸國家", "方式", "燃料", "趟次", "T*km"],
                "海運": ["出貨港口", "到達港口", "海運距離", "趟次", "T*km"],
                "陸運(特殊)": ["單趟運輸距離(km)", "運輸國家", "方式", "燃料", "趟次", "T*km"]
            },

            "19": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "驗收單號", "商品", "淨重量(單位:噸)", "客戶", "供應商名稱", "供應商地址", "貿易條件", "接貨地點", "送貨地點"],
                "陸運": ["單趟運輸距離(km)", "運輸國家", "方式", "燃料", "趟次", "T*km"],
                "海運": ["出貨港口", "到達港口", "海運距離", "趟次", "T*km"],
                "陸運(特殊)": ["單趟運輸距離(km)", "運輸國家", "方式", "燃料", "趟次", "T*km"]
            },

            "20": {
                "編輯區": ["刪除", "修改"],
                "員工通勤清冊": ["序號", "編號", "部門", "姓名", "交通方式", "排氣量(CC數)", "居住城市", "鄉鎮市區", "行政區公家機關地址", "至公司距離(km)", "年工作天數", "距離合計"],
            },

            "21": {
                "編輯區": ["刪除", "修改"],
                "員工出差清冊": ["序號", "編號", "部門", "姓名", "出差地點", "出差日期", "交通方式", "出發地", "目的地", "來回距離(pkm)"],
            },

            "22": {
                "編輯區": ["刪除", "修改"],
                "廢棄物處理": ["序號", "名稱", "重量(噸)", "運送時間", "處置地點", "處理方式", "處理廠商名稱", "運輸方式", "運輸燃料", "運輸距離(km)", "T*km"],
            }
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
