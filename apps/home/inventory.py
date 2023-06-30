import datetime
from urllib import request, parse
import pandas as pd
from IPython.core.display import display
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Value, CharField
from django.db.models.functions import Cast
from decimal import *
from django.http import HttpResponse
from .count import *

from .models import *
import json

from .views import carbon_system

pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.width', 200)


@login_required(login_url="/login/")
def inventory_summary(request):
    coefficient_source = request.session.get('coefficient_source')
    gwp_version = request.session.get('gwp_version')
    # 判斷使用者是否為公司帳號。
    if request.user.groups.filter(name='公司帳號').exists():
        factory_id = request.session.get('company_id')
    else:
        factory_id = request.session.get('factory_id')
    years = request.session.get('years')

    try:
        company_name = str(factory.objects.filter(id=factory_id).get())
        # print('company_name', company_name)
    except:
        company_name = ''

    emergency_generators_device = emergency_generators_inventory(years, factory_id, coefficient_source, gwp_version)
    combustion_equipment_device = combustion_equipment_inventory(years, factory_id, coefficient_source, gwp_version)
    output = pd.concat([emergency_generators_device, combustion_equipment_device])

    if output.empty:
        message = {
            'count_error': '沒有任何資料!'
        }
        request.method = "GET"
        return carbon_system(request, message)

    output = output.rename(
        columns={'process_area': '過程或區域', 'device_name': '排放源設施', 'fuel_type': '原燃物料', 'gas_name': '可能產生溫室氣體種類'})
    new_order = ['過程或區域', '排放源設施', '原燃物料', '可能產生溫室氣體種類']
    output = output.reindex(columns=new_order)
    display(output)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + parse.quote('溫室氣體排放量統計總表-' + company_name + '_' + years + '.xlsx', encoding="UTF-8")

    # 匯出Excel檔案
    output.to_excel(response, index=False)
    return response


def emergency_generators_inventory(years, factory_id, coefficient_source, gwp_version):
    df = emergency_generators_count(years, factory_id, coefficient_source, gwp_version)
    row_data = df.drop(columns=['sum_count', 'data_unit', 'emission', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient'])

    return row_data


def combustion_equipment_inventory(years, factory_id, coefficient_source, gwp_version):
    df = combustion_equipment_count(years, factory_id, coefficient_source, gwp_version)
    row_data = df.drop(columns=['sum_count', 'data_unit', 'emission', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient'])

    return row_data


# # 合并相同值的单元格
# output = output.style
# output.set_properties(**{'text-align': 'left'})  # 设置单元格对齐方式为左对齐
# output = output.set_table_styles([{'selector': 'td', 'props': [('text-align', 'left')]}])  # 设置表格中单元格的对齐方式
# output = output.set_caption('溫室氣體排放量統計總表')  # 设置标题
#
# # 创建一个新的Excel工作簿
# workbook = Workbook()
# sheet = workbook.active
#
# # 将DataFrame的样式应用到工作表
# for row in dataframe_to_rows(output.data, index=False, header=True):
#     sheet.append(row)
#
# # 合并相同值的单元格
# prev_value = None
# start_row = 2  # 跳过标题行，从第二行开始
# for row in range(2, sheet.max_row + 1):
#     current_value = sheet.cell(row=row, column=1).value
#     if current_value != prev_value:
#         if prev_value is not None:
#             # 合并单元格
#             sheet.merge_cells(start_row=start_row, start_column=1, end_row=row - 1, end_column=1)
#         prev_value = current_value
#         start_row = row