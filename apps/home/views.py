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
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.db import models

import apps
from .forms import *
from apps.home.models import emergency_generators, section_one, section_two
from apps.home.models import *


# from apps.home.models import *


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
            # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>1321213", current_process)
            all = list(section_two.objects.all())
            # print("00000000000000000000000000000000000000",all)
            d_data = list(section_two.objects.filter(cpid=current_process).values("d_name", "did"))
            # print("111111111111111111111111111111111111111111111111111111111", d_data)
            return JsonResponse(d_data, safe=False)


# 抓欄位
# @login_required(login_url="/login/")
# def load_table(request):
#     if request.method == 'GET':
#         device_id = request.GET.get('deviceId', None)
#         if device_id:
#             t_name = list(section_two.objects.filter(did=device_id).values("t_name"))
#             print("888888888", t_name)
#             for model in t_name:
#                 print("222222222222222222222222222222222222", model["t_name"])
#                 t_data = list(globals()[model["t_name"]].objects.filter().all().values())
#                 print(t_data)
#                 return JsonResponse(t_data, safe=False)

# 抓欄位(if
@login_required(login_url="/login/")
def load_table(request):
    if request.method == 'GET':
        device_id = request.GET.get('deviceId', None)
        if device_id:
            allTable = list(emergency_generators.objects.all())
            # print("00000000000000000000000000000000000000", allTable)
            # allTable.append({'total': 100})
            # print("55555555555555555555555555555555555555", allTable)

            t_name = list(section_two.objects.filter(did=device_id).values("d_name"))
            # print("888888888", t_name)
            # 從db撈每張表要顯示的值
            for a in t_name:
                if a["d_name"] == "緊急發電機":
                    t_data = list(
                        emergency_generators.objects.values("id", "device_id", "period_starttime", "period_endtime",
                                                            "device_capacity", "position", "department",
                                                            "january", "february", "march", "april",
                                                            "may", "june", "july", "august",
                                                            "september", "october", "november", "december"))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "燃燒設備":
                    fuel = combustion_equipment.objects.values("fuel_january", "fuel_february", "fuel_march",
                                                               "fuel_april", "fuel_may", "fuel_june",
                                                               "fuel_july", "fuel_august", "fuel_september",
                                                               "fuel_october", "fuel_november", "fuel_december")
                    heat = combustion_equipment.objects.values("heat_january", "heat_february", "heat_march",
                                                               "heat_april", "heat_may", "heat_june",
                                                               "heat_july", "heat_august", "heat_september",
                                                               "heat_october", "heat_november", "heat_december")
                    fuel_sum = 0
                    heat_sum = 0
                    c = 0
                    for a in fuel[0]:
                        fuel_sum = fuel_sum + fuel[0].get(a)
                    for a in heat[1]:
                        heat_sum = heat_sum + heat[1].get(a)
                        c += 1
                    heat_avg = heat_sum / c
                    print("fuel_sum::::::::::::::::::::::::::::::::::::::::", fuel_sum)
                    print("c::::::::::::::::::::::::::::::::::::::::", heat_avg)
                    t_data = []
                    for a in combustion_equipment.objects.values(
                            "id", "device_name", "device_id", "fuel_type", "period_starttime", "period_endtime",
                            "fuel_january", "fuel_february", "fuel_march", "fuel_april", "fuel_may", "fuel_june",
                            "fuel_july", "fuel_august", "fuel_september", "fuel_october", "fuel_november", "fuel_december",
                            "heat_january", "heat_february", "heat_march", "heat_april", "heat_may", "heat_june",
                            "heat_july", "heat_august", "heat_september", "heat_october", "heat_november", "heat_december"
                    ):
                        a["fuel_sum"] = fuel_sum
                        t_data.append(a)
                        return JsonResponse(t_data, safe=False)
                        # print("t_data::::::::::::::::::::::::::::::::::::::::::::::::", t_data)
                elif a["d_name"] == "公務車":
                    fuel = official_car.objects.values("january", "february", "march", "april",
                                                       "may", "june", "july", "august",
                                                       "september", "october", "november", "december")
                    print("fuel>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", fuel)
                    c = 0
                    for a in fuel:
                        sum_fuel = 0
                        # print("6666666666666666666666666666666666666666666666666666666666666", a)
                        for i in a:
                            # print("a[i]a[i]a[i]a[i]a[i]a[i]a[i]a[i]a[i]a[i]a[i]a[i]a[i]a[i]a[i]a[i]a[i]a[i]a[i]a[i]a[i]a[i]", a[i])
                            sum_fuel = sum_fuel + a[i]
                            # t_data.insert(5, sum_fuel)
                        print("sum_fuel>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", sum_fuel)
                        # c += 1

                    t_data = list(
                        official_car.objects.values("id", "vehicle_type", "device_id", "fuel_type", "department",
                                                    "january", "february", "march", "april",
                                                    "may", "june", "july", "august",
                                                    "september", "october", "november", "december",
                                                    "urea_add_date", "urea_add_quantity"))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "原物料使用":
                    t_data = list(
                        material.objects.values("id", "material_name", "material_id", "material_type",
                                                "january", "february", "march", "april",
                                                "may", "june", "july", "august",
                                                "september", "october", "november", "december"))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "製程添加化學品":
                    t_data = list(
                        process.objects.values("id", "process_add_name", "chemical_name", "chemical_formula",
                                               "process_stage", "material_id", "CAS_NO", "burn",
                                               "january", "february", "march", "april",
                                               "may", "june", "july", "august",
                                               "september", "october", "november", "december"))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "冰箱清單":
                    # 將要運算的值分別撈出(逸散率/填充量)
                    effusion_rate = refrigerator.objects.values("effusion_rate")
                    filling_volume = refrigerator.objects.values("filling_volume")
                    effusion_volume = effusion_rate[0].get("effusion_rate") * 0.01 * filling_volume[0].get("filling_volume")
                    # 運算後丟入字典，轉陣列
                    t_data = []
                    for a in refrigerator.objects.values("id", "device_name", "device_id", "brand_name", "model_type",
                                                         "years", "position", "refrigerant_type",
                                                         "filling_volume", "filling_date", "filling_fix_volume", "effusion_rate"):
                        a["effusion_volume"] = effusion_volume
                        # print("raw_data::::::::::::::::::::::::::::::::::::::::::::", a)
                        t_data.append(a)
                        # print("t_data::::::::::::::::::::::::::::::::::::::::::::", t_data)
                        return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "冷氣機清單":
                    t_data = list(
                        airconditioner.objects.values("id", "device_name", "device_id", "brand_name", "model_type",
                                                      "years", "position", "refrigerant_type",
                                                      "filling_volume", "filling_date", "filling_fix_volume", "effusion_rate"))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "車輛清單":
                    t_data = list(
                        vehicle.objects.values("id", "device_name", "device_id", "brand_name", "model_type",
                                               "years", "position", "refrigerant_type",
                                               "filling_volume", "filling_date", "filling_fix_volume", "effusion_rate"))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "飲水機清單":
                    t_data = list(
                        water_dispenser.objects.values("id", "device_name", "device_id", "brand_name", "model_type",
                                                       "years", "position", "refrigerant_type",
                                                       "filling_volume", "filling_date", "filling_fix_volume", "effusion_rate"))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "冰水機清單":
                    t_data = list(
                        ice_water_dispenser.objects.values("id", "device_name", "device_id", "brand_name", "model_type",
                                                           "years", "position", "refrigerant_type",
                                                           "filling_volume", "filling_date", "filling_fix_volume", "effusion_rate"))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "製冰機清單":
                    t_data = list(
                        ice_maker.objects.values("id", "device_name", "device_id", "brand_name", "model_type",
                                                 "years", "position", "refrigerant_type",
                                                 "filling_volume", "filling_date", "filling_fix_volume", "effusion_rate"))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "其他設備清單":
                    t_data = list(
                        other_device.objects.values("id", "device_name", "device_id", "brand_name", "model_type",
                                                    "years", "position", "refrigerant_type",
                                                    "filling_volume", "filling_date", "filling_fix_volume", "effusion_rate"))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "冷媒總表":
                    t_data = list(
                        refrigerant_total_table.objects.values("id", "device_name", "device_id", "brand_name", "model_type",
                                                               "years", "position", "refrigerant_type",
                                                               "filling_volume", "filling_date", "filling_fix_volume", "effusion_rate"))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "滅火器":
                    t_data = list(
                        extinguisher.objects.values("id", "device_id", "position", "extinguisher_name",
                                                    "extinguisher_type", "extinguisher_vendor", "chemical_spec", "chemical_weight", "inventory", "using_date", "using_amount", "replace_filling_date", "replace_filling_amount"))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "人天清冊":
                    t_data = list(
                        personnel_inventory.objects.values("id", "years", "monthly", "employee_number", "daily_hours",
                                                           "working_days", "overtime", "leave_hours",
                                                           "day_off_hours"))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "保全清單":
                    t_data = list(
                        security.objects.values("id", "years", "monthly", "security_number", "daily_hours",
                                                "working_days", "total_working_hours", "total_working_day"))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "用電量":
                    t_data = list(
                        electricity.objects.values("id", "years", "EMI_id", "address",
                                                   "january", "february", "march", "april",
                                                   "may", "june", "july", "august",
                                                   "september", "october", "november", "december"))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "上游運輸":
                    t_data = list(
                        upstream_transportation.objects.values("id", "acceptance_receipt", "commodity_name", "commodity_NW",
                                                               "customer", "supplier", "supplier_address",
                                                               "trade_term", "receiving_address", "delivery_address", "transport_distance",
                                                               "transport_country", "transport_type", "vehicle_fuel", "trips",
                                                               "overseas_transport_type", "overseas_vehicle_fuel", "overseas_transport_distance", "overseas_trips",
                                                               "special_transport_distance", "special_transport_country", "special_transport_type", "special_vehicle_fuel", "special_trips"))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "下游運輸":
                    t_data = list(
                        downstream_transportation.objects.values("id", "device_id", "period_starttime", "period_endtime",
                                                                 "device_capacity", "position", "department",
                                                                 "january", "february", "march", "april",
                                                                 "may", "june", "july", "august",
                                                                 "september", "october", "november", "december"))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "員工通勤":
                    t_data = list(
                        employee_commute.objects.values("id", "employee_id", "department", "employee_name",
                                                        "transportation", "displacement", "city",
                                                        "township", "address", "commute_distance", "work_days"))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "員工出差":
                    t_data = list(
                        employee_business_trip.objects.values("id", "employee_id", "department", "employee_name",
                                                              "business_trip_location", "business_trip_date", "transportation",
                                                              "departure", "destination", "round_trip_distance"))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "廢棄物":
                    t_data = list(
                        waste.objects.values("id", "waste_name", "waste_date", "waste_weigh",
                                             "waste_disposal", "waste_location", "transport_responsibility",
                                             "transport_type", "transport_type", "transport_fuel", "transport_distance"))
                    return JsonResponse(t_data, safe=False)


