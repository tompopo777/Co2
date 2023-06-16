# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import django.contrib.auth.models
from django import template
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.urls import reverse, reverse_lazy
from decimal import *
from datetime import datetime
from .forms import *
from apps.home.models import *
from .csv import *


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/index.html')
    if request.user.groups.filter(name='公司帳號').exists():
        pass
    else:
        current_user = Profile.objects.filter(user_id=request.user.id).get()
        factory_id = current_user.factory_id
        request.session.update({'factory_id': factory_id})
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
        current_class = request.GET.get('currentClass')
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
        current_process = int(request.GET.get('currentProcess'))
        if current_process:
            d_data = list(section_two.objects.filter(cpid=current_process).values("d_name", "did"))
            return JsonResponse(d_data, safe=False)


# 判斷目前使用者在哪個group
def current_user_group_id(request):
    try:
        user_id = request.user.id
        current_user = Profile.objects.filter(user_id=user_id).get()
        factory_id = current_user.factory_id
        # factory_name = current_user.factory
        return factory_id
    except:
        pass


# 抓欄位(
@login_required(login_url="/login/")
def load_table(request):
    if request.method == 'GET':
        device_id = request.session.get('dropdown_three')
        year = request.session.get('years')
        # 判斷使用者是否為公司帳號。
        if request.user.groups.filter(name='公司帳號').exists():
            factory_id = request.session.get('company_id')
        else:
            factory_id = request.session.get('factory_id')
        t_name = list(section_two.objects.filter(did=device_id).values("d_name", "did"))
        # 從db撈每張表要顯示的值
        for a in t_name:
            if a["d_name"] == "柴油發電機":
                print(a["did"])
                t_data = []
                # raw_data = emergency_generators.objects.filter(company_id__in=factory_id_list, years=year).values("id", "device_id", "device_capacity", "position",
                raw_data = emergency_generators.objects.filter(company_id=factory_id, years=year).values("id", "device_id", "device_capacity", "position",
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
                    consumption_total = consumption_total.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
                    # 抓單筆資料
                    single_data.update(raw_data[i])
                    # 將計算後的加油量丟回字典
                    single_data["total"] = consumption_total
                    # 將 estimate 替換成中文
                    single_data["estimate"] = "是" if single_data["estimate"] else "否"
                    # 顯示有引用單據
                    if image.objects.filter(table_id=a["did"], single_id=raw_data[i].get('id')).exists():
                        single_data["image"] = "✔"
                    else:
                        single_data["image"] = None
                    t_data.append(single_data)

                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "燃燒設備":
                t_data = []
                # 「合計」前後的資料分開
                raw_data = combustion_equipment.objects.filter(company_id=factory_id, years=year).values("id", "device_name", "device_id", "fuel_type",
                                                                                                         "fuel_january", "fuel_february", "fuel_march", "fuel_april", "fuel_may", "fuel_june",
                                                                                                         "fuel_july", "fuel_august", "fuel_september", "fuel_october", "fuel_november", "fuel_december")
                heat_data = combustion_equipment.objects.filter(company_id=factory_id, years=year).values("heat_january", "heat_february", "heat_march", "heat_april", "heat_may", "heat_june",
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
                    Total_fuel = Total_fuel.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
                    avg_heat = avg_heat.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
                    # 將計算後的「合計」丟回字典
                    single_data["Total_fuel"] = Total_fuel
                    for j in heat_data[i]:
                        # 「合計」後的資料(每月熱值)丟回字典
                        single_data[j] = heat_data[i].get(j)
                    # 將計算後的「平均熱值」丟回字典
                    single_data["avg_heat"] = avg_heat
                    # 顯示有引用單據
                    if image.objects.filter(table_id=a["did"], single_id=raw_data[i].get('id')).exists():
                        single_data["image"] = "✔"
                    else:
                        single_data["image"] = None
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "公務車":
                t_data = []
                # 「合計」前後的資料分開抓
                raw_data = official_car.objects.filter(company_id=factory_id, years=year).values("id", "vehicle_type", "device_id", "fuel_type", "department", "metering_method")
                consumptions_data = official_car.objects.filter(company_id=factory_id, years=year).values("january", "february", "march", "april", "may", "june", "july", "august",
                                                                                                          "september", "october", "november", "december")

                urea_data = official_car.objects.filter(company_id=factory_id, years=year).values("urea_january", "urea_february", "urea_march", "urea_april",
                                                                                                  "urea_may", "urea_june", "urea_july", "urea_august",
                                                                                                  "urea_september", "urea_october", "urea_november", "urea_december")
                # 計算耗用量合計
                for i in range(raw_data.count()):
                    single_data = raw_data[i]
                    consumption_total = 0
                    for j in consumptions_data[i]:
                        # 「逐一」將資料(耗用量)丟回字典
                        single_data[j] = consumptions_data[i].get(j)
                        consumption_total += consumptions_data[i].get(j)
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
                        # 顯示有引用單據
                    if image.objects.filter(table_id=a["did"], single_id=raw_data[i].get('id')).exists():
                        single_data["image"] = "✔"
                    else:
                        single_data["image"] = None
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "原物料使用":
                t_data = list(
                    material.objects.filter(company_id=factory_id, years=year).values("id", "material_id", "material_type", "material_name",
                                                                                      "process_add_name", "chemical_name", "chemical_formula", "carbon_content",
                                                                                      "january", "february", "march", "april",
                                                                                      "may", "june", "july", "august",
                                                                                      "september", "october", "november", "december"))
                # 顯示有引用單據
                for raw_data in t_data:
                    if image.objects.filter(table_id=a["did"], single_id=raw_data.get('id')).exists():
                        raw_data["image"] = "✔"
                    else:
                        raw_data["image"] = None
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "製程添加化學品":
                t_data = []
                raw_data = process.objects.filter(company_id=factory_id, years=year).values("id", "process_stage", "material_id", "process_add_name",
                                                                                            "carbon_content", "burn", "VOCs",
                                                                                            "january", "february", "march", "april",
                                                                                            "may", "june", "july", "august",
                                                                                            "september", "october", "november", "december")
                unit = process.objects.filter(company_id=factory_id, years=year).values("unit")
                # 計算使用量合計
                for i in range(raw_data.count()):
                    consumption_total = raw_data[i].get("january") + raw_data[i].get("february") + raw_data[i].get("march") + raw_data[i].get("april") + \
                                        raw_data[i].get("may") + raw_data[i].get("june") + raw_data[i].get("july") + raw_data[i].get("august") + \
                                        raw_data[i].get("september") + raw_data[i].get("october") + raw_data[i].get("november") + raw_data[i].get("december")
                    # print("total::::::::::::::::::::::::::::::::::::::::", total)

                    single_data = raw_data[i]
                    # 將計算後的使用量丟回字典
                    consumption_total = consumption_total.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
                    single_data["total"] = consumption_total
                    # 將 estimate 替換成中文
                    single_data["burn"] = "是" if single_data["burn"] else "否"
                    single_data["VOCs"] = "是" if single_data["VOCs"] else "否"
                    # 將單位丟回字典
                    for j in unit[i]:
                        single_data[j] = unit[i].get(j)
                        # 顯示有引用單據
                    if image.objects.filter(table_id=a["did"], single_id=raw_data[i].get('id')).exists():
                        single_data["image"] = "✔"
                    else:
                        single_data["image"] = None
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "冰箱清單":
                t_data = []
                raw_data = refrigerator.objects.filter(company_id=factory_id, years=year).values("id", "device_id", "device_name", "brand_name", "model_type", "position",
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
                    effusion_volume = effusion_volume.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
                    single_data["effusion_volume"] = effusion_volume
                    # 顯示有引用單據
                    if image.objects.filter(table_id=a["did"], single_id=raw_data[i].get('id')).exists():
                        single_data["image"] = "✔"
                    else:
                        single_data["image"] = None
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "冷氣機清單":
                t_data = []
                raw_data = airconditioner.objects.filter(company_id=factory_id, years=year).values("id", "device_id", "device_name", "brand_name", "model_type", "position",
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
                    effusion_volume = effusion_volume.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
                    single_data["effusion_volume"] = effusion_volume
                    # 顯示有引用單據
                    if image.objects.filter(table_id=a["did"], single_id=raw_data[i].get('id')).exists():
                        single_data["image"] = "✔"
                    else:
                        single_data["image"] = None
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "車輛清單":
                t_data = []
                raw_data = vehicle.objects.filter(company_id=factory_id, years=year).values("id", "device_id", "device_name", "brand_name", "model_type", "position",
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
                    effusion_volume = effusion_volume.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
                    single_data["effusion_volume"] = effusion_volume
                    # 顯示有引用單據
                    if image.objects.filter(table_id=a["did"], single_id=raw_data[i].get('id')).exists():
                        single_data["image"] = "✔"
                    else:
                        single_data["image"] = None
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "飲水機清單":
                t_data = []
                raw_data = water_dispenser.objects.filter(company_id=factory_id, years=year).values("id", "device_id", "device_name", "brand_name", "model_type", "position",
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
                    effusion_volume = effusion_volume.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
                    single_data["effusion_volume"] = effusion_volume
                    # 顯示有引用單據
                    if image.objects.filter(table_id=a["did"], single_id=raw_data[i].get('id')).exists():
                        single_data["image"] = "✔"
                    else:
                        single_data["image"] = None
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "冰水機清單":
                t_data = []
                raw_data = ice_water_dispenser.objects.filter(company_id=factory_id, years=year).values("id", "device_id", "device_name", "brand_name", "model_type", "position",
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
                    effusion_volume = effusion_volume.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
                    single_data["effusion_volume"] = effusion_volume
                    # 顯示有引用單據
                    if image.objects.filter(table_id=a["did"], single_id=raw_data[i].get('id')).exists():
                        single_data["image"] = "✔"
                    else:
                        single_data["image"] = None
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "製冰機清單":
                t_data = []
                raw_data = ice_maker.objects.filter(company_id=factory_id, years=year).values("id", "device_id", "device_name", "brand_name", "model_type", "position",
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
                    effusion_volume = effusion_volume.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
                    single_data["effusion_volume"] = effusion_volume
                    # 顯示有引用單據
                    if image.objects.filter(table_id=a["did"], single_id=raw_data[i].get('id')).exists():
                        single_data["image"] = "✔"
                    else:
                        single_data["image"] = None
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "設備清單":
                t_data = []
                raw_data = other_device.objects.filter(company_id=factory_id, years=year).values("id", "device_id", "device_name", "brand_name", "model_type", "position",
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
                    effusion_volume = effusion_volume.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
                    single_data["effusion_volume"] = effusion_volume
                    # 顯示有引用單據
                    if image.objects.filter(table_id=a["did"], single_id=raw_data[i].get('id')).exists():
                        single_data["image"] = "✔"
                    else:
                        single_data["image"] = None
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "滅火器":
                t_data = list(
                    extinguisher.objects.filter(company_id=factory_id, years=year).values("id", "device_id", "extinguisher_vendor", "extinguisher_type", "position", "inventory",
                                                                                          "chemical_weight", "using_amount", "monthly", "replace_filling_amount", "replace_filling_date"))
                # 顯示有引用單據
                for raw_data in t_data:
                    if image.objects.filter(table_id=a["did"], single_id=raw_data.get('id')).exists():
                        raw_data["image"] = "✔"
                    else:
                        raw_data["image"] = None
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "人天清冊":
                t_data = list(
                    personnel_inventory.objects.filter(company_id=factory_id, years=year).values("id", "classification",
                                                                                                 "WKhours_january", "WKhours_february", "WKhours_march", "WKhours_april", "WKhours_may", "WKhours_june",
                                                                                                 "WKhours_july", "WKhours_august", "WKhours_september", "WKhours_october", "WKhours_november", "WKhours_december",
                                                                                                 "WKnum_january", "WKnum_february", "WKnum_march", "WKnum_april", "WKnum_may", "WKnum_june",
                                                                                                 "WKnum_july", "WKnum_august", "WKnum_september", "WKnum_october", "WKnum_november", "WKnum_december"))
                # 顯示有引用單據
                for raw_data in t_data:
                    if image.objects.filter(table_id=a["did"], single_id=raw_data.get('id')).exists():
                        raw_data["image"] = "✔"
                    else:
                        raw_data["image"] = None
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "委外人員清冊":
                t_data = list(
                    employee.objects.filter(company_id=factory_id, years=year).values("id", "career",
                                                                                      "employeeNum_january", "employeeNum_february", "employeeNum_march", "employeeNum_april", "employeeNum_may", "employeeNum_june",
                                                                                      "employeeNum_july", "employeeNum_august", "employeeNum_september", "employeeNum_october", "employeeNum_november", "employeeNum_december",
                                                                                      "WKdays_january", "WKdays_february", "WKdays_march", "WKdays_april", "WKdays_may", "WKdays_june", "WKdays_july", "WKdays_august",
                                                                                      "WKdays_september", "WKdays_october", "WKdays_november", "WKdays_december",
                                                                                      "WKhours_january", "WKhours_february", "WKhours_march", "WKhours_april", "WKhours_may", "WKhours_june", "WKhours_july",
                                                                                      "WKhours_august", "WKhours_september", "WKhours_october", "WKhours_november", "WKhours_december"))
                # 顯示有引用單據
                for raw_data in t_data:
                    if image.objects.filter(table_id=a["did"], single_id=raw_data.get('id')).exists():
                        raw_data["image"] = "✔"
                    else:
                        raw_data["image"] = None
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "廢水":
                t_data = []
                raw_data = waste_water.objects.filter(company_id=factory_id, years=year).values("id", "Pi", "Wi", "CODi", "Si", "MCFj", "Bo", "Ri", "COD_total")
                # 計算加油量合計
                for i in range(raw_data.count()):
                    single_data = {}
                    Pi = raw_data[i].get("Pi")
                    Wi = "{:.10f}".format(raw_data[i].get("Wi"))
                    CODi = "{:.10f}".format(raw_data[i].get("CODi"))
                    COD_total = "{:.10f}".format(raw_data[i].get("COD_total"))
                    Si = "{:.10f}".format(raw_data[i].get("Si"))
                    MCFj = "{:.10f}".format(raw_data[i].get("MCFj"))
                    Bo = "{:.10f}".format(raw_data[i].get("Bo"))
                    Ri = "{:.10f}".format(raw_data[i].get("Ri"))

                    if Pi is not None:
                        Pi = "{:.10f}".format(Pi)
                        ch4 = (((raw_data[i].get("Pi") * raw_data[i].get("Wi") * raw_data[i].get("CODi")) - (raw_data[i].get("Si"))) * (raw_data[i].get("Bo") * raw_data[i].get("MCFj"))) - raw_data[i].get("Ri")
                        consumption_total = ch4.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
                    else:
                        ch4 = (((raw_data[i].get("Wi") * raw_data[i].get("CODi")) - (raw_data[i].get("Si"))) * (raw_data[i].get("Bo") * raw_data[i].get("MCFj"))) - raw_data[i].get("Ri")
                        consumption_total = ch4.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
                    # 抓單筆資料
                    single_data.update(raw_data[i])
                    # 將計算後的加油量丟回字典
                    single_data["Pi"] = Pi
                    single_data["Wi"] = Wi
                    single_data["CODi"] = CODi
                    single_data["COD_total"] = COD_total
                    single_data["Si"] = Si
                    single_data["MCFj"] = MCFj
                    single_data["Bo"] = Bo
                    single_data["Ri"] = Ri
                    single_data["ch4"] = consumption_total
                    t_data.append(single_data)

                    # for i in range(raw_data.count()):
                    #     cod_total = (raw_data[i].get("Pi") * raw_data[i].get("Wi") * raw_data[i].get("CODi") - raw_data[i].get("Si")) * (raw_data[i].get("Bo") * raw_data[i].get("MCFj")) - raw_data[i].get("Ri")
                    #     raw_data[i]["CH4"] = cod_total
                    # print(raw_data)
                    # t_data.append(raw_data)
                    # t_data = list(waste_water.objects.filter(company_id=factory_id, years=year).values("id", "Pi", "Wi", "CODi", "COD_total", "Si", "MCFj", "Bo", "Ri"))
                    # 顯示有引用單據
                    if image.objects.filter(table_id=a["did"], single_id=raw_data[i].get('id')).exists():
                        single_data["image"] = "✔"
                    else:
                        single_data["image"] = None
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "廢汙泥":
                t_data = list(
                    waste_sludge.objects.filter(company_id=factory_id, years=year).values("id", "waste_sludge_treatment_name", "waste_sludge_inflow_rate", "average_inlet_MLSS_concentration",
                                                                                          "CH4_capture_system_rate", "combustion_equipment_efficiency"))
                # 顯示有引用單據
                for raw_data in t_data:
                    if image.objects.filter(table_id=a["did"], single_id=raw_data.get('id')).exists():
                        raw_data["image"] = "✔"
                    else:
                        raw_data["image"] = None
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "溶劑、噴霧劑":
                t_data = list(solvent_aerosol_emission_sources.objects.filter(company_id=factory_id, years=year).values("id", "solvent_name", "solvent_amount", "solvent_capacity", "solvent_capacity_unit", "gas_name", "gas_ratio", "density"))
                # 顯示有引用單據
                for raw_data in t_data:
                    if image.objects.filter(table_id=a["did"], single_id=raw_data.get('id')).exists():
                        raw_data["image"] = "✔"
                    else:
                        raw_data["image"] = None
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "用電量":
                t_data = []
                # 將要運算的值分別撈出(逸散率/填充量)
                raw_data = electricity.objects.filter(company_id=factory_id, years=year).values("id", "EMI_id", "address",
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
                    kw_hr = kw_hr.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
                    kkw_hr = kkw_hr.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
                    single_data["kw_hr"] = kw_hr
                    single_data["kkw_hr"] = kkw_hr
                    # 顯示有引用單據
                    if image.objects.filter(table_id=a["did"], single_id=raw_data[i].get('id')).exists():
                        single_data["image"] = "✔"
                    else:
                        single_data["image"] = None
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "上游運輸":
                t_data = list(
                    upstream_transportation.objects.filter(company_id=factory_id, years=year).values("id", "acceptance_receipt", "commodity_name", "weight", "commodity_NW",
                                                                                                     "organizational_use_products", "customer", "supplier", "supplier_address",
                                                                                                     "trade_term", "receiving_address", "delivery_address",
                                                                                                     "transport_distance", "transport_country", "transport_type", "transport_fuel", "paid", "trips",
                                                                                                     "overseas_transport_distance", "overseas_delivery", "overseas_arrive", "overseas_paid", "overseas_trips",
                                                                                                     "special_transport_distance", "special_transport_country", "special_transport_type", "special_transport_fuel", "special_paid", "special_trips",
                                                                                                     "air_transport_distance", "air_delivery", "air_arrive", "air_paid", "air_trips"))
                # 顯示有引用單據
                for raw_data in t_data:
                    if image.objects.filter(table_id=a["did"], single_id=raw_data.get('id')).exists():
                        raw_data["image"] = "✔"
                    else:
                        raw_data["image"] = None
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "下游運輸":
                t_data = list(
                    downstream_transportation.objects.filter(company_id=factory_id, years=year).values("id", "acceptance_receipt", "commodity_name", "weight", "commodity_NW", "customer", "supplier", "supplier_address",
                                                                                                       "trade_term", "receiving_address", "delivery_address",
                                                                                                       "transport_distance", "transport_country", "transport_type", "transport_fuel", "paid", "trips",
                                                                                                       "overseas_transport_distance", "overseas_delivery", "overseas_arrive", "overseas_paid", "overseas_trips",
                                                                                                       "special_transport_distance", "special_transport_country", "special_transport_type", "special_transport_fuel", "special_paid", "special_trips",
                                                                                                       "air_transport_distance", "air_delivery", "air_arrive", "air_paid", "air_trips"))
                # 顯示有引用單據
                for raw_data in t_data:
                    if image.objects.filter(table_id=a["did"], single_id=raw_data.get('id')).exists():
                        raw_data["image"] = "✔"
                    else:
                        raw_data["image"] = None
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "員工通勤":
                t_data = []
                # 將要運算的值分別撈出(員工數/每日工時/每月工作天數/加班+補休時數/請假時數/休假時數)
                pre_data = employee_commute.objects.filter(company_id=factory_id, years=year).values("id", "employee_id", "department", "employee_name")
                post_data = employee_commute.objects.filter(company_id=factory_id, years=year).values("city", "township", "address", "commute_distance", "work_days")
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
                raw_data = employee_business_trip.objects.filter(company_id=factory_id, years=year).values("id", "business_trip_number", "employee_id", "department", "employee_name", "business_trip_location", "business_trip_date")
                for i in range(raw_data.count()):
                    single_data = raw_data[i]
                    id = raw_data[i].get("id")
                    section = trip_section.objects.filter(trip_id=id).values("transportation", "distance")
                    transportation_dic = {"自駕汽車": Decimal('0'), "高鐵": Decimal('0'), "火車(電聯)": Decimal('0'), "火車(柴聯)": Decimal('0'), "計程車": Decimal('0'), "機車": Decimal('0'), "捷運": Decimal('0'), "飛機": Decimal('0'), "船舶": Decimal('0')}
                    for s in section:
                        way = s.get("transportation")
                        if way in transportation_dic:
                            transportation_dic[way] += (s.get("distance"))
                        for d in transportation_dic:
                            if transportation_dic.get(d) == 0:
                                single_data[d] = None
                            else:
                                single_data[d] = round(transportation_dic.get(d), 4)
                                # 顯示有引用單據
                    if image.objects.filter(table_id=a["did"], single_id=raw_data[i].get('id')).exists():
                        single_data["image"] = "✔"
                    else:
                        single_data["image"] = None
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "廢棄物":
                t_data = []
                raw_data = waste.objects.filter(company_id=factory_id, years=year).values("id", "waste_name", "waste_weigh", "waste_date",
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
                    # 顯示有引用單據
                    if image.objects.filter(table_id=a["did"], single_id=raw_data[i].get('id')).exists():
                        single_data["image"] = "✔"
                    else:
                        single_data["image"] = None
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "VOCs_1":
                t_data = list(VOCs_one.objects.filter(company_id=factory_id, years=year).values("id", "emission", "concentration_ch4"))
                # 顯示有引用單據
                for raw_data in t_data:
                    if image.objects.filter(table_id=a["did"], single_id=raw_data.get('id')).exists():
                        raw_data["image"] = "✔"
                    else:
                        raw_data["image"] = None
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "VOCs_2":
                t_data = list(VOCs_two.objects.filter(company_id=factory_id, years=year).values("id", "disposal_volume", "concentration_ch4", "voc_capture_rate", "combustion_equipment_rate",
                                                                                                "concentration_entrance", "concentration_exit", "builtIn_rate", "custom_rate"))
                # 顯示有引用單據
                for raw_data in t_data:
                    if image.objects.filter(table_id=a["did"], single_id=raw_data.get('id')).exists():
                        raw_data["image"] = "✔"
                    else:
                        raw_data["image"] = None
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "納管廢水排放量":
                t_data = []
                raw_data = pipe_wastewater.objects.filter(company_id=factory_id, years=year).values("id", "pipe_id", "address", "factory", "january", "february", "march", "april", "may", "june", "july", "august",
                                                                                                    "september", "october", "november", "december")
                # 計算當月排放量
                for i in range(raw_data.count()):
                    Total_Emission = raw_data[i].get("january") + raw_data[i].get("february") + raw_data[i].get("march") + raw_data[i].get("april") + \
                                     raw_data[i].get("may") + raw_data[i].get("june") + raw_data[i].get("july") + raw_data[i].get("august") + \
                                     raw_data[i].get("september") + raw_data[i].get("october") + raw_data[i].get("november") + raw_data[i].get("december")
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    Total_Emission = Total_Emission.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
                    single_data["Total_Emission"] = Total_Emission
                    # 顯示有引用單據
                    if image.objects.filter(table_id=a["did"], single_id=raw_data[i].get('id')).exists():
                        single_data["image"] = "✔"
                    else:
                        single_data["image"] = None
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "採購原物料":
                t_data = []
                raw_data = purchase_material.objects.filter(company_id=factory_id, years=year).values("id", "product_id", "product_name", "vendor", "category_name", "material_type",
                                                                                                      "january", "february", "march", "april", "may", "june", "july", "august",
                                                                                                      "september", "october", "november", "december")
                # 計算當月排放量
                for i in range(raw_data.count()):
                    Total_Purchase = raw_data[i].get("january") + raw_data[i].get("february") + raw_data[i].get("march") + raw_data[i].get("april") + \
                                     raw_data[i].get("may") + raw_data[i].get("june") + raw_data[i].get("july") + raw_data[i].get("august") + \
                                     raw_data[i].get("september") + raw_data[i].get("october") + raw_data[i].get("november") + raw_data[i].get("december")
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    Total_Purchase = Total_Purchase.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
                    single_data["Total_Purchase"] = Total_Purchase
                    # 顯示有引用單據
                    if image.objects.filter(table_id=a["did"], single_id=raw_data[i].get('id')).exists():
                        single_data["image"] = "✔"
                    else:
                        single_data["image"] = None
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)
            elif a["d_name"] == "產品間接排放":
                t_data = []
                raw_data = product_indirect_emissions.objects.filter(company_id=factory_id, years=year).values("id", "product_id", "product_name", "january", "february", "march", "april", "may", "june", "july", "august",
                                                                                                               "september", "october", "november", "december")
                # 計算當月排放量
                for i in range(raw_data.count()):
                    Total_Deliver = raw_data[i].get("january") + raw_data[i].get("february") + raw_data[i].get("march") + raw_data[i].get("april") + \
                                    raw_data[i].get("may") + raw_data[i].get("june") + raw_data[i].get("july") + raw_data[i].get("august") + \
                                    raw_data[i].get("september") + raw_data[i].get("october") + raw_data[i].get("november") + raw_data[i].get("december")
                    # 抓單筆資料
                    single_data = raw_data[i]
                    # 將計算後的逸散量丟回字典
                    Total_Deliver = Total_Deliver.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
                    single_data["Total_Deliver"] = Total_Deliver
                    # 顯示有引用單據
                    if image.objects.filter(table_id=a["did"], single_id=raw_data[i].get('id')).exists():
                        single_data["image"] = "✔"
                    else:
                        single_data["image"] = None
                    t_data.append(single_data)
                return JsonResponse(t_data, safe=False)


@permission_required('home.add_emergency_generators', login_url="/login/", raise_exception=True)
def copy_last_year_data(request):
    if request.method == 'GET':
        device_id = request.session.get('dropdown_three')
        factory_id = request.session.get('factory_id')
        t_name = list(section_two.objects.filter(did=device_id).values("d_name"))
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

        # 獲取當前年份
        this_year = datetime.now().year
        # 獲取去年年份
        last_year = this_year - 1

        model = modelName.get(str(device_id))
        if model:
            last_year_data = model.objects.filter(company_id=factory_id, years=last_year).values()
            # 如果去年沒有資料，顯示 alert 訊息
            if not last_year_data:
                response_data = {
                    'success': False,
                    'copy_data_message': f'{last_year}年沒有任何資料！'
                }
                return response_data

            # 檢查當前年份是否已有資料
            if model.objects.filter(company_id=factory_id, years=this_year).exists():
                response_data = {
                    'success': False,
                    'copy_data_message': f'{this_year}年資料已存在！'
                }
                return response_data

                # # 檢查逐筆資料是否已存在
                # copied_data_count = 0
                # skipped_data_count = 0
                # for data in last_year_data:
                #     data.pop('id')  # 刪除主鍵
                #     data['years'] = this_year
                #
                #     # 檢查逐筆資料是否已存在
                #     if model.objects.filter(company_id=factory_id, years=this_year, **data).exists():
                #         skipped_data_count += 1
                #         continue  # 跳過已存在的資料
                #
                #     # 儲存逐筆資料到資料庫
                #     model.objects.create(**data)
                #     copied_data_count += 1

            # 將年份改為今年
            for data in last_year_data:
                data.pop('id')  # 刪除主鍵
                data['years'] = this_year

            # 將資料儲存回資料庫中
            model.objects.bulk_create(
                [model(**data) for data in last_year_data]
            )

            # 回傳 alert 訊息
            response_data = {
                'success': True,  # 也可以改為 False
                'copy_data_message': f'{last_year}年資料複製成功！'
            }
            return response_data
        else:
            print(f"未找到對應的模型類別: {t_name}")

        # for a in t_name:
        #     if a["d_name"] == "柴油發電機":
        #         last_year_data = emergency_generators.objects.filter(years=last_year).filter(company_id=factory_id).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         emergency_generators.objects.bulk_create(
        #             [emergency_generators(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '燃燒設備':
        #         last_year_data = combustion_equipment.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         combustion_equipment.objects.bulk_create(
        #             [combustion_equipment(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '公務車':
        #         last_year_data = official_car.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         official_car.objects.bulk_create(
        #             [official_car(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '原物料使用':
        #         last_year_data = material.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         material.objects.bulk_create(
        #             [material(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '製程添加化學品':
        #         last_year_data = process.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         process.objects.bulk_create(
        #             [process(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '冰箱清單':
        #         last_year_data = refrigerator.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         refrigerator.objects.bulk_create(
        #             [refrigerator(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '冷氣機清單':
        #         last_year_data = airconditioner.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         airconditioner.objects.bulk_create(
        #             [airconditioner(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '車輛清單':
        #         last_year_data = vehicle.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         vehicle.objects.bulk_create(
        #             [vehicle(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '飲水機清單':
        #         last_year_data = water_dispenser.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         water_dispenser.objects.bulk_create(
        #             [water_dispenser(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '冰水機清單':
        #         last_year_data = ice_water_dispenser.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         ice_water_dispenser.objects.bulk_create(
        #             [ice_water_dispenser(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '製冰機清單':
        #         last_year_data = ice_maker.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         ice_maker.objects.bulk_create(
        #             [ice_maker(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '設備清單':
        #         last_year_data = other_device.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         other_device.objects.bulk_create(
        #             [other_device(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '滅火器':
        #         last_year_data = extinguisher.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         extinguisher.objects.bulk_create(
        #             [extinguisher(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '人添清冊':
        #         last_year_data = personnel_inventory.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         personnel_inventory.objects.bulk_create(
        #             [personnel_inventory(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '委外人員清冊':
        #         last_year_data = employee.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         employee.objects.bulk_create(
        #             [employee(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '厭氧廢水':
        #         last_year_data = waste_water.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         waste_water.objects.bulk_create(
        #             [waste_water(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '廢汙泥':
        #         last_year_data = waste_sludge.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         waste_sludge.objects.bulk_create(
        #             [waste_sludge(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '溶劑、噴霧劑':
        #         last_year_data = solvent_aerosol_emission_sources.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         solvent_aerosol_emission_sources.objects.bulk_create(
        #             [solvent_aerosol_emission_sources(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == 'VOCs_1':
        #         last_year_data = VOCs_one.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         VOCs_one.objects.bulk_create(
        #             [VOCs_one(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == 'VOCs_2':
        #         last_year_data = VOCs_two.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         VOCs_two.objects.bulk_create(
        #             [VOCs_two(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '用電量':
        #         last_year_data = electricity.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         electricity.objects.bulk_create(
        #             [electricity(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '上游運輸':
        #         last_year_data = upstream_transportation.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         upstream_transportation.objects.bulk_create(
        #             [upstream_transportation(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '下游運輸':
        #         last_year_data = downstream_transportation.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         downstream_transportation.objects.bulk_create(
        #             [downstream_transportation(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '員工通勤':
        #         # 抓取母表資料
        #         last_year_commute_data = employee_commute.objects.filter(company_id=factory_id, years=last_year).values()
        #         last_year_commute_data_id = list(last_year_commute_data.values_list('id', flat=True))
        #         last_year_transport_data = transportation_way.objects.filter(commute_id__in=last_year_commute_data_id).values()
        #
        #         # 如果去年沒有母表資料，顯示 alert 訊息
        #         if not last_year_commute_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #
        #         commute_id_dict = {}
        #         new_commute_data = []
        #         new_transportation_data = []
        #
        #         for data in last_year_commute_data:
        #             original_id = data['id']  # 記錄原本的id
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #             new_commute = employee_commute.objects.create(**data)
        #             new_commute_data.append(new_commute)
        #             commute_id_dict[original_id] = new_commute.id  # 將原本的id和新的id建立對應關係
        #
        #         # 將資料儲存回資料庫中
        #         for data in last_year_transport_data:
        #             original_commute_id = data['commute_id']
        #             new_commute_id = commute_id_dict[original_commute_id]
        #             data.pop('id')  # 刪除主鍵
        #             data['commute_id'] = new_commute_id
        #             new_transportation = transportation_way(**data)
        #             new_transportation_data.append(new_transportation)
        #
        #         # 儲存新的子表資料到資料庫中
        #         transportation_way.objects.bulk_create(new_transportation_data)
        #
        #     elif a["d_name"] == '員工出差':
        #         last_year_data = employee_business_trip.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         employee_business_trip.objects.bulk_create(
        #             [employee_business_trip(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '廢棄物':
        #         last_year_data = waste.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         waste.objects.bulk_create(
        #             [waste(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '納管廢水排放量':
        #         last_year_data = pipe_wastewater.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         pipe_wastewater.objects.bulk_create(
        #             [pipe_wastewater(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '採購原物料':
        #         last_year_data = purchase_material.objects.filter(years=last_year, company_id=factory_id).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         purchase_material.objects.bulk_create(
        #             [purchase_material(**data) for data in last_year_data]
        #         )
        #     elif a["d_name"] == '產品間接排放':
        #         last_year_data = product_indirect_emissions.objects.filter(company_id=factory_id, years=last_year).values()
        #         # 如果去年沒有資料，顯示 alert 訊息
        #         if not last_year_data:
        #             response_data = {
        #                 'success': False,
        #                 'message': f'{last_year}年沒有任何資料！'
        #             }
        #             return JsonResponse(response_data)
        #         # 將年份改為今年
        #         for data in last_year_data:
        #             data.pop('id')  # 刪除主鍵
        #             data['years'] = this_year
        #         # 將資料儲存回資料庫中
        #         product_indirect_emissions.objects.bulk_create(
        #             [product_indirect_emissions(**data) for data in last_year_data]
        #         )
        #
        # # 回傳 alert 訊息
        # response_data = {
        #     'success': True,  # 也可以改為 False
        #     'message': f'{last_year}年資料複製成功！'
        # }
        # return response_data
        # return JsonResponse(response_data)


@login_required(login_url="/login/")
def emergency_generators_add(request):
    context = {}
    EG_add = EGform(request)
    if request.method == "POST":
        EG_add = EGform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if EG_add.is_valid():
            EG_add = EG_add.save(commit=False)
            EG_add.company_id = factory_id
            EG_add.years = request.session.get('years')
            EG_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = emergency_generators.objects.values("id").last().get("id")
            table_id = emergency_generators.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/emergency_generators_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", EG_add.errors)
    context['EG_add'] = EG_add
    context['years'] = request.session.get('years')
    return render(request, 'home/emergency-generator.html', context)


@login_required(login_url="/login/")
def combustion_equipment_add(request):
    context = {}
    CE_add = CEform(request)
    if request.method == "POST":
        CE_add = CEform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if CE_add.is_valid():
            CE_add = CE_add.save(commit=False)
            CE_add.company_id = factory_id
            CE_add.years = request.session.get('years')
            CE_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = combustion_equipment.objects.values("id").last().get("id")
            table_id = combustion_equipment.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/combustion_equipment_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", CE_add.errors)
    context['CE_add'] = CE_add
    context['years'] = request.session.get('years')
    return render(request, 'home/combustion-equipment.html', context)


@login_required(login_url="/login/")
# _add標準寫法
def official_car_add(request):
    context = {}
    OffCar_add = OFform(request)
    if request.method == "POST":
        OffCar_add = OFform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if OffCar_add.is_valid():
            OffCar_add = OffCar_add.save(commit=False)
            OffCar_add.company_id = factory_id
            OffCar_add.years = request.session.get('years')
            OffCar_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = official_car.objects.values("id").last().get("id")
            table_id = official_car.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/official_car_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", OffCar_add.errors)
    context['OffCar_add'] = OffCar_add
    context['years'] = request.session.get('years')
    return render(request, 'home/official-car.html', context)


@login_required(login_url="/login/")
def material_add(request):
    context = {}
    MT_add = MTform(request)
    if request.method == "POST":
        MT_add = MTform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if MT_add.is_valid():
            MT_add = MT_add.save(commit=False)
            MT_add.company_id = factory_id
            MT_add.years = request.session.get('years')
            MT_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = material.objects.values("id").last().get("id")
            table_id = material.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/material_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", MT_add.errors)
    context['MT_add'] = MT_add
    context['years'] = request.session.get('years')
    return render(request, 'home/material.html', context)


@login_required(login_url="/login/")
def process_add(request):
    context = {}
    PC_add = PCform(request)
    if request.method == "POST":
        PC_add = PCform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if PC_add.is_valid():
            PC_add = PC_add.save(commit=False)
            PC_add.company_id = factory_id
            PC_add.years = request.session.get('years')
            PC_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = process.objects.values("id").last().get("id")
            table_id = process.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/process_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", PC_add.errors)
    context['PC_add'] = PC_add
    context['years'] = request.session.get('years')
    return render(request, 'home/process.html', context)


@login_required(login_url="/login/")
def refrigerator_add(request):
    context = {}
    RF_add = RFform(request)
    if request.method == "POST":
        RF_add = RFform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if RF_add.is_valid():
            RF_add = RF_add.save(commit=False)
            RF_add.company_id = factory_id
            RF_add.years = request.session.get('years')
            RF_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = refrigerator.objects.values("id").last().get("id")
            table_id = refrigerator.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/refrigerator_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", RF_add.errors)
    context['RF_add'] = RF_add
    context['years'] = request.session.get('years')
    return render(request, 'home/refrigerator.html', context)


@login_required(login_url="/login/")
def airconditioner_add(request):
    context = {}
    AC_add = ACform(request)
    if request.method == "POST":
        AC_add = ACform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if AC_add.is_valid():
            AC_add = AC_add.save(commit=False)
            AC_add.company_id = factory_id
            AC_add.years = request.session.get('years')
            AC_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = airconditioner.objects.values("id").last().get("id")
            table_id = airconditioner.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/airconditioner_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", AC_add.errors)
    context['AC_add'] = AC_add
    context['years'] = request.session.get('years')
    return render(request, 'home/airconditioner.html', context)


@login_required(login_url="/login/")
def vehicle_add(request):
    context = {}
    VC_add = VCform(request)
    if request.method == "POST":
        VC_add = VCform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if VC_add.is_valid():
            VC_add = VC_add.save(commit=False)
            VC_add.company_id = factory_id
            VC_add.years = request.session.get('years')
            VC_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = vehicle.objects.values("id").last().get("id")
            table_id = vehicle.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/vehicle_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", VC_add.errors)
    context['VC_add'] = VC_add
    context['years'] = request.session.get('years')
    return render(request, 'home/vehicle.html', context)


@login_required(login_url="/login/")
def water_dispenser_add(request):
    context = {}
    WD_add = WDform(request)
    if request.method == "POST":
        WD_add = WDform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if WD_add.is_valid():
            WD_add = WD_add.save(commit=False)
            WD_add.company_id = factory_id
            WD_add.years = request.session.get('years')
            WD_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = water_dispenser.objects.values("id").last().get("id")
            table_id = water_dispenser.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/water_dispenser_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", WD_add.errors)
    context['WD_add'] = WD_add
    context['years'] = request.session.get('years')
    return render(request, 'home/water-dispenser.html', context)


@login_required(login_url="/login/")
def ice_water_dispenser_add(request):
    context = {}
    IWD_add = IWDform(request)
    if request.method == "POST":
        IWD_add = IWDform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if IWD_add.is_valid():
            IWD_add = IWD_add.save(commit=False)
            IWD_add.company_id = factory_id
            IWD_add.years = request.session.get('years')
            IWD_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = ice_water_dispenser.objects.values("id").last().get("id")
            table_id = ice_water_dispenser.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/ice_water_dispenser_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", IWD_add.errors)
    context['IWD_add'] = IWD_add
    context['years'] = request.session.get('years')
    return render(request, 'home/ice-water-dispenser.html', context)


@login_required(login_url="/login/")
def ice_maker_add(request):
    context = {}
    IM_add = IMform(request)
    if request.method == "POST":
        IM_add = IMform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if IM_add.is_valid():
            IM_add = IM_add.save(commit=False)
            IM_add.company_id = factory_id
            IM_add.years = request.session.get('years')
            IM_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = ice_maker.objects.values("id").last().get("id")
            table_id = ice_maker.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/ice_maker_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", IM_add.errors)
    context['IM_add'] = IM_add
    context['years'] = request.session.get('years')
    return render(request, 'home/ice-maker.html', context)


@login_required(login_url="/login/")
def other_device_add(request):
    context = {}
    OD_add = ODform(request)
    if request.method == "POST":
        OD_add = ODform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if OD_add.is_valid():
            OD_add = OD_add.save(commit=False)
            OD_add.company_id = factory_id
            OD_add.years = request.session.get('years')
            OD_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = other_device.objects.values("id").last().get("id")
            table_id = other_device.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/other_device_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", OD_add.errors)
    context['OD_add'] = OD_add
    context['years'] = request.session.get('years')
    return render(request, 'home/other-device.html', context)


@login_required(login_url="/login/")
def extinguisher_add(request):
    context = {}
    EX_add = EXform(request)
    if request.method == "POST":
        EX_add = EXform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if EX_add.is_valid():
            EX_add = EX_add.save(commit=False)
            EX_add.company_id = factory_id
            EX_add.years = request.session.get('years')
            EX_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = extinguisher.objects.values("id").last().get("id")
            table_id = extinguisher.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/extinguisher_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", EX_add.errors)
    context['EX_add'] = EX_add
    context['years'] = request.session.get('years')
    return render(request, 'home/extinguisher.html', context)


@login_required(login_url="/login/")
def personnel_inventory_add(request):
    context = {}
    PI_add = PIform(request)
    if request.method == "POST":
        PI_add = PIform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if PI_add.is_valid():
            PI_add = PI_add.save(commit=False)
            PI_add.company_id = factory_id
            PI_add.years = request.session.get('years')
            PI_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = personnel_inventory.objects.values("id").last().get("id")
            table_id = personnel_inventory.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/personnel_inventory_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", PI_add.errors)
    context['PI_add'] = PI_add
    context['years'] = request.session.get('years')
    return render(request, 'home/personnel-inventory.html', context)


@login_required(login_url="/login/")
def employee_add(request):
    context = {}
    EMP_add = EMPform(request)
    if request.method == "POST":
        EMP_add = EMPform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if EMP_add.is_valid():
            EMP_add = EMP_add.save(commit=False)
            EMP_add.company_id = factory_id
            EMP_add.years = request.session.get('years')
            EMP_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = employee.objects.values("id").last().get("id")
            table_id = employee.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/employee_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", EMP_add.errors)
    context['EMP_add'] = EMP_add
    context['years'] = request.session.get('years')
    return render(request, 'home/employee.html', context)


# 廢水
@login_required(login_url="/login/")
def waste_water_add(request):
    context = {}
    waste_water_add = WASTEWATERform(request)
    if request.method == "POST":
        waste_water_add = WASTEWATERform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if waste_water_add.is_valid():
            waste_water_add = waste_water_add.save(commit=False)
            waste_water_add.company_id = factory_id
            waste_water_add.years = request.session.get('years')
            waste_water_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = waste_water.objects.values("id").last().get("id")
            table_id = waste_water.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/waste_water_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", waste_water_add.errors)
    context['waste_water_add'] = waste_water_add
    context['years'] = request.session.get('years')
    return render(request, 'home/waste-water.html', context)


# 廢汙泥
@login_required(login_url="/login/")
def waste_sludge_add(request):
    context = {}
    waste_sludge_add = WasteSludgeForm(request)
    if request.method == "POST":
        waste_sludge_add = WasteSludgeForm(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if waste_sludge_add.is_valid():
            waste_sludge_add = waste_sludge_add.save(commit=False)
            waste_sludge_add.company_id = factory_id
            waste_sludge_add.years = request.session.get('years')
            waste_sludge_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = waste_sludge.objects.values("id").last().get("id")
            table_id = waste_sludge.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/waste_sludge_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", waste_sludge_add.errors)
    context['waste_sludge_add'] = waste_sludge_add
    context['years'] = request.session.get('years')
    return render(request, 'home/waste-sludge.html', context)


# 溶劑、噴霧劑
@login_required(login_url="/login/")
def solvent_aerosol_emission_sources_add(request):
    context = {}
    SAES_add = SolventAerosolEmissionSourcesForm(request)
    if request.method == "POST":
        SAES_add = SolventAerosolEmissionSourcesForm(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if SAES_add.is_valid():
            solvent = SAES_add.save(commit=False)
            solvent.company_id = factory_id
            solvent.years = request.session.get('years')
            solvent.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/solvent_aerosol_emission_sources_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", SAES_add.errors)
    context['SAES_add'] = SAES_add
    context['years'] = request.session.get('years')
    return render(request, 'home/solvent-aerosol-emission-sources.html', {'SAES_add': SAES_add})


# VOCs1表單儲存
@login_required(login_url="/login/")
def VOCs_one_add(request):
    context = {}
    VOCs_one_add = VOCsOneForm(request)
    if request.method == "POST":
        VOCs_one_add = VOCsOneForm(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if VOCs_one_add.is_valid():
            VOCs_one_add = VOCs_one_add.save(commit=False)
            VOCs_one_add.company_id = factory_id
            VOCs_one_add.years = request.session.get('years')
            VOCs_one_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = VOCs_one.objects.values("id").last().get("id")
            table_id = VOCs_one.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/VOCs_one_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", VOCs_one_add.errors)
    context['VOCs_one_add'] = VOCs_one_add
    context['years'] = request.session.get('years')
    return render(request, 'home/VOCs-one.html', context)


# VOCs2表單儲存
@login_required(login_url="/login/")
def VOCs_two_add(request):
    context = {}
    VOCs_two_add = VOCsTwoForm(request)
    if request.method == "POST":
        VOCs_two_add = VOCsTwoForm(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if VOCs_two_add.is_valid():
            VOCs_two_add = VOCs_two_add.save(commit=False)
            VOCs_two_add.company_id = factory_id
            VOCs_two_add.years = request.session.get('years')
            VOCs_two_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = VOCs_two.objects.values("id").last().get("id")
            table_id = VOCs_two.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/VOCs_two_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", VOCs_two_add.errors)
    context['VOCs_two_add'] = VOCs_two_add
    context['years'] = request.session.get('years')
    return render(request, 'home/VOCs-two.html', context)


# 用電量
@login_required(login_url="/login/")
def electricity_add(request):
    context = {}
    ELEC_add = ELECform(request)
    if request.method == "POST":
        ELEC_add = ELECform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if ELEC_add.is_valid():
            ELEC_add = ELEC_add.save(commit=False)
            ELEC_add.company_id = factory_id
            ELEC_add.years = request.session.get('years')
            ELEC_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = electricity.objects.values("id").last().get("id")
            table_id = electricity.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/electricity_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", ELEC_add.errors)
    context['ELEC_add'] = ELEC_add
    context['years'] = request.session.get('years')
    return render(request, 'home/electricity.html', context)


# 上游運輸
@login_required(login_url="/login/")
def upstream_transportation_add(request):
    context = {}
    UT_add = UTform(request)
    if request.method == "POST":
        UT_add = UTform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if UT_add.is_valid():
            UT_add = UT_add.save(commit=False)
            UT_add.company_id = factory_id
            UT_add.years = request.session.get('years')
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
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/upstream_transportation_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", UT_add.errors)
    context['UT_add'] = UT_add
    context['years'] = request.session.get('years')
    return render(request, 'home/upstream-transportation.html', context)


# 下游運輸
@login_required(login_url="/login/")
def downstream_transportation_add(request):
    context = {}
    DT_add = DTform(request)
    if request.method == "POST":
        DT_add = DTform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if DT_add.is_valid():
            DT_add = DT_add.save(commit=False)
            DT_add.company_id = factory_id
            DT_add.years = request.session.get('years')
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
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/downstream_transportation_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", DT_add.errors)
    context['DT_add'] = DT_add
    context['years'] = request.session.get('years')
    return render(request, 'home/downstream-transportation.html', context)


@login_required(login_url="/login/")
def employee_commute_add(request):
    context = {}
    EC_add = ECform(request)
    if request.method == "POST":
        EC_add = ECform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if EC_add.is_valid():
            commute = EC_add.save(commit=False)
            commute.company_id = factory_id
            commute.years = request.session.get('years')
            commute.save()
            Commute_formSet = CommuteFormSet(request.POST, request.FILES, instance=commute)
            if Commute_formSet.is_valid():
                Commute_formSet.save()
                stage = request.POST.get('stage')
                image_path = request.FILES.getlist('file_field')
                last_id = employee_commute.objects.values("id").last().get("id")
                table_id = employee_commute.objects.values("did").last().get("did")
                for img in image_path:
                    photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                    print(stage)
                    photo.save()
                # 根據前端submit input的name判斷
                if 'addAnother' in request.POST:
                    messages.success(request, '表單已成功提交！')
                    return redirect('/employee_commute_add/')
                else:
                    return redirect('/carbon-system/')
            else:
                last_data = employee_commute.objects.last()
                last_data.delete()
                print("Commute_formSet>>>>>>>>>>>>>>>>>>>>\n", Commute_formSet)
                return render(request, 'home/employee-commute.html', {'EC_add': EC_add, 'CommuteFormSet': CommuteFormSet, 'years': request.session.get('years')})
        else:
            print("\n", EC_add.errors)
    context['EC_add'] = EC_add
    return render(request, 'home/employee-commute.html', {'EC_add': EC_add, 'CommuteFormSet': CommuteFormSet, 'years': request.session.get('years')})


@login_required(login_url="/login/")
def employee_business_trip_add(request):
    context = {}
    EBT_add = EBTform(request)
    if request.method == "POST":
        EBT_add = EBTform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if EBT_add.is_valid():
            business = EBT_add.save(commit=False)
            business.company_id = factory_id
            business.years = request.session.get('years')
            business.save()
            tripsection_formSet = TripSectionFormSet(request.POST, request.FILES, instance=business)
            if tripsection_formSet.is_valid():
                tripsection_formSet.save()
                stages = request.POST.getlist('stage')
                last_id = employee_business_trip.objects.values("id").last().get("id")
                table_id = employee_business_trip.objects.values("did").last().get("did")
                for stage in stages:
                    if stage == "員工出差段數":
                        image_paths = request.FILES.getlist('file_field1')
                    elif stage == "員工出差":
                        image_paths = request.FILES.getlist('file_field2')
                    else:
                        image_paths = []
                    for img in image_paths:
                        photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                        print(stage)
                        photo.save()
                # 根據前端submit input的name判斷
                if 'addAnother' in request.POST:
                    messages.success(request, '表單已成功提交！')
                    print('request.method', request.method)
                    print('表單已成功提交')
                    return redirect('/employee_business_trip_add/')
                else:
                    return redirect('/carbon-system/')
            else:
                last_data = employee_business_trip.objects.last()
                last_data.delete()
                print("tripsection_formSet表單錯誤>>>>>>>>>>>>>>>>>>>>\n", tripsection_formSet)
                return render(request, 'home/employee-business-trip.html', {'EBT_add': EBT_add, 'TripSectionFormSet': TripSectionFormSet, 'years': request.session.get('years')})
        else:
            print("\n", EBT_add.errors)
    context['EBT_add'] = EBT_add
    return render(request, 'home/employee-business-trip.html', {'EBT_add': EBT_add, 'TripSectionFormSet': TripSectionFormSet, 'years': request.session.get('years')})


@login_required(login_url="/login/")
def waste_add(request):
    context = {}
    WASTE_add = WASTEform(request)
    if request.method == "POST":
        WASTE_add = WASTEform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if WASTE_add.is_valid():
            WASTE_add = WASTE_add.save(commit=False)
            WASTE_add.company_id = factory_id
            WASTE_add.years = request.session.get('years')
            WASTE_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = waste.objects.values("id").last().get("id")
            table_id = waste.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/waste_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", WASTE_add.errors)
    context['WASTE_add'] = WASTE_add
    context['years'] = request.session.get('years')
    return render(request, 'home/waste.html', context)


# 納管廢水
@login_required(login_url="/login/")
def pipe_wastewater_add(request):
    context = {}
    PW_add = PWform(request)
    if request.method == "POST":
        PW_add = PWform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if PW_add.is_valid():
            PW_add = PW_add.save(commit=False)
            PW_add.company_id = factory_id
            PW_add.years = request.session.get('years')
            PW_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = pipe_wastewater.objects.values("id").last().get("id")
            table_id = pipe_wastewater.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/pipe_wastewater_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", PW_add.errors)
    context['PW_add'] = PW_add
    context['years'] = request.session.get('years')
    return render(request, 'home/pipe-wastewater.html', context)


# 採購原物料
@login_required(login_url="/login/")
def purchase_material_add(request):
    context = {}
    PM_add = PMform(request)
    if request.method == "POST":
        PM_add = PMform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if PM_add.is_valid():
            PM_add = PM_add.save(commit=False)
            PM_add.company_id = factory_id
            PM_add.years = request.session.get('years')
            PM_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = purchase_material.objects.values("id").last().get("id")
            table_id = purchase_material.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/purchase_material_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", PM_add.errors)
    context['PM_add'] = PM_add
    context['years'] = request.session.get('years')
    return render(request, 'home/purchase-material.html', context)


# 產品間接排放
@login_required(login_url="/login/")
def product_indirect_emissions_add(request):
    context = {}
    PIE_add = PIEform(request)
    if request.method == "POST":
        PIE_add = PIEform(request, request.POST, request.FILES)
        factory_id = request.session.get('factory_id')
        if PIE_add.is_valid():
            PIE_add = PIE_add.save(commit=False)
            PIE_add.company_id = factory_id
            PIE_add.years = request.session.get('years')
            PIE_add.save()
            stage = request.POST.get('stage')
            image_path = request.FILES.getlist('file_field')
            last_id = product_indirect_emissions.objects.values("id").last().get("id")
            table_id = product_indirect_emissions.objects.values("did").last().get("did")
            for img in image_path:
                photo = image(image_path=img, single_id=last_id, table_id=table_id, stage=stage)
                print(stage)
                photo.save()
            # 根據前端submit input的name判斷
            if 'addAnother' in request.POST:
                messages.success(request, '表單已成功提交！')
                return redirect('/product_indirect_emissions_add/')
            else:
                return redirect('/carbon-system/')
        else:
            print("\n", PIE_add.errors)
    context['PIE_add'] = PIE_add
    context['years'] = request.session.get('years')
    return render(request, 'home/product-indirect-emissions.html', context)


# ~~~
@login_required(login_url="/login/")
def carbon_system(request, message=None):
    if request.method == 'GET':
        # if request.user.is_authenticated:
        #     username = request.user.username
        #     print("username: ", username)

        # print('user', request.user.groups.filter(name='廠帳號'))
        # print('user', User.objects.all())
        # print('company', company.objects.get(id=1))

        # company_a_users = User.objects.filter(company=company.objects.get(company_name='Company A'))
        # for a in request.session:
        groups_query = request.user.groups.all()
        factory_group = factory.objects.exclude(factory_name='永續發展暨建值管理中心')
        user = Profile.objects.get(user_id=request.user.id)
        company_group = factory.objects.filter(company_id=user.company_id)
        context = {
            "groups_query": groups_query,
            "factory_group": factory_group,
            "company_group": company_group,
            "message": "",
            "count_error": "",
            "export_error": ""
        }
        if message:
            context.update(message)
        if request.session.get('dropdown_one') and request.session.get('dropdown_two') and request.session.get('dropdown_three'):
            context.update(request.session)
        return render(request, "home/carbon-system.html", context)
    if request.method == 'POST':
        dropdown_one = request.POST.get('dropdown_one')
        dropdown_two = request.POST.get('dropdown_two')
        dropdown_three = request.POST.get('dropdown_three')
        factory_id = request.POST.get('factory_dropdown')
        company_id = request.POST.get('company_dropdown')
        years = request.POST.get('years')
        if company_id is None:
            if factory_id is None:
                factory_id = current_user_group_id(request)
            # factory_id = current_user_group_id(request)
        print('factory_id', factory_id)
        # print('company_id', company_id)
        dropdown = {
            'dropdown_one': dropdown_one,
            'dropdown_two': dropdown_two,
            'dropdown_three': dropdown_three,
            'factory_id': factory_id,
            'company_id': company_id,
            'years': years,
        }
        request.session.update(dropdown)
        return redirect('/carbon-system/')


# 新增轉跳
@permission_required('home.add_emergency_generators', login_url="/login/", raise_exception=True)
@login_required(login_url="/login/")
def bar_action(request):
    if request.method == "GET":
        # 判斷是否有權限
        # if request.user.has_perm('home.add_emergency_generators'):
        #     print('yes')
        # else:
        #     print('no')
        # _permission = User.objects.get(username=request.user).get_all_permissions()
        # print('_permission', _permission)
        if 'add_page' in request.GET:
            device_id = request.session.get('dropdown_three')
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
                "27": pipe_wastewater_add(request),
                "28": purchase_material_add(request),
                "29": product_indirect_emissions_add(request)
            }
            device_function = None
            if function_dic.get(device_id):
                device_function = function_dic.get(device_id)
            return device_function
        if 'copy_last_year' in request.GET:
            message = copy_last_year_data(request)
            print('message', message)
            return carbon_system(request, message)
        if 'public_version' in request.GET:
            return public_version(request)
        if 'export_excel' in request.GET:
            message = export_excel(request)
            # 匯出錯誤訊息return字典到carbon_system
            if isinstance(message, dict):
                return carbon_system(request, message)
            else:
                return message


# 編輯轉跳
@permission_required('home.change_emergency_generators', login_url="/login/", raise_exception=True)
@login_required(login_url="/login/")
def edit_device(request, error_from=None, error_formset=None):
    datasheet_id = request.session.get('dropdown_three')
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
            single_dataID = request.GET.get('single_dataID')
            years = request.session.get('years')
            request.session.update({'single_dataID': single_dataID})
            current_data = dbName.objects.get(id=single_dataID)
            update_from = form(request, instance=current_data)

            formUpdata_name = {
                'form': update_from,
                'datasheet_id': datasheet_id,
                'single_dataID': single_dataID,
                'years': years,
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
        # 編輯後表單內容有誤轉跳
        if request.method == 'POST':
            single_dataID = request.session.get('single_dataID')
            years = request.session.get('years')
            update_from = error_from

            formUpdata_name = {
                'form': update_from,
                'datasheet_id': datasheet_id,
                'single_dataID': single_dataID,
                'years': years
            }
            # 表中表情況
            try:
                if datasheet_id in formsetName:
                    # update_formset = formset(instance=current_data)
                    # update_formset = formset(request.POST, request.FILES, instance=current_data)
                    update_formset = error_formset
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
def update_device(request, single_dataID):
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
    datasheet_id = request.session.get('dropdown_three')
    if modelName.get(datasheet_id) and formName.get(datasheet_id):
        dbName = modelName.get(datasheet_id)
        form = formName.get(datasheet_id)
        current_data = get_object_or_404(dbName, id=single_dataID)
        update_from = form(request, request.POST, request.FILES, instance=current_data)

        if request.method == 'POST':
            # 表中表情況
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
                        return edit_device(request, update_from, update_formset)
            except:
                pass
            # 正常表單(非表中表)
            if update_from.is_valid():
                update_from.save()
                return redirect('/carbon-system/', locals())
            else:
                print("\n", update_from.errors)
                return edit_device(request, update_from)


# 刪除資料
@permission_required('home.delete_emergency_generators', login_url="/login/", raise_exception=True)
@login_required(login_url="/login/")
def delete_device(request):
    if request.method == 'GET':
        datasheet_id = request.session.get('dropdown_three')
        delete_list = request.GET.get('delete_str').split()
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
            current_data = dbName.objects.filter(id__in=delete_list)
            current_data.delete()  # 刪除該筆資料
            return JsonResponse(delete_list, safe=False)


# 新增title
@login_required(login_url="/login/")
def add_title(request):
    if request.method == 'GET':
        device_id = request.session.get('dropdown_three')
        # 選擇title要顯示的欄位
        htmlName = {
            # 柴油發電機
            "1": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "設備編號", "容量(𝓁)", "地點", "部門", "是否推估"],
                "加油量(單位:𝓁)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "合計"],
                "佐證資料": ["引用單據"],
            },
            # 燃燒設備
            "2": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "名稱", "編號", "燃料種類"],
                "使用量": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "合計"],
                "熱值(Kcal/kg)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "平均"],
                "佐證資料": ["引用單據"],
            },
            # 公務車
            "3": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "類別", "編號", "燃料種類", "所屬單位", "計程方式"],
                "耗用量(單位:油車𝓁/電車kWh/公里數km)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "合計"],
                "尿素添加量(𝓁)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "合計"],
                "佐證資料": ["引用單據"],
            },
            # 原物料
            "4": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "原物料號", "原/物料", "名稱"],
                "是否為化學品": ["化學品名稱", "化學品名", "化學式"],
                "月用量(單位:公噸)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
                "佐證資料": ["引用單據"],
                "是否為化學品": ["化學品名稱", "化學品名", "化學式", "含碳量(%)"],
                "月用量(單位:公噸)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
            },
            # 製成添加物
            "5": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "製程階段", "料號", "製程添加名稱", "含碳量(%)", "是否燃燒", "VOCs"],
                "使用量(單位:公斤)": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "總計", "使用量單位"],
                "佐證資料": ["引用單據"],
            },
            # 冰箱清單
            "6": {
                "編輯區": ["刪除", "修改"],
                "冰箱清單": ["序號", "編號", "名稱", "品牌", "型號", "位置", "購買年份", "規格填充量", "冷媒類型", "維修填充量(kg)", "逸散率(%)", "逸散量"],
                "佐證資料": ["引用單據"],
            },
            # 冷氣機清單
            "7": {
                "編輯區": ["刪除", "修改"],
                "冷氣機清單": ["序號", "編號", "名稱", "品牌", "型號", "位置", "購買年份", "規格填充量", "冷媒類型", "維修填充量(kg)", "逸散率(%)", "逸散量"],
                "佐證資料": ["引用單據"],
            },
            # 車輛清單
            "8": {
                "編輯區": ["刪除", "修改"],
                "車輛清單": ["序號", "編號", "名稱", "品牌", "型號", "位置", "購買年份", "規格填充量", "冷媒類型", "維修填充量(kg)", "逸散率(%)", "逸散量"],
                "佐證資料": ["引用單據"],
            },
            # 飲水機清單
            "9": {
                "編輯區": ["刪除", "修改"],
                "飲水機清單": ["序號", "編號", "名稱", "品牌", "型號", "位置", "購買年份", "規格填充量", "冷媒類型", "維修填充量(kg)", "逸散率(%)", "逸散量"],
                "佐證資料": ["引用單據"],
            },
            # 冰水機清單
            "10": {
                "編輯區": ["刪除", "修改"],
                "冰水機清單": ["序號", "編號", "名稱", "品牌", "型號", "位置", "購買年份", "規格填充量", "冷媒類型", "維修填充量(kg)", "逸散率(%)", "逸散量"],
                "佐證資料": ["引用單據"],
            },
            # 製冰機清單
            "11": {
                "編輯區": ["刪除", "修改"],
                "製冰機清單": ["序號", "編號", "名稱", "品牌", "型號", "位置", "購買年份", "規格填充量", "冷媒類型", "維修填充量(kg)", "逸散率(%)", "逸散量"],
                "佐證資料": ["引用單據"],
            },
            # 設備清單
            "12": {
                "編輯區": ["刪除", "修改"],
                "設備清單": ["序號", "編號", "名稱", "品牌", "型號", "位置", "購買年份", "規格填充量", "冷媒類型", "維修填充量(kg)", "逸散率(%)", "逸散量"],
                "佐證資料": ["引用單據"],
            },
            # 滅火器
            "13": {
                "編輯區": ["刪除", "修改"],
                "滅火器清單": ["序號", "設備編號", "廠商", "類型", "擺放位置(廠別)", "庫存量", "藥劑重量(單位:kg)", "使用量數量", "使用月份", "更換/填充量", "更換/填充日期"],
                "佐證資料": ["引用單據"],
            },
            # 人天清冊
            "14": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "類型"],
                "時數": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
                "人數": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
                "佐證資料": ["引用單據"],
            },
            # 委外人員
            "15": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "人員類別"],
                "員工人數": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
                "當月工作天數": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
                "每日工作時數": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
                "佐證資料": ["引用單據"],
            },
            # 廢水
            "16": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "Pi:工業部門生產量", "Wi:廢水產生量", "CODi:化學需氧量", "Si:污泥移除量", "MCFj:甲烷修正係數", "Bo:最大CH4產生量", "Ri:甲烷移除量", "每年事業廢水之COD總量", u"CH\u2084"],
                "內容": ["序號", "Pi:工業部門生產量", "Wi:廢水產生量", "CODi:化學需氧量", "每年事業廢水之COD總量", "Si:污泥移除量", "MCFj:甲烷修正係數", "Bo:最大CH4產生量", "Ri:甲烷移除量", u"CH\u2084"],
                "佐證資料": ["引用單據"],
            },
            # 廢汙泥
            "17": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "廢棄污泥厭氧處理單元名稱", "污泥進流量(立方公尺/年)", "平均進流MLSS濃度(mg/L)", u"CH\u2084捕集系統捕集率", "燃燒設備效率"],
                "佐證資料": ["引用單據"],
            },
            # 溶劑、噴霧劑
            "18": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "溶劑、噴霧劑名稱", "數量(瓶/罐)", "容量", "單位", "氣體名稱", "氣體含量(%)", "密度"],
                "佐證資料": ["引用單據"],
            },

            "19": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "VOCs排放量(千立方公尺/年)", u"CH\u2084濃度(ppm)"],
                "佐證資料": ["引用單據"],
            },

            "20": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "VOCs排放量(千立方公尺/年)", u'CH\u2084濃度', "VOCs設備補集率", "燃燒設備效率"],
                "VOCs濃度": ["入口濃度", "出口濃度"],
                u"CO\u2082排放係數": ["內設值", "自訂值"],
                "佐證資料": ["引用單據"],
            },
            # 用電量
            "21": {
                "編輯區": ["刪除", "修改"],
                "用電量": ["序號", "電表編號", "地址", "一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "小計(度)", "總計(千度)"],
                "佐證資料": ["引用單據"],
            },
            # 上游運輸
            "22": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "單號", "商品", "淨/毛重", "重量(噸)", "組織使用產品", "客戶", "供應商名稱", "供應商地址", "貿易條件", "接貨地點", "送貨地點"],
                "陸運": ["單趟運輸距離(km)", "運輸國家", "交通工具", "燃料", "支付方", "趟次"],
                "海運": ["海運距離(nm)", "出貨港口", "到達港口", "支付方", "趟次"],
                "陸運(特殊)": ["單趟運輸距離(km)", "運輸國家", "交通工具", "燃料", "支付方", "趟次"],
                "空運": ["單趟運輸距離(km)", "出貨機場", "到達機場", "支付方", "趟次"],
                "佐證資料": ["引用單據"],
            },
            # 下游運輸
            "23": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "單號", "商品", "淨/毛重", "重量(噸)", "客戶", "供應商名稱", "供應商地址", "貿易條件", "接貨地點", "送貨地點"],
                "陸運": ["單趟運輸距離(km)", "運輸國家", "交通工具", "燃料", "支付方", "趟次"],
                "海運": ["海運距離(nm)", "出貨港口", "到達港口", "支付方", "趟次"],
                "陸運(特殊)": ["單趟運輸距離(km)", "運輸國家", "交通工具", "燃料", "支付方", "趟次"],
                "空運": ["單趟運輸距離(km)", "出貨機場", "到達機場", "支付方", "趟次"],
                "佐證資料": ["引用單據"],
            },
            # 員工通勤
            "24": {
                "編輯區": ["刪除", "修改"],
                "員工通勤清冊": ["序號", "編號", "部門", "姓名", "交通方式", "居住城市", "鄉鎮市區", "行政區公家機關地址", "至公司距離(km)", "年工作天數", "距離合計"],
                "佐證資料": ["引用單據"],
            },

            # 員工出差
            "25": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "出差單號", "員工編號", "部門", "姓名", "出差地點", "啟程日期"],
                "距離(pkm)": ["自駕汽車", "高鐵", "火車(電聯)", "火車(柴聯)", "計程車", "機車", "捷運", "飛機", "船舶"],
                "佐證資料": ["引用單據"],
            },
            # 廢棄物
            "26": {
                "編輯區": ["刪除", "修改"],
                "廢棄物處理": ["序號", "名稱", "重量(噸)", "運送時間", "處置地點", "處理方式", "處理廠商名稱", "運輸方式", "運輸燃料", "運輸距離(km)", "T*km"],
                "佐證資料": ["引用單據"],
            },

            # 納管廢水
            "27": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "納管編號", "廠別", "地址"],
                "納管廢水排放量": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "小計(公噸)"],
                "佐證資料": ["引用單據"],
            },

            # 原物料採購
            "28": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "產品編號", "產品名稱", "廠商", "大類名稱", "原/物料"],
                "原物料採購量": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "小計(公噸)"],
                "佐證資料": ["引用單據"],
            },

            # 原物料採購
            "29": {
                "編輯區": ["刪除", "修改"],
                "內容": ["序號", "產品編號", "產品名稱"],
                "產品間接排放量": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", "小計(公噸)"],
                "佐證資料": ["引用單據"],
            },
        }
        # 如果沒有刪除、編輯權限，把編輯區拿掉
        if not request.user.has_perm('home.add_emergency_generators'):
            for val_dic in htmlName.values():
                del val_dic['編輯區']

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
