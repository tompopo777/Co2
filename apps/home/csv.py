import io
import zipfile

import pandas as pd
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from urllib import parse

from .models import *




@csrf_exempt
@require_http_methods(["POST"])
def csv_view(request):
    if request.method == "POST":
        # if 'start' in request.POST and 'end' and 'type' in request.POST:
            # start = request.POST.get('start')
            # end = request.POST.get('end')
            # type = request.POST.get('type')
            # if 'statistics' in request.POST:
            #     statistics = request.POST.get('statistics')
            # else:
            #     statistics = '0'
            # if 'checkbox' in request.POST:
            #     checkbox_check = []
            #     checkbox_check_boolean = request.POST.getlist('checkbox')
            #     # true,false 轉成誰是true 0~3
            #     r = 0
            #     for c in checkbox_check_boolean:
            #         if c == 'true':
            #             checkbox_check.append(str(r))
            #         r += 1
            # if 'checkbox_check_boolean' not in locals():
            #     checkbox_check = ['0']
            # excel = []
            # excel_name = []
            # for c in checkbox_check:
            #     # 抓取全部co2資料
            #     co2, name = csv_getdata(request, type, c)
            #     if name == 'false':
            #         # 權限不足
            #         return HttpResponse(status=500)
            #     # 這邊可以使用query
            #     if start:
            #         co2 = co2.filter(date__gte=start)
            #     if end:
            #         co2 = co2.filter(date__lte=end)

        did = request.POST.get('did')
        excel_did = section_two.objects.filter(did__exact=int(did))

        df = csv_statistics(globals()[excel_did[0].t_name].objects.all())


        csv_name = excel_did[0].d_name + '.csv'

        # csv型態
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; charset=utf_8_sig; filename=' + parse.quote(csv_name, encoding="UTF-8")
        df.to_csv(index=False, sep=',', encoding='utf_8_sig', path_or_buf=response, na_rep='NULL')


        return response



def csv_statistics(data):
    df = pd.DataFrame(list(data.values()))
    df = df.drop(columns=['did_id'])
    df = df.drop(columns=['image_note'])
    df = df.drop(columns=['image_path'])
    return df