# 抓欄位(字典
# @login_required(login_url="/login/")
# def load_table(request):
#     dict = {
#         "emergency_generators": ["id", "device_id", "period_starttime", 'period_endtime', 'device_capacity', "position", 'department', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'],
#         "combustion_equipment": "",
#         "official_car": "",
#         "material": "",
#         "process": "",
#         "refrigerator": "",
#         "airconditioner": "",
#         "vehicle": "",
#         "water_dispenser": "",
#         "ice_water_dispenser": "",
#         "ice_maker": "",
#         "other_device": "",
#         "refrigerant_total_table": "",
#         "extinguisher": "",
#         "personnel_inventory": "",
#         "security": "",
#         "electricity": "",
#         "upstream_transportation": "",
#         "downstream_transportation": "",
#         "employee_commute": "",
#         "employee_business": "",
#         "waste": ""
#     }
#     if request.method == 'GET':
#         device_id = request.GET.get('deviceId', None)
#         if device_id:
#             t_name = list(section_two.objects.filter(did=device_id).values("t_name"))
#             print("888888888", t_name)
#             for model in t_name:
#                 print("222222222222222222222222222222222222", model["t_name"])
#                 col = "id", "device_id"
#                 # tt = col.split(",")
#                 # print("test", tt)
#                 # 怎麼丟到values
#                 aa = emergency_generators.objects.filter().values(col)
#                 print("9999999999999999999999999999999999999", aa)
#                 t_data = list(globals()[model["t_name"]].objects.filter().all().values())
#                 print(t_data)
#                 return JsonResponse(t_data, safe=False)


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
def emergency_generators_edit(request, id=None, mode=None):
    if mode == "edit":
        unit = emergency_generators.objects.get(id=1)
        unit.device_id = request.GET['device_id']
        unit.period_starttime = request.GET['period_starttime']
        unit.period_endtime = request.GET['period_endtime']
        unit.device_capacity = request.GET['device_id']
        unit.position = request.GET['position']
        unit.department = request.GET['department']
        unit.january = request.GET['january']
        unit.february = request.GET['february']
        unit.march = request.GET['march']
        unit.april = request.GET['april']
        unit.may = request.GET['may']
        unit.june = request.GET['june']
        unit.july = request.GET['july']
        unit.august = request.GET['august']
        unit.september = request.GET['september']
        unit.october = request.GET['october']
        unit.november = request.GET['november']
        unit.december = request.GET['december']
        unit.image_note = request.GET['image_note']
        unit.image_path = request.GET['image_path']

        unit.save()

        return render(request, "home/emergency-generator.html", locals())

    # else:
    #     return render(request, "home/carbon-system.html", locals())


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
def carbon_system(request):
    return render(request, "home/carbon-system.html", locals())


