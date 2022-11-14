# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError

from .forms import EGform
from apps.home.models import emergency_generators, section_one


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
# ajax
# @login_required(login_url="/login/")
# class ClientDetailView(DetailView):
#     model = Client
# @login_required(login_url="/login/")
# def ajax_load_process(request):
#     if request.method == 'GET':
#         current_class = request.GET.get('currentClass', None)
#         if current_class:
#             data = list(SectionOne.objects.filter(C_name=current_class).values("P_name", "CP_id"))
#             return JsonResponse(data, safe=False)




@login_required(login_url="/login/")
def getClass(request):
    allClass = section_one.objects.all()
    a = allClass.filter(c_name="")
    context = {'allClass': allClass}
    return render(request, "home/carbon-system.html", context)
    # return render(request, "home/official-car.html", locals())

    # if request.method == "POST":
    #     form = Inquire(request.POST)
    #     if form.is_valid():
    #         return render(request, "carbon-system.html", {'allClass': allClass})
    # else:
    #     form = Inquire()


@login_required(login_url="/login/")
def emergency_generators_add(request):
    if request.method == "POST":
        EG_add = EGform(request.POST)
        if EG_add.is_valid():
            device_id = EG_add.cleaned_data['device_id']
            period_starttime = EG_add.cleaned_data['period_starttime']
            period_endttime = EG_add.cleaned_data['period_endttime']
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
            image_path = EG_add.cleaned_data['image_path']

            unit = emergency_generators.objects.create(
                device_id=device_id,
                period_starttime=period_starttime,
                period_endttime=period_endttime,
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
                image_path=image_path
            )

            unit.save()

            return redirect('/emergency_generator/')

        else:
            message = '請完整填寫',
    else:
        message = '請輸入資料(資料不作驗證)'
        post = EGform()
    return redirect('/carbon-system/')


@login_required(login_url="/login/")
def emergency_generator(request):
    return render(request, "home/emergency-generator.html", locals())


@login_required(login_url="/login/")
def carbon_system(request):
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>0")

    if request.method == 'GET':
        currentClass = request.GET.get('cclass')
        if currentClass == None:
            currentClass = 0
        print(">>>>>>>>>>>>>>>>>>>>>.", currentClass)
        aa = section_one.objects.all()
        allProcess = section_one.objects.filter(c_name=currentClass).values()
        # allProcess = section_one.objects.filter(c_name='1')
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>1")
        # selectProcess = allProcess.p_name
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>2",selectProcess)
        context = {'allProcess': allProcess}
    return render(request, "home/carbon-system.html", context)