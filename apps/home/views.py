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
            print("111111111111111111111111111111111111111111111111111111111", d_data)
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
            # allTable = list(emergency_generators.objects.all())
            # print("00000000000000000000000000000000000000", allTable)
            # allTable[0].total = 100
            # print("55555555555555555555555555555555555555", allTable[0].total)

            t_name = list(section_two.objects.filter(did=device_id).values("d_name"))
            # print("888888888", t_name)
            for a in t_name:
                if a["d_name"] == "緊急發電機":
                    t_data = list(
                        emergency_generators.objects.values("id", "device_id", "period_starttime", "period_endtime",
                                                            "device_capacity", "position", "department",
                                                            "january", "february", "march", "april",
                                                            "may", "june", "july", "august",
                                                            "september", "october", "november", "december"))
                    print("t_data::::::::::::::::::::::::::::::::::::::::::::::::", t_data)
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "燃燒設備":
                    t_data = list(combustion_equipment.objects.values("id", "device_id", "device_name", "fuel_type",
                                                                      "period_starttime", "period_endtime",
                                                                      "fuel_january", "fuel_february", "fuel_march",
                                                                      "fuel_april",
                                                                      "fuel_may", "fuel_june", "fuel_july",
                                                                      "fuel_august",
                                                                      "fuel_september", "fuel_october", "fuel_november",
                                                                      "fuel_december",
                                                                      "heat_january", "heat_february", "heat_march",
                                                                      "heat_april",
                                                                      "heat_may", "heat_june", "heat_july",
                                                                      "heat_august",
                                                                      "heat_september", "heat_october", "heat_november",
                                                                      "heat_december"))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "公務車":
                    t_data = list(
                        official_car.objects.values("id", "vehicle_type", "device_id", "fuel_type", "department",
                                                    "january", "february", "march", "april",
                                                    "may", "june", "july", "august",
                                                    "september", "october", "november", "december"))
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
                    t_data = list(
                        refrigerator.objects.values("id", "device_name", "brand_name", "model_type",
                                                    "years", "position", "refrigerant_type",
                                                    "filling_volume"))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "冷氣機清單":
                    t_data = list(
                        airconditioner.objects.values("id", "device_name", "device_id", "brand_name", "model_type",
                                                      "years", "position", "refrigerant_type",
                                                      "filling_volume", "effusion_rate"))
                    return JsonResponse(t_data, safe=False)
                # 以下未改
                elif a["d_name"] == "車輛清單":
                    t_data = list(
                        airconditioner.objects.values("id", "device_id", "period_starttime", "period_endtime",
                                                      "device_capacity", "position", "department",
                                                      "january", "february", "march", "april",
                                                      "may", "june", "july", "august",
                                                      "september", "october", "november", "december", ))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "飲水機清單":
                    t_data = list(
                        combustion_equipment.objects.values("id", "device_id", "period_starttime", "period_endtime",
                                                            "device_capacity", "position", "department",
                                                            "january", "february", "march", "april",
                                                            "may", "june", "july", "august",
                                                            "september", "october", "november", "december", ))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "冰水機清單":
                    t_data = list(
                        combustion_equipment.objects.values("id", "device_id", "period_starttime", "period_endtime",
                                                            "device_capacity", "position", "department",
                                                            "january", "february", "march", "april",
                                                            "may", "june", "july", "august",
                                                            "september", "october", "november", "december", ))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "製冰機清單":
                    t_data = list(
                        combustion_equipment.objects.values("id", "device_id", "period_starttime", "period_endtime",
                                                            "device_capacity", "position", "department",
                                                            "january", "february", "march", "april",
                                                            "may", "june", "july", "august",
                                                            "september", "october", "november", "december", ))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "其他設備清單":
                    t_data = list(
                        combustion_equipment.objects.values("id", "device_id", "period_starttime", "period_endtime",
                                                            "device_capacity", "position", "department",
                                                            "january", "february", "march", "april",
                                                            "may", "june", "july", "august",
                                                            "september", "october", "november", "december", ))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "冷媒總表":
                    t_data = list(
                        combustion_equipment.objects.values("id", "device_id", "period_starttime", "period_endtime",
                                                            "device_capacity", "position", "department",
                                                            "january", "february", "march", "april",
                                                            "may", "june", "july", "august",
                                                            "september", "october", "november", "december", ))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "滅火器":
                    t_data = list(
                        combustion_equipment.objects.values("id", "device_id", "period_starttime", "period_endtime",
                                                            "device_capacity", "position", "department",
                                                            "january", "february", "march", "april",
                                                            "may", "june", "july", "august",
                                                            "september", "october", "november", "december", ))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "人天清冊":
                    t_data = list(
                        combustion_equipment.objects.values("id", "device_id", "period_starttime", "period_endtime",
                                                            "device_capacity", "position", "department",
                                                            "january", "february", "march", "april",
                                                            "may", "june", "july", "august",
                                                            "september", "october", "november", "december", ))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "保全清單":
                    t_data = list(
                        combustion_equipment.objects.values("id", "device_id", "period_starttime", "period_endtime",
                                                            "device_capacity", "position", "department",
                                                            "january", "february", "march", "april",
                                                            "may", "june", "july", "august",
                                                            "september", "october", "november", "december", ))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "用電量":
                    t_data = list(
                        combustion_equipment.objects.values("id", "device_id", "period_starttime", "period_endtime",
                                                            "device_capacity", "position", "department",
                                                            "january", "february", "march", "april",
                                                            "may", "june", "july", "august",
                                                            "september", "october", "november", "december", ))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "上游運輸":
                    t_data = list(
                        combustion_equipment.objects.values("id", "device_id", "period_starttime", "period_endtime",
                                                            "device_capacity", "position", "department",
                                                            "january", "february", "march", "april",
                                                            "may", "june", "july", "august",
                                                            "september", "october", "november", "december", ))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "下游運輸":
                    t_data = list(
                        combustion_equipment.objects.values("id", "device_id", "period_starttime", "period_endtime",
                                                            "device_capacity", "position", "department",
                                                            "january", "february", "march", "april",
                                                            "may", "june", "july", "august",
                                                            "september", "october", "november", "december", ))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "員工通勤":
                    t_data = list(
                        combustion_equipment.objects.values("id", "device_id", "period_starttime", "period_endtime",
                                                            "device_capacity", "position", "department",
                                                            "january", "february", "march", "april",
                                                            "may", "june", "july", "august",
                                                            "september", "october", "november", "december", ))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "員工出差":
                    t_data = list(
                        combustion_equipment.objects.values("id", "device_id", "period_starttime", "period_endtime",
                                                            "device_capacity", "position", "department",
                                                            "january", "february", "march", "april",
                                                            "may", "june", "july", "august",
                                                            "september", "october", "november", "december", ))
                    return JsonResponse(t_data, safe=False)
                elif a["d_name"] == "廢棄物":
                    t_data = list(
                        combustion_equipment.objects.values("id", "device_id", "period_starttime", "period_endtime",
                                                            "device_capacity", "position", "department",
                                                            "january", "february", "march", "april",
                                                            "may", "june", "july", "august",
                                                            "september", "october", "november", "december", ))
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
def emergency_generator(request):
    EG_add = EGform(request.POST)

    return render(request, "home/emergency-generator.html", locals())

