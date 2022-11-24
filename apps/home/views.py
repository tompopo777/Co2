# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from json import dumps

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
from .forms import EGform
from apps.home.models import emergency_generators, section_one, section_two


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

@login_required(login_url="/login/")
def load_table(request):
    if request.method == 'GET':
        device_id = request.GET.get('deviceId', None)
        if device_id:
            t_name = list(section_two.objects.filter(did=device_id).values("t_name"))
            print("888888888", t_name)
            for model in t_name:
                print("222222222222222222222222222222222222", model["t_name"])

                test = model["t_name"][5:]
                total_data = globals()[test].objects.filter().all().values()
                # print("555555", total_data[0].__dict__)
                t_data = list(total_data)
                print(t_data)
                return JsonResponse(t_data, safe=False)

# # 抓欄位
# @login_required(login_url="/login/")
# def load_table(request):
#     if request.method == 'GET':
#         device_id = request.GET.get('deviceId', None)
#         if device_id:
#             # allTable = list(emergency_generators.objects.all())
#             # print("00000000000000000000000000000000000000", allTable)
#             # allTable[0].total = 100
#             # print("55555555555555555555555555555555555555", allTable[0].total)
#
#             t_name = list(section_two.objects.filter(did=device_id).values("d_name"))
#             # print("888888888", t_name)
#             for a in t_name:
#                 if a["d_name"] == "緊急發電機":
#                     t_data = list(emergency_generators.objects.values("device_id", "period_starttime", "period_endtime",
#                                                                       "device_capacity", "position", "department",
#                                                                       "january", "february", "march", "april",
#                                                                       "may", "june", "july", "august",
#                                                                       "september", "october", "november", "december"))
#                     # print("ttttttttttttttttttttttttt", t_data)
#                     return JsonResponse(t_data, safe=False)
#                 # elif a["d_name"] == "燃燒設備":
#                 #     t_data = list(emergency_generators.objects.values("device_id", "period_starttime", "period_endtime",
#                 #                                                       "device_capacity", "position", "department",
#                 #                                                       "january", "february", "march", "april",
#                 #                                                       "may", "june", "july", "august",
#                 #                                                       "september", "october", "november", "december", ))
#                 #     return JsonResponse(t_data, safe=False)
#
#             # from apps.home.models import t_data[0].table_name
#             # t_data[0].table_name__
#             # print("111111111111111111111111111111111111111111111111111111111", t_data)
#             # return JsonResponse(t_data, safe=False)
#

@login_required(login_url="/login/")
def emergency_generators_add(request):
    if request.method == "POST":
        EG_add = EGform(request.POST)
        if EG_add.is_valid():
            device_id = EG_add.cleaned_data['device_id']
            period_starttime = EG_add.cleaned_data['period_starttime']
            period_endtime = EG_add.cleaned_data['period_endtime']
            device_capacity = EG_add.cleaned_data['device_capacity']
            position = EG_add.cleaned_data['position']
            department = EG_add.cleaned_data['department']
            january = EG_add.cleaned_data['january']
            february = EG_add.cleaned_data['february']
            march = EG_add.cleaned_data['march']
            april = EG_add.cleaned_data['april']
            may = EG_add.cleaned_data['may']
            june = EG_add.cleaned_data['june']
            july = EG_add.cleaned_data['july']
            august = EG_add.cleaned_data['august']
            september = EG_add.cleaned_data['september']
            october = EG_add.cleaned_data['october']
            november = EG_add.cleaned_data['november']
            december = EG_add.cleaned_data['december']
            image_note = EG_add.cleaned_data['image_note']
            # image_path = EG_add.cleaned_data['image_path']

            unit = emergency_generators.objects.create(
                device_id=device_id,
                period_starttime=period_starttime,
                period_endtime=period_endtime,
                device_capacity=device_capacity,
                position=position,
                department=department,
                january=january,
                february=february,
                march=march,
                april=april,
                may=may,
                june=june,
                july=july,
                august=august,
                september=september,
                october=october,
                november=november,
                december=december,
                image_note=image_note,
                # image_path=image_path
            )

            unit.save()

            return redirect('/carbon-system/')


        else:
            message = '請完整填寫',
    else:
        message = '請輸入資料(資料不作驗證)'

    return render(request, "home/emergency-generators.html", locals())


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

    else:
        return render(request, "home/carbon-system.html", locals())


@login_required(login_url="/login/")
def combustion_equipment_add(request):
    if request.method == "POST":
        CE_add = CEform(request.POST)
        if CE_add.is_valid():
            device_name = CE_add.cleaned_data['device_name']
            device_id = CE_add.cleaned_data['device_id']
            fuel_type = CE_add.cleaned_data['fuel_type']
            period_starttime = CE_add.cleaned_data['period_starttime']
            period_endtime = CE_add.cleaned_data['period_endtime']
            january = CE_add.cleaned_data['january']
            february = CE_add.cleaned_data['february']
            march = CE_add.cleaned_data['march']
            april = CE_add.cleaned_data['april']
            may = CE_add.cleaned_data['may']
            june = CE_add.cleaned_data['june']
            july = CE_add.cleaned_data['july']
            august = CE_add.cleaned_data['august']
            september = CE_add.cleaned_data['september']
            october = CE_add.cleaned_data['october']
            november = CE_add.cleaned_data['november']
            december = CE_add.cleaned_data['december']
            image_note = CE_add.cleaned_data['image_note']
            image_path = CE_add.cleaned_data['image_path']

            unit = combustion_equipment.objects.create(
                device_name=device_name,
                device_id=device_id,
                fuel_type=fuel_type,
                period_starttime=period_starttime,
                period_endtime=period_endtime,
                fuel_january=fuel_january,
                fuel_february=fuel_february,
                fuel_march=fuel_march,
                fuel_april=fuel_april,
                fuel_may=fuel_may,
                fuel_june=fuel_june,
                fuel_july=fuel_july,
                fuel_august=fuel_august,
                fuel_september=fuel_september,
                fuel_october=fuel_october,
                fuel_november=fuel_november,
                fuel_december=fuel_december,
                heat_january=heat_january,
                heat_february=heat_february,
                heat_march=heat_march,
                heat_april=heat_april,
                heat_may=heat_may,
                heat_june=heat_june,
                heat_july=heat_july,
                heat_august=heat_august,
                heat_september=heat_september,
                heat_october=heat_october,
                heat_november=heat_november,
                heat_december=heat_december,
                image_note=image_note,
                image_path=image_path
            )

            unit.save()

            return redirect('/carbon-system/')
        else:
            message = '請完整填寫',
    else:
        message = '請輸入資料(資料不作驗證)'
        post = EGform()
    return render(request, "home/combustion-equipment.html", locals())



@login_required(login_url="/login/")
def emergency_generator(request):
    EG_add = EGform(request.POST)
    return render(request, "home/emergency-generator.html", locals())


@login_required(login_url="/login/")
def carbon_system(request):
    # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>0")
    #
    # if request.method == 'GET':
    #     currentClass = request.GET.get('cclass')
    #     if currentClass == None:
    #         currentClass = 0
    #     allProcess = section_one.objects.all()
    #         # filter(c_name=currentClass).values()
    #     selectProcess = allProcess.filter(c_name=currentClass)
    #     for a in selectProcess:
    #         print(">>>>>>>>>>>>>>>>>...", a.p_name)
    #     # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>2",selectProcess)
    #     context = {'allProcess': allProcess}
    return render(request, "home/carbon-system.html", locals())
