# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse



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


@login_required(login_url="/login/")
def emergency_generators(request):
    if request.method == "POST":
        device_id = request.POST['device_id']
        period_startime = request.POST['period_startime']
        period_endtime = request.POST['period_endtime']
        position = request.POST['position']
        department = request.POST['department']
        january = request.POST['january']
        february = request.POST['february']
        march = request.POST['march']
        april = request.POST['april']
        may = request.POST['may']
        june = request.POST['june']
        july = request.POST['july']
        august = request.POST['august']
        september = request.POST['september']
        october = request.POST['october']
        november = request.POST['november']
        december = request.POST['december']
        image_note = request.POST['image_note']
        image_path = request.POST['image_path']

        unit = emergency_generators.objects.creat(
            device_id=device_id,
            period_startime=period_startime,
            period_endtime=period_endtime,
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
            image_path=image_path
        )

        unit.save()

        return redirect('/emergency-generator/')
    else:
        message = '請輸入資料(資料不作驗證)'
    return render(request, "emergency-generator.html", locals())