@login_required(login_url="/login/")
def combustion_equipment(request):
    CE_add = CEform(request.POST)

    return render(request, "home/combustion-equipment.html", locals())





@login_required(login_url="/login/")
def carbon_system(request):
    return render(request, "home/carbon-system.html", locals())


# 新增轉跳
@login_required(login_url="/login/")
def add_page(request):
    global page
    if request.method == "GET":
        htmlName = {
            "1": "home/emergency-generator.html",
            "2": "home/combustion-equipment.html",
            "3": "home/official-car.html",
            "4": "home/material.html",
            "6": "home/refrigerator.html",
            "7": "home/airconditioner.html",
            "8": "home/vehicle.html",
            "9": "home/vehicle.html",
            "10": "home/ice-water_dispenser.html",
            "11": "home/ice-maker.html",
            "12": "home/other-device.html",
            "13": "home/refrigerant-total_table.html",
            "14": "home/extinguisher.html",
            "15": "home/personnel-inventory.html",
            "16": "home/security.html",
            "17": "home/electricity.html",
            "18": "home/upstream-transportation.html",
            "19": "home/downstream-transportation.html",
            "20": "home/employee-commute.html",
            "21": "home/employee-business.html",
            "22": "home/waste.html",
            "data": "home/waste.html"
        }
        device_id = request.GET.get('deviceId', None)
        for a in htmlName:
            if device_id == a:
                print("-------------------------------------------", htmlName.get(a))
                page = htmlName.get(a)
        return render(request, page, locals())

# 新增title
@login_required(login_url="/login/")
def add_title(request):
    if request.method == 'GET':
        device_id = request.GET.get('deviceId', None)
        print("]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]", device_id)
        htmlName = {
            "1": {"內容": ["序號", "燃料開始日期", "燃料結束日期", "編號", "容量(𝓁)", "地點", "所屬單位"], "加油量(單位:公升)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]},
            "2": "home/combustion-equipment-table.html",
            "3": "home/official_car-table.html",
            "4": {"內容": ["序號", "原物料號", "原/物料", "名稱"], "月用量(單位:公噸)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]},
            "6": "home/refrigerator-table.html",
            "7": "home/airconditioner-table.html",
            "8": "home/vehicle-table.html",
            "9": "home/vehicle-table.html",
            "10": "home/ice_water_dispenser-table.html",
            "11": "home/ice_maker-table.html",
            "12": "home/other_device-table.html",
            "13": "home/refrigerant_total_table-table.html",
            "14": "home/extinguisher-table.html",
            "15": "home/personnel_inventory-table.html",
            "16": "home/security-table.html",
            "17": "home/electricity-table.html",
            "18": "home/upstream_transportation-table.html",
            "19": "home/downstream_transportation-table.html",
            "20": "home/employee_commute-table.html",
            "21": "home/employee_business-table.html",
            "22": "home/waste-table.html",
            "data": "home/waste-table.html"
        }
    # a = request.GET.get('deviceId')
    # context = {'html': a}
    context = htmlName.get(device_id)
    # print('我好帥', context)
    print("htmlName:::::::::::::::::::::::::::::::::::::::::::::::::::", context)
    title = [context]
    # print('我好帥2', title)
    return JsonResponse(title, safe=False)