# 新增轉跳
@login_required(login_url="/login/")
def add_page(request):
    global page
    if request.method == "GET":
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

        device_id = request.GET.get('deviceId', None)
        for a in htmlName:
            if device_id == a:
                page = htmlName.get(a)
        return render(request, page, locals())


# 新增title
@login_required(login_url="/login/")
def add_title(request):
    if request.method == 'GET':
        device_id = request.GET.get('deviceId', None)
        # 選擇title要顯示的欄位
        htmlName = {
            "1": {
                "內容": ["序號", "燃料開始日期", "燃料結束日期", "編號", "容量(𝓁)", "地點", "部門"],
                "加油量(單位:公升)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "合計"]
            },

            "2": {
                "內容": ["序號", "名稱", "編號", "燃料種類", "燃料開始日期", "燃料結束日期"],
                "使用量": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "合計"],
                "熱值(Kcal/kg)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "平均"]
            },

            "3": {
                "內容": ["序號", "類別", "編號", "燃料", "部門"],
                "加油量(單位:公升)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "合計"],
                "尿素": ["日期", "添加量(𝓁)"]
            },

            "4": {
                "內容": ["序號", "原物料號", "原/物料", "名稱"],
                "月用量(單位:公噸)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
            },

            "5": {
                "內容": ["序號", "製程階段", "料號", "製程添加物", "化學品名", "化學式", "CAS NO", "是否燃燒"],
                "使用量(單位:公斤)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
            },
            # 冷媒(6~13)
            "6": {
                "冰箱清單": ["序號", "名稱", "編號", "品牌", "型號", "年份", "位置", "冷媒類型", "規格填充量", "冷媒填充日", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "7": {
                "冷氣機清單": ["序號", "名稱", "編號", "品牌", "型號", "年份", "位置", "冷媒類型", "規格填充量", "冷媒填充日", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "8": {
                "車輛清單": ["序號", "名稱", "編號", "品牌", "型號", "年份", "位置", "冷媒類型", "規格填充量", "冷媒填充日", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "9": {
                "飲水機清單": ["序號", "名稱", "編號", "品牌", "型號", "年份", "位置", "冷媒類型", "規格填充量", "冷媒填充日", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "10": {
                "冰水機清單": ["序號", "名稱", "編號", "品牌", "型號", "年份", "位置", "冷媒類型", "規格填充量", "冷媒填充日", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "11": {
                "製冰機清單": ["序號", "名稱", "編號", "品牌", "型號", "年份", "位置", "冷媒類型", "規格填充量", "冷媒填充日", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "12": {
                "其他設備": ["序號", "名稱", "編號", "品牌", "型號", "年份", "位置", "冷媒類型", "規格填充量", "冷媒填充日", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "13": {
                "冷媒總表": ["序號", "名稱", "編號", "品牌", "型號", "年份", "位置", "冷媒類型", "規格填充量", "冷媒填充日", "維修填充量(kg)", "逸散率(%)", "逸散量"]
            },

            "14": {
                "滅火器清單": ["序號", "編號", "位置", "名稱", "類型", "廠商", "藥劑規格(單位:磅)", "藥劑重量(單位:kg)", "庫存量", "使用日期", "使用量", "更換/填充日期", "更換/填充量"]
            },

            "15": {
                "人天清冊": ["序號", "年份", "月份", "員工數", "每日工時", "每月工作天數", "加班+補修時數", "請假時數", "休假時數", "當月總工時", "當月總工作人天"]
            },

            "16": {
                "保全清冊": ["序號", "年份", "月份", "保全人數", "每日工時", "每月工作天數", "當月工時", "當月工作人天"]
            },

            "17": {
                "用電量": ["序號", "年份", "電表編號", "地址", "一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "小計(度)", "總計(千度)"]
            },

            "18": {
                "內容": ["序號", "驗收單號", "商品", "淨重量(單位:噸)", "客戶", "供應商名稱", "供應商地址", "貿易條件", "接貨地點", "送貨地點"],
                "陸運": ["單趟運輸距離(km)", "運輸國家", "方式", "燃料", "趟次", "T*km"],
                "海運": ["出貨港口", "到達港口", "海運距離", "趟次", "T*km"],
                "陸運(特殊)": ["單趟運輸距離(km)", "運輸國家", "方式", "燃料", "趟次", "T*km"]
            },

            "19": "home/downstream_transportation-table.html",

            "20": {
                "員工通勤清冊": ["序號", "編號", "部門", "姓名", "交通方式", "排氣量(CC數)", "居住城市", "鄉鎮市區", "行政區公家機關地址", "至公司距離(km)", "年工作天數", "距離合計"],
            },

            "21": {
                "員工出差清冊": ["序號", "編號", "部門", "姓名", "出差地點", "出差日期", "交通方式", "出發地", "目的地", "來回距離(pkm)"],
            },

            "22": {
                "廢棄物處理": ["序號", "名稱", "運送時間", "重量(噸)", "處理方式", "處置地點", "運輸責任歸屬", "運輸方式", "燃料", "運輸距離(km)", "T*km"],
            }
        }
    # a = request.GET.get('deviceId')
    # context = {'html': a}
    title = [htmlName.get(device_id)]
    # print('我好帥', context)
    # print("htmlName:::::::::::::::::::::::::::::::::::::::::::::::::::", context)
    # print('我好帥2', title)
    return JsonResponse(title, safe=False)
