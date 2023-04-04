# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import json
import os.path
from json import dumps

import django.contrib.auth.models
import pandas as pd
from django import template
from django.contrib.auth.decorators import login_required, permission_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.urls import reverse, reverse_lazy
from decimal import *
from django.utils.datastructures import MultiValueDictKeyError
from django.db import models
from django.db.models import Count, Sum, F, Value, Subquery, CharField
from datetime import datetime
import apps
from .forms import *
from apps.home.models import *


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    # dropdown = {
    #     'dropdown_one': "dropdown_one",
    #     'dropdown_two': "dropdown_two",
    #     'dropdown_three': "dropdown_three",
    # }
    # request.session.update(dropdown)
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


# 判斷目前使用者在哪個group
def current_user_group_id(request):
    groups_query = request.user.groups.values("id")
    for groups in groups_query:
        company_id = groups["id"]
        return company_id


# 抓欄位(
@login_required(login_url="/login/")
def load_table(request):
    global consumption_data
    if request.method == 'GET':
        device_id = request.GET.get('deviceId')
        company_value = request.GET.get('company_value')
        year = request.GET.get('yearInput')
        if company_value is None:
            company_id = current_user_group_id(request)
        else:
            company_id = int(company_value)
        t_name = list(section_two.objects.filter(did=device_id).values("d_name"))
        # 四捨五入小數點第四位
        getcontext().prec = 4
        # print("888888888", t_name)
        # 從db撈每張表要顯示的值
        for a in t_name:
            if a["d_name"] == "柴油發電機":
                t_data = []
                raw_data = emergency_generators.objects.filter(company_id=company_id, years=year).values("id", "device_id", "device_capacity", "position",
                                                                                                         "department", "estimate",
                                                                                                         "january", "february", "march", "april",
                                                                                                         "may", "june", "july", "august",
                                                                                                         "september", "october", "november", "december")
                # 計算加油量合計
                for i in range(raw_data.count()):
                    single_data = {}
                    consumption_total = raw_data[i].get("january") + raw_data[i].get("february") + raw_data[i].get("march") + raw_data[i].get("april") + \
                                        raw_data[i].get("may") + raw_data[i].get("june") + raw_data[i].get("july") + raw_data[i].get("august") + \
                                        raw_data[i].get("september") + raw_data[i].get("october") + raw_data[i].get("november") + raw_data[i].get("december")
                    # 抓單筆資料
                    single_data.update(raw_data[i])
                    # 將計算後的加油量丟回字典
                    single_data["total"] = consumption_total
                    # 將 estimate 替換成中文
                    single_data["estimate"] = "是" if single_data["estimate"] else "否"
                    t_data.append(single_data)

                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "燃燒設備":
                t_data = []
                # 「合計」前後的資料分開
                raw_data = combustion_equipment.objects.filter(company_id=company_id, years=year).values("id", "device_name", "device_id", "fuel_type",
                                                                                                         "fuel_january", "fuel_february", "fuel_march", "fuel_april", "fuel_may", "fuel_june",
                                                                                                         "fuel_july", "fuel_august", "fuel_september", "fuel_october", "fuel_november", "fuel_december")
                heat_data = combustion_equipment.objects.filter(company_id=company_id, years=year).values("heat_january", "heat_february", "heat_march", "heat_april", "heat_may", "heat_june",
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
                    # print("Total_fuel", Total_fuel)
                    # 將計算後的「合計」丟回字典
                    single_data["Total_fuel"] = '%.4f' % Total_fuel
                    for j in heat_data[i]:
                        # 「合計」後的資料(每月熱值)丟回字典
                        single_data[j] = heat_data[i].get(j)
                    # 將計算後的「平均熱值」丟回字典
                    # single_data["avg_heat"] = round(avg_heat, 4)
                    single_data["avg_heat"] = '%.4f' % avg_heat
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "公務車":
                t_data = []
                # 「合計」前後的資料分開抓
                raw_data = official_car.objects.filter(company_id=company_id, years=year).values("id", "vehicle_type", "device_id", "fuel_type", "department", "metering_method")
                consumptions_data = official_car.objects.filter(company_id=company_id, years=year).values("january", "february", "march", "april", "may", "june", "july", "august",
                                                                                                          "september", "october", "november", "december")

                urea_data = official_car.objects.filter(company_id=company_id, years=year).values("urea_january", "urea_february", "urea_march", "urea_april",
                                                                                                  "urea_may", "urea_june", "urea_july", "urea_august",
                                                                                                  "urea_september", "urea_october", "urea_november", "urea_december")
                # 計算耗用量合計
                for i in range(raw_data.count()):
                    single_data = raw_data[i]
                    consumption_total = 0
                    for j in consumptions_data[i]:
                        # print("oil:::", consumptions_data[i].get(j))
                        # 「逐一」將資料(耗用量)丟回字典
                        single_data[j] = consumptions_data[i].get(j)
                        consumption_total += consumptions_data[i].get(j)
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
                    material.objects.filter(company_id=company_id, years=year).values("id", "material_id", "material_type", "material_name",
                                                                                      "process_add_name", "chemical_name", "chemical_formula",
                                                                                      "january", "february", "march", "april",
                                                                                      "may", "june", "july", "august",
                                                                                      "september", "october", "november", "december"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "製程添加化學品":
                t_data = []
                raw_data = process.objects.filter(company_id=company_id, years=year).values("id", "process_stage", "material_id", "process_add_name",
                                                                                            "carbon_content", "burn", "VOCs",
                                                                                            "january", "february", "march", "april",
                                                                                            "may", "june", "july", "august",
                                                                                            "september", "october", "november", "december")
                unit = process.objects.filter(company_id=company_id).values("unit")
                # 計算使用量合計
                for i in range(raw_data.count()):
                    consumption_total = raw_data[i].get("january") + raw_data[i].get("february") + raw_data[i].get("march") + raw_data[i].get("april") + \
                                        raw_data[i].get("may") + raw_data[i].get("june") + raw_data[i].get("july") + raw_data[i].get("august") + \
                                        raw_data[i].get("september") + raw_data[i].get("october") + raw_data[i].get("november") + raw_data[i].get("december")
                    # print("total::::::::::::::::::::::::::::::::::::::::", total)

                    single_data = raw_data[i]
                    # 將計算後的使用量丟回字典
                    single_data["total"] = '%.4f' % consumption_total
                    # 將 estimate 替換成中文
                    single_data["burn"] = "是" if single_data["burn"] else "否"
                    single_data["VOCs"] = "是" if single_data["VOCs"] else "否"
                    # 將單位丟回字典
                    for j in unit[i]:
                        single_data[j] = unit[i].get(j)
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "冰箱清單":
                t_data = []
                raw_data = refrigerator.objects.filter(company_id=company_id, years=year).values("id", "device_id", "device_name", "brand_name", "model_type", "position",
                                                                                                 "years_purchased", "filling_volume", "refrigerant_type", "filling_fix_volume",
                                                                                                 "effusion_rate")
                # 取單筆逸散量計算
                for i in range(raw_data.count()):
                    # 將要運算的值分別撈出(逸散率/填充量)
                    effusion_volume = Decimal(raw_data[i].get("effusion_rate")) * Decimal(0.01) * raw_data[i].get("filling_volume")
                    # print("effusion_volume::::::::::::::::::::::::::::::::::::::::", effusion_volume)
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    single_data["effusion_volume"] = '%.4f' % effusion_volume
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "冷氣機清單":
                t_data = []
                raw_data = airconditioner.objects.filter(company_id=company_id, years=year).values("id", "device_id", "device_name", "brand_name", "model_type", "position",
                                                                                                   "years_purchased", "filling_volume", "refrigerant_type", "filling_fix_volume",
                                                                                                   "effusion_rate")
                # 取單筆逸散量計算
                for i in range(raw_data.count()):
                    # 將要運算的值分別撈出(逸散率/填充量)
                    effusion_volume = Decimal(raw_data[i].get("effusion_rate")) * Decimal(0.01) * raw_data[i].get("filling_volume")
                    # print("effusion_volume::::::::::::::::::::::::::::::::::::::::", effusion_volume)
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    single_data["effusion_volume"] = '%.4f' % effusion_volume
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "車輛清單":
                t_data = []
                raw_data = vehicle.objects.filter(company_id=company_id, years=year).values("id", "device_id", "device_name", "brand_name", "model_type", "position",
                                                                                            "years_purchased", "filling_volume", "refrigerant_type", "filling_fix_volume",
                                                                                            "effusion_rate")
                # 取單筆逸散量計算
                for i in range(raw_data.count()):
                    # 將要運算的值分別撈出(逸散率/填充量)
                    effusion_volume = Decimal(raw_data[i].get("effusion_rate")) * Decimal(0.01) * raw_data[i].get("filling_volume")
                    # print("effusion_volume::::::::::::::::::::::::::::::::::::::::", effusion_volume)
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    single_data["effusion_volume"] = '%.4f' % effusion_volume
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "飲水機清單":
                t_data = []
                raw_data = water_dispenser.objects.filter(company_id=company_id, years=year).values("id", "device_id", "device_name", "brand_name", "model_type", "position",
                                                                                                    "years_purchased", "filling_volume", "refrigerant_type", "filling_fix_volume",
                                                                                                    "effusion_rate")
                # 取單筆逸散量計算
                for i in range(raw_data.count()):
                    # 將要運算的值分別撈出(逸散率/填充量)
                    effusion_volume = Decimal(raw_data[i].get("effusion_rate")) * Decimal(0.01) * raw_data[i].get("filling_volume")
                    # print("effusion_volume::::::::::::::::::::::::::::::::::::::::", effusion_volume)
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    single_data["effusion_volume"] = '%.4f' % effusion_volume
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "冰水機清單":
                t_data = []
                raw_data = ice_water_dispenser.objects.filter(company_id=company_id, years=year).values("id", "device_id", "device_name", "brand_name", "model_type", "position",
                                                                                                        "years_purchased", "filling_volume", "refrigerant_type", "filling_fix_volume",
                                                                                                        "effusion_rate")
                # 取單筆逸散量計算
                for i in range(raw_data.count()):
                    # 將要運算的值分別撈出(逸散率/填充量)
                    effusion_volume = Decimal(raw_data[i].get("effusion_rate")) * Decimal(0.01) * raw_data[i].get("filling_volume")
                    # print("effusion_volume::::::::::::::::::::::::::::::::::::::::", effusion_volume)
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    single_data["effusion_volume"] = '%.4f' % effusion_volume
                    # single_data["effusion_volume"] = effusion_volume
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "製冰機清單":
                t_data = []
                raw_data = ice_maker.objects.filter(company_id=company_id, years=year).values("id", "device_id", "device_name", "brand_name", "model_type", "position",
                                                                                              "years_purchased", "filling_volume", "refrigerant_type", "filling_fix_volume",
                                                                                              "effusion_rate")
                # 取單筆逸散量計算
                for i in range(raw_data.count()):
                    # 將要運算的值分別撈出(逸散率/填充量)
                    effusion_volume = Decimal(raw_data[i].get("effusion_rate")) * Decimal(0.01) * raw_data[i].get("filling_volume")
                    # print("effusion_volume::::::::::::::::::::::::::::::::::::::::", effusion_volume)
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    single_data["effusion_volume"] = '%.4f' % effusion_volume
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "設備清單":
                t_data = []
                raw_data = other_device.objects.filter(company_id=company_id, years=year).values("id", "device_id", "device_name", "brand_name", "model_type", "position",
                                                                                                 "years_purchased", "filling_volume", "refrigerant_type", "filling_fix_volume",
                                                                                                 "effusion_rate")
                # 取單筆逸散量計算
                for i in range(raw_data.count()):
                    # 將要運算的值分別撈出(逸散率/填充量)
                    effusion_volume = Decimal(raw_data[i].get("effusion_rate")) * Decimal(0.01) * raw_data[i].get("filling_volume")
                    # print("effusion_volume::::::::::::::::::::::::::::::::::::::::", effusion_volume)
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    single_data["effusion_volume"] = '%.4f' % effusion_volume
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "滅火器":
                t_data = list(
                    extinguisher.objects.filter(company_id=company_id, years=year).values("id", "device_id", "extinguisher_vendor", "extinguisher_type", "position", "inventory",
                                                                                          "chemical_weight", "using_amount", "monthly", "replace_filling_amount", "replace_filling_date"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "人天清冊":
                t_data = list(
                    personnel_inventory.objects.filter(company_id=company_id, years=year).values("id", "classification",
                                                                                                 "WKhours_january", "WKhours_february", "WKhours_march", "WKhours_april", "WKhours_may", "WKhours_june",
                                                                                                 "WKhours_july", "WKhours_august", "WKhours_september", "WKhours_october", "WKhours_november", "WKhours_december",
                                                                                                 "WKnum_january", "WKnum_february", "WKnum_march", "WKnum_april", "WKnum_may", "WKnum_june",
                                                                                                 "WKnum_july", "WKnum_august", "WKnum_september", "WKnum_october", "WKnum_november", "WKnum_december"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "委外人員清冊":
                t_data = list(
                    employee.objects.filter(company_id=company_id, years=year).values("id", "career",
                                                                                      "employeeNum_january", "employeeNum_february", "employeeNum_march", "employeeNum_april", "employeeNum_may", "employeeNum_june",
                                                                                      "employeeNum_july", "employeeNum_august", "employeeNum_september", "employeeNum_october", "employeeNum_november", "employeeNum_december",
                                                                                      "WKdays_january", "WKdays_february", "WKdays_march", "WKdays_april", "WKdays_may", "WKdays_june", "WKdays_july", "WKdays_august",
                                                                                      "WKdays_september", "WKdays_october", "WKdays_november", "WKdays_december",
                                                                                      "WKhours_january", "WKhours_february", "WKhours_march", "WKhours_april", "WKhours_may", "WKhours_june", "WKhours_july",
                                                                                      "WKhours_august", "WKhours_september", "WKhours_october", "WKhours_november", "WKhours_december"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "廢水":
                t_data = list(
                    waste_water.objects.filter(company_id=company_id, years=year).values("id", "waste_water_treatment_name", "waste_water_inflow_rate", "average_inlet_COD_concentration",
                                                                                         "average_COD_removal_rate", "CH4_capture_system_rate", "combustion_equipment_efficiency"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "廢汙泥":
                t_data = list(
                    waste_sludge.objects.filter(company_id=company_id, years=year).values("id", "waste_sludge_treatment_name", "waste_sludge_inflow_rate", "average_inlet_MLSS_concentration",
                                                                                          "CH4_capture_system_rate", "combustion_equipment_efficiency"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "溶劑、噴霧劑":
                t_data = list(solvent_aerosol_emission_sources.objects.filter(company_id=company_id, years=year).values("id", "solvent_name", "solvent_amount", "solvent_capacity", "solvent_capacity_unit", "gas_name", "gas_ratio", "density"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "用電量":
                t_data = []
                # 將要運算的值分別撈出(逸散率/填充量)
                raw_data = electricity.objects.filter(company_id=company_id, years=year).values("id", "EMI_id", "address",
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
                    single_data["kw_hr"] = '%.4f' % kw_hr
                    single_data["kkw_hr"] = '%.4f' % kkw_hr
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "上游運輸":
                t_data = list(
                    upstream_transportation.objects.filter(company_id=company_id).values("id", "acceptance_receipt", "commodity_name", "weight", "commodity_NW",
                                                                                         "organizational_use_products", "customer", "supplier", "supplier_address",
                                                                                         "trade_term", "receiving_address", "delivery_address",
                                                                                         "transport_distance", "transport_country", "transport_type", "transport_fuel", "paid", "trips",
                                                                                         "overseas_transport_distance", "overseas_delivery", "overseas_arrive", "overseas_paid", "overseas_trips",
                                                                                         "special_transport_distance", "special_transport_country", "special_transport_type", "special_transport_fuel", "special_paid", "special_trips",
                                                                                         "air_transport_distance", "air_delivery", "air_arrive", "air_paid", "air_trips"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "下游運輸":
                t_data = list(
                    downstream_transportation.objects.filter(company_id=company_id).values("id", "acceptance_receipt", "commodity_name", "weight", "commodity_NW", "customer", "supplier", "supplier_address",
                                                                                           "trade_term", "receiving_address", "delivery_address",
                                                                                           "transport_distance", "transport_country", "transport_type", "transport_fuel", "paid", "trips",
                                                                                           "overseas_transport_distance", "overseas_delivery", "overseas_arrive", "overseas_paid", "overseas_trips",
                                                                                           "special_transport_distance", "special_transport_country", "special_transport_type", "special_transport_fuel", "special_paid", "special_trips",
                                                                                           "air_transport_distance", "air_delivery", "air_arrive", "air_paid", "air_trips"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "員工通勤":
                t_data = []
                # 將要運算的值分別撈出(員工數/每日工時/每月工作天數/加班+補休時數/請假時數/休假時數)
                pre_data = employee_commute.objects.filter(company_id=company_id, years=year).values("id", "employee_id", "department", "employee_name")
                post_data = employee_commute.objects.filter(company_id=company_id, years=year).values("city", "township", "address", "commute_distance", "work_days")
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
                raw_data = employee_business_trip.objects.filter(company_id=company_id).values("id", "business_trip_number", "employee_id", "department", "employee_name", "business_trip_location", "business_trip_date")
                for i in range(raw_data.count()):
                    single_data = raw_data[i]
                    id = raw_data[i].get("id")
                    section = trip_section.objects.filter(trip_id=id).values("transportation", "distance")
                    transportation_dic = {"自駕汽車": 0.0, "高鐵": 0.0, "火車(電聯)": 0.0, "火車(柴聯)": 0.0, "計程車": 0.0, "機車": 0.0, "捷運": 0.0, "飛機": 0.0, "船舶": 0.0}
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
                raw_data = waste.objects.filter(company_id=company_id).values("id", "waste_name", "waste_weigh", "waste_date",
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
                t_data = list(VOCs_one.objects.filter(company_id=company_id, years=year).values("id", "emission", "concentration_ch4"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "VOCs_2":
                t_data = list(VOCs_two.objects.filter(company_id=company_id, years=year).values("id", "disposal_volume", "concentration_ch4", "voc_capture_rate", "combustion_equipment_rate",
                                                                                                "concentration_entrance", "concentration_exit", "builtIn_rate", "custom_rate"))
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "納管廢水排放量":
                t_data = []
                raw_data = pipe_wastewater.objects.filter(company_id=company_id, years=year).values("id", "pipe_id", "address", "factory", "january", "february", "march", "april", "may", "june", "july", "august",
                                                                                                    "september", "october", "november", "december")
                # 計算當月排放量
                for i in range(raw_data.count()):
                    Total_Emission = raw_data[i].get("january") + raw_data[i].get("february") + raw_data[i].get("march") + raw_data[i].get("april") + \
                                     raw_data[i].get("may") + raw_data[i].get("june") + raw_data[i].get("july") + raw_data[i].get("august") + \
                                     raw_data[i].get("september") + raw_data[i].get("october") + raw_data[i].get("november") + raw_data[i].get("december")
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    single_data["Total_Emission"] = '%.4f' % Total_Emission
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "採購原物料":
                t_data = []
                raw_data = purchase_material.objects.filter(company_id=company_id, years=year).values("id", "product_id", "product_name", "january", "february", "march", "april", "may", "june", "july", "august",
                                                                                                      "september", "october", "november", "december")
                # 計算當月排放量
                for i in range(raw_data.count()):
                    Total_Purchase = raw_data[i].get("january") + raw_data[i].get("february") + raw_data[i].get("march") + raw_data[i].get("april") + \
                                     raw_data[i].get("may") + raw_data[i].get("june") + raw_data[i].get("july") + raw_data[i].get("august") + \
                                     raw_data[i].get("september") + raw_data[i].get("october") + raw_data[i].get("november") + raw_data[i].get("december")
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    single_data["Total_Purchase"] = '%.4f' % Total_Purchase
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "產品間接排放":
                t_data = []
                raw_data = product_indirect_emissions.objects.filter(company_id=company_id, years=year).values("id", "product_id", "product_name", "january", "february", "march", "april", "may", "june", "july", "august",
                                                                                                               "september", "october", "november", "december")
                # 計算當月排放量
                for i in range(raw_data.count()):
                    Total_Deliver = raw_data[i].get("january") + raw_data[i].get("february") + raw_data[i].get("march") + raw_data[i].get("april") + \
                                    raw_data[i].get("may") + raw_data[i].get("june") + raw_data[i].get("july") + raw_data[i].get("august") + \
                                    raw_data[i].get("september") + raw_data[i].get("october") + raw_data[i].get("november") + raw_data[i].get("december")
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    single_data["Total_Deliver"] = '%.4f' % Total_Deliver
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)


def copy_last_year_data(request):
    if request.method == 'GET':
        device_id = request.GET.get('deviceId')
        print(device_id)
        company_value = request.GET.get('company_value')
        if company_value is None:
            company_id = current_user_group_id(request)
        else:
            company_id = int(company_value)
        print("load_table_company_value", company_value)
        t_name = list(section_two.objects.filter(did=device_id).values("d_name"))

        # 獲取當前年份
        this_year = datetime.now().year
        # 獲取去年年份
        last_year = this_year - 1

        for a in t_name:
            if a["d_name"] == "柴油發電機":
                last_year_data = emergency_generators.objects.filter(years=last_year, company_id=company_id).values(
                    'device_id', 'device_capacity', 'position', 'department', 'estimate',
                    'january', 'february', 'march', 'april', 'may', 'june', 'july',
                    'august', 'september', 'october', 'november', 'december',
                    'image_note', 'message_board', 'company_id', 'did_id'
                )
                # 如果去年沒有資料，顯示 alert 訊息
                if not last_year_data:
                    response_data = {
                        'success': False,
                        'message': '去年沒有任何資料！'
                    }
                    return JsonResponse(response_data)
                # 將年份改為今年
                for data in last_year_data:
                    data['years'] = this_year
                # 將資料儲存回資料庫中
                emergency_generators.objects.bulk_create(
                    [emergency_generators(**data) for data in last_year_data]
                )
            elif a["d_name"] == '燃燒設備':
                last_year_data = combustion_equipment.objects.filter(company_id=company_id, years=last_year).values(
                    'years', 'device_name', 'device_id', 'fuel_type', 'fuel_january',
                    'fuel_february', 'fuel_march', 'fuel_april', 'fuel_may', 'fuel_june', 'fuel_july', 'fuel_august',
                    'fuel_september', 'fuel_october', 'fuel_november', 'fuel_december', 'heat_january', 'heat_february',
                    'heat_march', 'heat_april', 'heat_may', 'heat_june', 'heat_july', 'heat_august', 'heat_september',
                    'heat_october', 'heat_november', 'heat_december', 'image_note', 'message_board', 'company_id', 'did_id'
                )
                # 如果去年沒有資料，顯示 alert 訊息
                if not last_year_data:
                    response_data = {
                        'success': False,
                        'message': '去年沒有任何資料！'
                    }
                    return JsonResponse(response_data)
                # 將年份改為今年
                for data in last_year_data:
                    data['years'] = this_year
                # 將資料儲存回資料庫中
                combustion_equipment.objects.bulk_create(
                    [combustion_equipment(**data) for data in last_year_data]
                )
        # 回傳 alert 訊息
        response_data = {
            'success': True,  # 也可以改為 False
            'message': '複製成功！'
        }
        return JsonResponse(response_data)


@login_required(login_url="/login/")
def emergency_generators_add(request, company_id=None):
    context = {}
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        EG_add = EGform(request.POST, request.FILES)
        if EG_add.is_valid():
            EG_add = EG_add.save(commit=False)
            EG_add.company_id = company_id
            EG_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = emergency_generators.objects.values("id").last().get("id")
            table_id = emergency_generators.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
        else:
            print(EG_add.errors)
    else:
        company_id = company_id
        EG_add = EGform()
    context['EG_add'] = EG_add
    context['company_id'] = company_id
    return render(request, 'home/emergency-generator.html', context)


@login_required(login_url="/login/")
def combustion_equipment_add(request, company_id=None):
    context = {}
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        CE_add = CEform(request.POST, request.FILES)
        if CE_add.is_valid():
            CE_add = CE_add.save(commit=False)
            CE_add.company_id = company_id
            CE_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = combustion_equipment.objects.values("id").last().get("id")
            table_id = combustion_equipment.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
    else:
        company_id = company_id
        CE_add = CEform()
    context['CE_add'] = CE_add
    context['company_id'] = company_id
    return render(request, 'home/combustion-equipment.html', context)


@login_required(login_url="/login/")
def official_car_add(request, company_id=None):
    context = {}
    OffCar_add = OFform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if OffCar_add.is_valid():
            urea = request.POST.getlist("urea")
            OffCar_add = OffCar_add.save(commit=False)
            if urea:
                OffCar_add.urea_january = urea[0]
                OffCar_add.urea_february = urea[1]
                OffCar_add.urea_march = urea[2]
                OffCar_add.urea_april = urea[3]
                OffCar_add.urea_may = urea[4]
                OffCar_add.urea_june = urea[5]
                OffCar_add.urea_july = urea[6]
                OffCar_add.urea_august = urea[7]
                OffCar_add.urea_september = urea[8]
                OffCar_add.urea_october = urea[9]
                OffCar_add.urea_november = urea[10]
                OffCar_add.urea_december = urea[11]
            OffCar_add.company_id = company_id
            OffCar_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = official_car.objects.values("id").last().get("id")
            table_id = official_car.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
    else:
        company_id = company_id
        OffCar_add = OFform()
    context['OffCar_add'] = OffCar_add
    context['company_id'] = company_id
    return render(request, 'home/official-car.html', context)


@login_required(login_url="/login/")
def material_add(request, company_id=None):
    context = {}
    MT_add = MTform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if MT_add.is_valid():
            MT_add = MT_add.save(commit=False)
            MT_add.company_id = company_id
            MT_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = material.objects.values("id").last().get("id")
            table_id = material.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
    else:
        company_id = company_id
        MT_add = MTform()
    context['MT_add'] = MT_add
    context['company_id'] = company_id
    return render(request, 'home/material.html', context)


@login_required(login_url="/login/")
def process_add(request, company_id=None):
    context = {}
    PC_add = PCform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if PC_add.is_valid():
            PC_add = PC_add.save(commit=False)
            PC_add.company_id = company_id
            PC_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = process.objects.values("id").last().get("id")
            table_id = process.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
    else:
        company_id = company_id
        PC_add = PCform()
    context['PC_add'] = PC_add
    context['company_id'] = company_id
    return render(request, 'home/process.html', context)


@login_required(login_url="/login/")
def refrigerator_add(request, company_id=None):
    context = {}
    RF_add = RFform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if RF_add.is_valid():
            RF_add = RF_add.save(commit=False)
            RF_add.company_id = company_id
            RF_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = refrigerator.objects.values("id").last().get("id")
            table_id = refrigerator.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
        else:
            return redirect('/new_device/', {'RF_add': RF_add})
    else:
        company_id = company_id
        RF_add = RFform()
    context['RF_add'] = RF_add
    context['company_id'] = company_id
    return render(request, 'home/refrigerator.html', context)


@login_required(login_url="/login/")
def airconditioner_add(request, company_id=None):
    context = {}
    AC_add = ACform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if AC_add.is_valid():
            AC_add = AC_add.save(commit=False)
            AC_add.company_id = company_id
            AC_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = airconditioner.objects.values("id").last().get("id")
            table_id = airconditioner.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
        else:
            return redirect('/new_device/', {'AC_add': AC_add})
    else:
        company_id = company_id
        AC_add = ACform()
    context['AC_add'] = AC_add
    context['company_id'] = company_id
    return render(request, 'home/airconditioner.html', context)


@login_required(login_url="/login/")
def vehicle_add(request, company_id=None):
    context = {}
    VC_add = VCform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if VC_add.is_valid():
            VC_add = VC_add.save(commit=False)
            VC_add.company_id = company_id
            VC_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = vehicle.objects.values("id").last().get("id")
            table_id = vehicle.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
    else:
        company_id = company_id
        VC_add = VCform()
    context['VC_add'] = VC_add
    context['company_id'] = company_id
    return render(request, 'home/vehicle.html', context)


@login_required(login_url="/login/")
def water_dispenser_add(request, company_id=None):
    context = {}
    WD_add = WDform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if WD_add.is_valid():
            WD_add = WD_add.save(commit=False)
            WD_add.company_id = company_id
            WD_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = water_dispenser.objects.values("id").last().get("id")
            table_id = water_dispenser.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
    else:
        company_id = company_id
        WD_add = WDform()
    context['WD_add'] = WD_add
    context['company_id'] = company_id
    return render(request, 'home/water-dispenser.html', context)


@login_required(login_url="/login/")
def ice_water_dispenser_add(request, company_id=None):
    context = {}
    IWD_add = IWDform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if IWD_add.is_valid():
            IWD_add.save(commit=False)
            IWD_add.company_id = company_id
            IWD_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = ice_water_dispenser.objects.values("id").last().get("id")
            table_id = ice_water_dispenser.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
    else:
        company_id = company_id
        IWD_add = IWDform()
    context['IWD_add'] = IWD_add
    context['company_id'] = company_id
    return render(request, 'home/ice-water-dispenser.html', context)


@login_required(login_url="/login/")
def ice_maker_add(request, company_id=None):
    context = {}
    IM_add = IMform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if IM_add.is_valid():
            IM_add = IM_add.save(commit=False)
            IM_add.company_id = company_id
            IM_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = ice_maker.objects.values("id").last().get("id")
            table_id = ice_maker.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
    else:
        company_id = company_id
        IM_add = IMform()
    context['IM_add'] = IM_add
    context['company_id'] = company_id
    return render(request, 'home/ice-maker.html', context)


@login_required(login_url="/login/")
def other_device_add(request, company_id=None):
    context = {}
    OD_add = ODform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if OD_add.is_valid():
            OD_add = OD_add.save(commit=False)
            OD_add.company_id = company_id
            OD_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = other_device.objects.values("id").last().get("id")
            table_id = other_device.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
    else:
        company_id = company_id
        OD_add = ODform()
    context['OD_add'] = OD_add
    context['company_id'] = company_id
    return render(request, 'home/other-device.html', context)


@login_required(login_url="/login/")
def extinguisher_add(request, company_id=None):
    context = {}
    EX_add = EXform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if EX_add.is_valid():
            EX_add = EX_add.save(commit=False)
            EX_add.company_id = company_id
            EX_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = extinguisher.objects.values("id").last().get("id")
            table_id = extinguisher.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
    else:
        company_id = company_id
        EX_add = EXform()
    context['EX_add'] = EX_add
    context['company_id'] = company_id
    return render(request, 'home/extinguisher.html', context)


@login_required(login_url="/login/")
def personnel_inventory_add(request, company_id=None):
    context = {}
    PI_add = PIform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if PI_add.is_valid():
            PI_add = PI_add.save(commit=False)
            PI_add.company_id = company_id
            PI_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = personnel_inventory.objects.values("id").last().get("id")
            table_id = personnel_inventory.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
    else:
        company_id = company_id
        PI_add = PIform()
    context['PI_add'] = PI_add
    context['company_id'] = company_id
    return render(request, 'home/personnel-inventory.html', context)


@login_required(login_url="/login/")
def employee_add(request, company_id=None):
    context = {}
    EMP_add = EMPform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if EMP_add.is_valid():
            EMP_add = EMP_add.save(commit=False)
            EMP_add.company_id = company_id
            EMP_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = employee.objects.values("id").last().get("id")
            table_id = employee.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
    else:
        company_id = company_id
        EMP_add = EMPform()
    context['EMP_add'] = EMP_add
    context['company_id'] = company_id
    return render(request, 'home/employee.html', context)


# 廢水
@login_required(login_url="/login/")
def waste_water_add(request, company_id=None):
    context = {}
    waste_water_add = WASTEWATERform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if waste_water_add.is_valid():
            waste_water_add = waste_water_add.save(commit=False)
            waste_water_add.company_id = company_id
            waste_water_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = waste_water.objects.values("id").last().get("id")
            table_id = waste_water.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
    else:
        company_id = company_id
        waste_water_add = WASTEWATERform
    context['waste_water_add'] = waste_water_add
    context['company_id'] = company_id
    return render(request, 'home/waste-water.html', context)


# 廢汙泥
@login_required(login_url="/login/")
def waste_sludge_add(request, company_id=None):
    context = {}
    waste_sludge_add = WasteSludgeForm(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if waste_sludge_add.is_valid():
            waste_sludge_add = waste_sludge_add.save(commit=False)
            waste_sludge_add.company_id = company_id
            waste_sludge_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = waste_sludge_add.objects.values("id").last().get("id")
            table_id = waste_sludge_add.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
    else:
        company_id = company_id
        waste_sludge_add = WasteSludgeForm()
    context['waste_sludge_add'] = waste_sludge_add
    context['company_id'] = company_id
    return render(request, 'home/waste-sludge.html', context)


# 溶劑、噴霧劑
@login_required(login_url="/login/")
def solvent_aerosol_emission_sources_add(request, company_id=None):
    context = {}
    SAES_add = SolventAerosolEmissionSourcesForm(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if SAES_add.is_valid():
            solvent = SAES_add.save(commit=False)
            solvent.company_id = company_id
            solvent.save()
            return redirect('/carbon-system/')
        # else:
        #     print("SAES_add表單錯誤>>>>>>>>>>>>>>>>>>>>\n", SAES_add.errors)
        #     return render(request, 'home/solvent-aerosol-emission-sources.html', {'SAES_add': SAES_add, 'company_id': company_id})
    else:
        company_id = company_id
        SAES_add = SolventAerosolEmissionSourcesForm()
    context['SAES_add'] = SAES_add
    context['company_id'] = company_id
    return render(request, 'home/solvent-aerosol-emission-sources.html', {'SAES_add': SAES_add, 'company_id': company_id})


# VOCs1表單儲存
@login_required(login_url="/login/")
def VOCs_one_add(request, company_id=None):
    context = {}
    VOCs_one_add = VOCsOneForm(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if VOCs_one_add.is_valid():
            VOCs_one_add = VOCs_one_add.save(commit=False)
            VOCs_one_add.company_id = company_id
            VOCs_one_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = VOCs_one.objects.values("id").last().get("id")
            table_id = VOCs_one.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
    else:
        company_id = company_id
        VOCs_one_add = VOCsOneForm()
    context['VOCs_one_add'] = VOCs_one_add
    context['company_id'] = company_id
    return render(request, 'home/VOCs-one.html', context)


# VOCs2表單儲存
@login_required(login_url="/login/")
def VOCs_two_add(request, company_id=None):
    context = {}
    VOCs_two_add = VOCsTwoForm(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        print("company_id", company_id)
        if VOCs_two_add.is_valid():
            VOCs_two_add = VOCs_two_add.save(commit=False)
            VOCs_two_add.company_id = company_id
            VOCs_two_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = VOCs_two.objects.values("id").last().get("id")
            table_id = VOCs_two.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
        else:
            print("\n", VOCs_two_add.errors)
            return render(request, 'home/VOCs-two.html', {'VOCs_two_add': VOCs_two_add, 'company_id': company_id})
    else:
        company_id = company_id
        VOCs_two_add = VOCsTwoForm()
    context['VOCs_two_add'] = VOCs_two_add
    context['company_id'] = company_id
    return render(request, 'home/VOCs-two.html', context)


@login_required(login_url="/login/")
def electricity_add(request, company_id=None):
    context = {}
    ELEC_add = ELECform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if ELEC_add.is_valid():
            ELEC_add = ELEC_add.save(commit=False)
            ELEC_add.company_id = company_id
            ELEC_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = electricity.objects.values("id").last().get("id")
            table_id = electricity.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
    else:
        company_id = company_id
        ELEC_add = ELECform
    context['ELEC_add'] = ELEC_add
    context['company_id'] = company_id
    return render(request, 'home/electricity.html', context)


@login_required(login_url="/login/")
def upstream_transportation_add(request, company_id=None):
    context = {}
    UT_add = UTform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if UT_add.is_valid():
            UT_add = UT_add.save(commit=False)
            UT_add.company_id = company_id
            UT_add.save()
            stages = request.POST.getlist('stage')
            last_id = upstream_transportation.objects.values("id").last().get("id")
            table_id = upstream_transportation.objects.values("did").last().get("did")
            for stage in stages:
                if stage == "陸運":
                    image_paths = request.FILES.getlist('file_field1')
                elif stage == "海運":
                    image_paths = request.FILES.getlist('file_field2')
                elif stage == "特殊陸運":
                    image_paths = request.FILES.getlist('file_field3')
                elif stage == "空運":
                    image_paths = request.FILES.getlist('file_field4')
                else:
                    image_paths = []
                for img in image_paths:
                    photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                    print(stage)
                    photo.save()
            return redirect('/carbon-system/')
    else:
        company_id = company_id
        UT_add = UTform()
    context['UT_add'] = UT_add
    context['company_id'] = company_id
    return render(request, 'home/upstream-transportation.html', context)


@login_required(login_url="/login/")
def downstream_transportation_add(request, company_id=None):
    context = {}
    DT_add = DTform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if DT_add.is_valid():
            DT_add = DT_add.save(commit=False)
            DT_add.company_id = company_id
            DT_add.save()
            stages = request.POST.getlist('stage')
            last_id = downstream_transportation.objects.values("id").last().get("id")
            table_id = downstream_transportation.objects.values("did").last().get("did")
            for stage in stages:
                if stage == "陸運":
                    image_paths = request.FILES.getlist('file_field1')
                elif stage == "海運":
                    image_paths = request.FILES.getlist('file_field2')
                elif stage == "特殊陸運":
                    image_paths = request.FILES.getlist('file_field3')
                elif stage == "空運":
                    image_paths = request.FILES.getlist('file_field4')
                else:
                    image_paths = []
                for img in image_paths:
                    photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                    print(stage)
                    photo.save()
            return redirect('/carbon-system/')
    else:
        company_id = company_id
        DT_add = DTform()
    context['DT_add'] = DT_add
    context['company_id'] = company_id
    return render(request, 'home/downstream-transportation.html', context)


@login_required(login_url="/login/")
def employee_commute_add(request, company_id=None):
    context = {}
    EC_add = ECform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if EC_add.is_valid():
            commute = EC_add.save(commit=False)
            commute.company_id = company_id
            commute.save()
            Commute_formSet = CommuteFormSet(request.POST, request.FILES, instance=commute)
            if Commute_formSet.is_valid():
                Commute_formSet.save()
                return redirect('/carbon-system/')
            else:
                last_data = employee_commute.objects.last()
                last_data.delete()
                print("Commute_formSet>>>>>>>>>>>>>>>>>>>>\n", Commute_formSet)
                return render(request, 'home/employee-commute.html', {'EC_add': EC_add, 'CommuteFormSet': CommuteFormSet, 'company_id': company_id})
    else:
        company_id = company_id
        EC_add = ECform()
    context['EC_add'] = EC_add
    context['company_id'] = company_id
    return render(request, 'home/employee-commute.html', {'EC_add': EC_add, 'CommuteFormSet': CommuteFormSet, 'company_id': company_id})


@login_required(login_url="/login/")
def employee_business_trip_add(request, company_id=None):
    context = {}
    EBT_add = EBTform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if EBT_add.is_valid():
            business = EBT_add.save(commit=False)
            business.company_id = company_id
            business.save()
            tripsection_formSet = TripSectionFormSet(request.POST, request.FILES, instance=business)
            if tripsection_formSet.is_valid():
                tripsection_formSet.save()
                return redirect('/carbon-system/')
            else:
                last_data = employee_business_trip.objects.last()
                last_data.delete()
                print("tripsection_formSet表單錯誤>>>>>>>>>>>>>>>>>>>>\n", tripsection_formSet)
                return render(request, 'home/employee-business-trip.html', {'EBT_add': EBT_add, 'TripSectionFormSet': TripSectionFormSet, 'company_id': company_id})
    else:
        EBT_add = EBTform()
        company_id = company_id
    context['EBT_add'] = EBT_add
    context['company_id'] = company_id
    return render(request, 'home/employee-business-trip.html', {'EBT_add': EBT_add, 'TripSectionFormSet': TripSectionFormSet, 'company_id': company_id})


@login_required(login_url="/login/")
def waste_add(request, company_id=None):
    context = {}
    WASTE_add = WASTEform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if WASTE_add.is_valid():
            WASTE_add = WASTE_add.save(commit=False)
            WASTE_add.company_id = company_id
            WASTE_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = waste.objects.values("id").last().get("id")
            table_id = waste.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
    else:
        company_id = company_id
        WASTE_add = WASTEform
    context['WASTE_add'] = WASTE_add
    context['company_id'] = company_id
    return render(request, 'home/waste.html', context)


# 納管廢水
@login_required(login_url="/login/")
def pipe_wastewater_add(request, company_id=None):
    context = {}
    PW_add = PWform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if PW_add.is_valid():
            PW_add = PW_add.save(commit=False)
            PW_add.company_id = company_id
            PW_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = pipe_wastewater.objects.values("id").last().get("id")
            table_id = pipe_wastewater.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
    else:
        company_id = company_id
        PW_add = PWform()
    context['PW_add'] = PW_add
    context['company_id'] = company_id
    return render(request, 'home/pipe-wastewater.html', context)


# 採購原物料
@login_required(login_url="/login/")
def purchase_material_add(request, company_id=None):
    context = {}
    PM_add = PMform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if PM_add.is_valid():
            PM_add = PM_add.save(commit=False)
            PM_add.company_id = company_id
            PM_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = purchase_material.objects.values("id").last().get("id")
            table_id = purchase_material.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
    else:
        company_id = company_id
        PM_add = PMform()
    context['PM_add'] = PM_add
    context['company_id'] = company_id
    return render(request, 'home/purchase-material.html', context)


# 產品間接排放
@login_required(login_url="/login/")
def product_indirect_emissions_add(request, company_id=None):
    context = {}
    PIE_add = PIEform(request.POST, request.FILES)
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if PIE_add.is_valid():
            PIE_add = PIE_add.save(commit=False)
            PIE_add.company_id = company_id
            PIE_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = product_indirect_emissions.objects.values("id").last().get("id")
            table_id = product_indirect_emissions.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            return redirect('/carbon-system/')
    else:
        company_id = company_id
        PIE_add = PIEform()
    context['PIE_add'] = PIE_add
    context['company_id'] = company_id
    return render(request, 'home/product-indirect-emissions.html', context)


# ~~~
@login_required(login_url="/login/")
def carbon_system(request):
    if request.user.is_authenticated:
        username = request.user.username
        print("username: ", username)
    groups_query = request.user.groups.values("name").first()
    company_group = django.contrib.auth.models.Group.objects.values("id", "name")[1:]

    company_id = current_user_group_id(request)
    context = {
        "groups_query": groups_query,
        "company_id": company_id,
        "company_group": company_group
    }

    # context.update(groups_query)
    # print("context: ", context)

    # if request.session.get('dropdown_one'):
    #     del request.session['dropdown_one']
    #     del request.session['dropdown_two']
    #     del request.session['dropdown_three']
    return render(request, "home/carbon-system.html", context)


# 新增轉跳
@login_required(login_url="/login/")
def add_page(request, ):
    global device_function
    if request.method == "GET":
        device_id = request.GET.get('deviceId')
        company_value = request.GET.get('company_value')
        if company_value is None:
            company_id = current_user_group_id(request)
        else:
            company_id = int(company_value)
        # 建立字典
        function_dic = {
            "1": emergency_generators_add(request, company_id),
            "2": combustion_equipment_add(request, company_id),
            "3": official_car_add(request, company_id),
            "4": material_add(request, company_id),
            "5": process_add(request, company_id),
            "6": refrigerator_add(request, company_id),
            "7": airconditioner_add(request, company_id),
            "8": vehicle_add(request, company_id),
            "9": water_dispenser_add(request, company_id),
            "10": ice_water_dispenser_add(request, company_id),
            "11": ice_maker_add(request, company_id),
            "12": other_device_add(request, company_id),
            "13": extinguisher_add(request, company_id),
            "14": personnel_inventory_add(request, company_id),
            "15": employee_add(request, company_id),
            "16": waste_water_add(request, company_id),
            "17": waste_sludge_add(request, company_id),
            "18": solvent_aerosol_emission_sources_add(request, company_id),
            "19": VOCs_one_add(request, company_id),
            "20": VOCs_two_add(request, company_id),
            "21": electricity_add(request, company_id),
            "22": upstream_transportation_add(request, company_id),
            "23": downstream_transportation_add(request, company_id),
            "24": employee_commute_add(request, company_id),
            "25": employee_business_trip_add(request, company_id),
            "26": waste_add(request, company_id),
            "27": pipe_wastewater_add(request, company_id),
            "28": purchase_material_add(request, company_id),
            "29": product_indirect_emissions_add(request, company_id)
        }
        if function_dic.get(device_id):
            device_function = function_dic.get(device_id)
        return device_function
        # return redirect(device_function, locals())


# 編輯轉跳
@login_required(login_url="/login/")
def edit_device(request):
    datasheet_id = request.GET.get('datasheet')
    single_dataID = request.GET.get('single_dataID')
    dropdown_one = request.GET.get('dropdown_one')
    dropdown_two = request.GET.get('dropdown_two')
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
        "27": pipe_wastewater,
        "28": purchase_material,
        "29": product_indirect_emissions
    }
    formlName = {
        "1": EGform, "2": CEform, "3": OFform, "4": MTform, "5": PCform,
        "6": RFform, "7": ACform, "8": VCform, "9": WDform, "10": IWDform,
        "11": IMform, "12": ODform, "13": EXform, "14": PIform, "15": EMPform,
        "16": WASTEWATERform, "17": WasteSludgeForm, "18": SolventAerosolEmissionSourcesForm,
        "19": VOCsOneForm, "20": VOCsTwoForm, "21": ELECform, "22": UTform,
        "23": DTform, "24": ECform, "25": EBTform, "26": WASTEform, "27": PWform, "28": PMform, "29": PIEform,
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
                "dropdown_one": dropdown_one,
                "dropdown_two": dropdown_two,
            }
            try:
                if datasheet_id in formsetName:
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
                "27": "home/pipe-wastewater-edit.html",
                "28": "home/purchase-material-edit.html",
                "29": "home/product-indirect-emissions-edit.html",
            }
            if htmlName.get(datasheet_id):
                EditDevice_page = htmlName.get(datasheet_id)
                return render(request, EditDevice_page, formUpdata_name)


# 儲存更新後的資料
@login_required(login_url="/login/")
def update_device(request, datasheet_id, single_dataID, dropdown_one, dropdown_two):
    if request.session.get('dropdown_one'):
        del request.session['dropdown_one']
        del request.session['dropdown_two']
        del request.session['dropdown_three']
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
        "27": pipe_wastewater,
        "28": purchase_material,
        "29": product_indirect_emissions
    }
    formName = {
        "1": EGform, "2": CEform, "3": OFform, "4": MTform, "5": PCform,
        "6": RFform, "7": ACform, "8": VCform, "9": WDform, "10": IWDform,
        "11": IMform, "12": ODform, "13": EXform, "14": PIform, "15": EMPform,
        "16": WASTEWATERform, "17": WasteSludgeForm, "18": SolventAerosolEmissionSourcesForm,
        "19": VOCsOneForm, "20": VOCsTwoForm, "21": ELECform, "22": UTform,
        "23": DTform, "24": ECform, "25": EBTform, "26": WASTEform, "27": PWform, "28": PMform, "29": PIEform,
    }
    formsetName = {
        "24": CommuteFormSet, "25": TripSectionFormSet
    }
    if modelName.get(datasheet_id) and formName.get(datasheet_id):
        dbName = modelName.get(datasheet_id)
        form = formName.get(datasheet_id)
        current_data = get_object_or_404(dbName, id=single_dataID)
        update_from = form(request.POST, request.FILES, instance=current_data)
        if request.method == 'POST':
            cancel = request.POST.get("cancel")
            # ~~~
            if cancel:
                print("cancel")
                dropdown = {
                    'dropdown_one': dropdown_one,
                    'dropdown_two': dropdown_two,
                    'dropdown_three': datasheet_id,
                }
                request.session.update(dropdown)
                return redirect('/carbon-system/')
            try:
                if datasheet_id in formsetName:
                    formset = formsetName.get(datasheet_id)
                    update_formset = formset(request.POST, request.FILES, instance=current_data)
                    if update_from.is_valid() and update_formset.is_valid():
                        update_from.save()
                        update_formset.save()
                        return redirect('/carbon-system/', locals())
                    else:
                        print("\n", update_formset.errors)
                        return redirect('/edit_device/?datasheet=' + str(datasheet_id) + '&single_dataID=' + str(single_dataID), locals())
            except:
                pass
            if update_from.is_valid():
                update_from.save()
                return redirect('/carbon-system/', locals())
            else:
                print("\n", update_from.errors)
                return redirect('/edit_device/?datasheet=' + str(datasheet_id) + '&single_dataID=' + str(single_dataID), locals())
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
            "27": pipe_wastewater,
            "28": purchase_material,
            "29": product_indirect_emissions
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
                "內容": ["序號", "設備編號", "容量(𝓁)", "地點", "部門", "是否推估"],
                "加油量(單位:𝓁)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "合計"]
            },

            "2": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "名稱", "編號", "燃料種類"],
                "使用量": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "合計"],
                "熱值(Kcal/kg)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "平均"]
            },

            "3": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "類別", "編號", "燃料種類", "所屬單位", "計程方式"],
                "耗用量(單位:油車𝓁/電車kWh/公里數km)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "合計"],
                "尿素添加量(𝓁)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "合計"]
            },

            "4": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "原物料號", "原/物料", "名稱"],
                "是否為化學品": ["化學品名稱", "化學品名", "化學式"],
                "月用量(單位:公噸)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
            },

            "5": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "製程階段", "料號", "製程添加名稱", "含碳量(%)", "是否燃燒", "VOCs"],
                "使用量(單位:公斤)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "總計", "使用量單位"]
            },
            # 冷媒(6~13)
            "6": {
                "編輯區": ["刪除", "修改"],
                "冰箱清單": ["序號", "編號", "名稱", "品牌", "型號", "位置", "規格填充量", "冷媒類型", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "7": {
                "編輯區": ["刪除", "修改"],
                "冷氣機清單": ["序號", "編號", "名稱", "品牌", "型號", "位置", "購買年份", "規格填充量", "冷媒類型", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "8": {
                "編輯區": ["刪除", "修改"],
                "車輛清單": ["序號", "編號", "名稱", "品牌", "型號", "位置", "購買年份", "規格填充量", "冷媒類型", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "9": {
                "編輯區": ["刪除", "修改"],
                "飲水機清單": ["序號", "編號", "名稱", "品牌", "型號", "位置", "購買年份", "規格填充量", "冷媒類型", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "10": {
                "編輯區": ["刪除", "修改"],
                "冰水機清單": ["序號", "編號", "名稱", "品牌", "型號", "位置", "購買年份", "規格填充量", "冷媒類型", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "11": {
                "編輯區": ["刪除", "修改"],
                "製冰機清單": ["序號", "編號", "名稱", "品牌", "型號", "位置", "購買年份", "規格填充量", "冷媒類型", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "12": {
                "編輯區": ["刪除", "修改"],
                "設備清單": ["序號", "編號", "名稱", "品牌", "型號", "位置", "購買年份", "規格填充量", "冷媒類型", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "13": {
                "編輯區": ["刪除", "修改"],
                "滅火器清單": ["序號", "設備編號", "廠商", "類型", "擺放位置(廠別)", "庫存量", "藥劑重量(單位:kg)", "使用量數量", "使用月份", "更換/填充量", "更換/填充日期"]
            },
            # 人天清冊
            "14": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "類型"],
                "時數": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
                "人數": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
            },

            "15": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "人員類別"],
                "員工人數": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
                "當月工作天數": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
                "每日工作時數": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
            },

            "16": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "廢水厭氧處理單元名稱 ", "廢水進流量(立方公尺/年)", "平均進流COD濃度(mg/L)", "平均進流COD濃度(mg/L)", u"CH\u2084捕集系統捕集率", "燃燒設備效率"],
            },

            "17": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "廢棄污泥厭氧處理單元名稱", "污泥進流量(立方公尺/年)", "平均進流MLSS濃度(mg/L)", u"CH\u2084捕集系統捕集率", "燃燒設備效率"],
            },

            "18": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "溶劑、噴霧劑名稱", "數量(瓶/罐)", "容量", "單位", "氣體名稱", "氣體含量(%)", "密度"]
            },

            "19": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "VOCs排放量(千立方公尺/年)", u"CH\u2084濃度(ppm)"],
            },

            "20": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "VOCs排放量(千立方公尺/年)", u'CH\u2084濃度', "VOCs設備補集率", "燃燒設備效率"],
                "VOCs濃度": ["入口濃度", "出口濃度"],
                u"CO\u2082排放係數": ["內設值", "自訂值"],
            },

            "21": {
                "編輯區": ["刪除", "修改"],
                "用電量": ["序號", "電表編號", "地址", "一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "小計(度)", "總計(千度)"]
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
                "員工通勤清冊": ["序號", "編號", "部門", "姓名", "交通方式", "居住城市", "鄉鎮市區", "行政區公家機關地址", "至公司距離(km)", "年工作天數", "距離合計"],
            },

            # 員工出差
            "25": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "出差單號", "員工編號", "部門", "姓名", "出差地點", "啟程日期"],
                "距離(pkm)": ["自駕汽車", "高鐵", "火車(電聯)", "火車(柴聯)", "計程車", "機車", "捷運", "飛機", "船舶"],
            },

            "26": {
                "編輯區": ["刪除", "修改"],
                "廢棄物處理": ["序號", "名稱", "重量(噸)", "運送時間", "處置地點", "處理方式", "處理廠商名稱", "運輸方式", "運輸燃料", "運輸距離(km)", "T*km"],
            },

            # 納管廢水
            "27": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "納管編號", "廠別", "地址"],
                "納管廢水排放量": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "小計(公噸)"]
            },

            # 原物料採購
            "28": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "產品編號", "產品名稱"],
                "原物料採購量": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "小計(公噸)"]
            },

            # 原物料採購
            "29": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "產品編號", "產品名稱"],
                "產品間接排放量": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "小計(公噸)"]
            },
        }
        if device_id in htmlName:
            title = [htmlName.get(device_id)]
            return JsonResponse(title, safe=False)


def chemical_dropdowm(request):
    chemical_add = list(chemical_table.objects.values("chemical_add"))
    return JsonResponse(chemical_add, safe=False)


def load_chemical(request):
    chemical_add = request.GET.get("add_ch_name")
    chemical_data = list(chemical_table.objects.filter(chemical_add=chemical_add).values("chemical_name", "chemical_formula"))
    return JsonResponse(chemical_data, safe=False)
