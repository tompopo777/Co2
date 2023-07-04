import datetime
from urllib import request, parse, response
import pandas as pd
from IPython.core.display import display
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Value, CharField
from django.db.models.functions import Cast
from decimal import *
from django.http import HttpResponse
from .count import *
import openpyxl
from .models import *
import json
from .views import carbon_system
from openpyxl.utils.dataframe import *
from openpyxl.styles import *

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

    # years = 2023
    # factory_id = 1
    # coefficient_source = '環保署溫室氣體排放係數管理表6.0.4'
    # gwp_version = 6
    emergency_generators_device = emergency_generators_inventory(years, factory_id, coefficient_source, gwp_version)
    combustion_equipment_device = combustion_equipment_inventory(years, factory_id, coefficient_source, gwp_version)
    official_car_device = official_car_inventory(years, factory_id, coefficient_source, gwp_version)
    refrigerant_device = refrigerant_inventory(years, factory_id, coefficient_source, gwp_version)
    personnel_inventory_device = personnel_inventory_inventory(years, factory_id, coefficient_source, gwp_version)
    employee_device = employee_inventory(years, factory_id, coefficient_source, gwp_version)
    # solvent_aerosol_emission_sources_device = solvent_aerosol_emission_sources_inventory(years, factory_id, coefficient_source, gwp_version)
    extinguisher_device = extinguisher_inventory(years, factory_id, coefficient_source, gwp_version)
    waste_water_device = waste_water_inventory(years, factory_id, coefficient_source, gwp_version)
    electricity_device = electricity_inventory(years, factory_id, coefficient_source, gwp_version)
    employee_commute_device = employee_commute_inventory(years, factory_id, coefficient_source, gwp_version)
    employee_business_trip_device = employee_business_trip_inventory(years, factory_id, coefficient_source, gwp_version)
    waste_transport_device = waste_transport_inventory(years, factory_id, coefficient_source, gwp_version)
    waste_process_device = waste_process_inventory(years, factory_id, coefficient_source, gwp_version)
    # purchase_material_device = purchase_material_inventory(years, factory_id, coefficient_source, gwp_version)

    output = pd.concat([emergency_generators_device, combustion_equipment_device, official_car_device, refrigerant_device, personnel_inventory_device,
                        employee_device, extinguisher_device, waste_water_device, electricity_device, employee_commute_device, employee_business_trip_device,
                        waste_transport_device, waste_process_device])

    if output.empty:
        message = {
            'count_error': '沒有任何資料!'
        }
        request.method = "GET"
        return carbon_system(request, message)

    output['total_emission'] = output['emission'].sum()
    output = output.drop_duplicates(subset=output.columns.difference(['total_emission']))
    print(output)

    output = output.rename(
        columns={'process_area': '過程或區域', 'device_name': '排放源設施', 'fuel_type': '原燃物料', 'gas_name': '可能產生溫室氣體種類', 'emission': '排放當量公噸(公噸/數據期間)', 'total_emission': '加總排放當量(公噸CO2e/年)'})
    new_order = ['過程或區域', '排放源設施', '原燃物料', '可能產生溫室氣體種類', '排放當量公噸(公噸/數據期間)', '加總排放當量(公噸CO2e/年)']
    output = output.reindex(columns=new_order)

    display(output)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + parse.quote('溫室氣體排放清冊-' + company_name + '_' + years + '.xlsx', encoding="UTF-8")

    # 将 DataFrame 写入指定位置的工作表
    sheet_name = "Sheet35"  # 指定工作表名
    start_row = 5  # 起始行
    end_row = start_row + len(output) - 1  # 合并的结束行
    start_col = 2  # 起始列

    # 合并 G 列的单元格
    merge_range = f'G{start_row}:G{end_row}'
    output.to_excel(response, index=False, sheet_name=sheet_name, startrow=start_row - 1, startcol=start_col - 1)

    # 返回响应
    return response

    # # 匯出Excel檔案
    # output.to_excel(response, index=False)
    # return response


# 發電機
def emergency_generators_inventory(years, factory_id, coefficient_source, gwp_version):
    df = emergency_generators_count(years, factory_id, coefficient_source, gwp_version)
    row_data = df.drop(columns=['sum_count', 'data_unit', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient'])
    # 合併所有的氣體
    row_data['gas_name'] = row_data['gas_name'].str.cat(sep=',')
    row_data = row_data.groupby(['process_area', 'device_name', 'fuel_type', 'gas_name'])['emission'].sum().reset_index()
    # row_data = row_data.groupby(['process_area']).agg({'device_name': 'first', 'fuel_type': 'first', 'gas_name': 'first', 'emission': 'sum'}).reset_index()
    return row_data


# 燃燒設備
def combustion_equipment_inventory(years, factory_id, coefficient_source, gwp_version):
    df = combustion_equipment_count(years, factory_id, coefficient_source, gwp_version)
    row_data = df.drop(columns=['sum_count', 'data_unit', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient'])
    # 合併所有的氣體
    row_data['fuel_type'] = row_data.groupby('device_name')['fuel_type'].transform(lambda x: ','.join(x))
    row_data['gas_name'] = row_data.groupby('device_name')['gas_name'].transform(lambda x: ','.join(x))
    # split將字串用逗號分割，然後再用set去除重複的
    row_data['fuel_type'] = row_data['fuel_type'].str.split(',').apply(lambda x: ','.join(set(x)))
    row_data['gas_name'] = row_data['gas_name'].str.split(',').apply(lambda x: ','.join(set(x)))
    row_data = row_data.groupby(['process_area', 'device_name', 'fuel_type', 'gas_name'])['emission'].sum().reset_index()
    return row_data


# 公務車
def official_car_inventory(years, factory_id, coefficient_source, gwp_version):
    df = official_car_count(years, factory_id, coefficient_source, gwp_version)
    row_data = df.drop(columns=['sum_count', 'data_unit', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient'])
    # 合併所有的氣體
    row_data['fuel_type'] = row_data.groupby('device_name')['fuel_type'].transform(lambda x: ','.join(x))
    row_data['gas_name'] = row_data.groupby('device_name')['gas_name'].transform(lambda x: ','.join(x))
    # split將字串用逗號分割，然後再用set去除重複的
    row_data['fuel_type'] = row_data['fuel_type'].str.split(',').apply(lambda x: ','.join(set(x)))
    row_data['gas_name'] = row_data['gas_name'].str.split(',').apply(lambda x: ','.join(set(x)))
    row_data = row_data.groupby(['process_area', 'device_name', 'fuel_type', 'gas_name'])['emission'].sum().reset_index()
    return row_data


# 冷媒全部
def refrigerant_inventory(years, factory_id, coefficient_source, gwp_version):
    refrigerator = refrigerator_count(years, factory_id, coefficient_source, gwp_version)
    airconditioner = airconditioner_count(years, factory_id, coefficient_source, gwp_version)
    vehicle = vehicle_count(years, factory_id, coefficient_source, gwp_version)
    water_dispenser = water_dispenser_count(years, factory_id, coefficient_source, gwp_version)
    ice_water_dispenser = ice_water_dispenser_count(years, factory_id, coefficient_source, gwp_version)
    ice_maker = ice_maker_count(years, factory_id, coefficient_source, gwp_version)
    other_device = other_device_count(years, factory_id, coefficient_source, gwp_version)
    refrigerant_device = pd.concat([refrigerator, airconditioner, vehicle, water_dispenser, ice_water_dispenser, ice_maker, other_device], axis=0)
    row_data = refrigerant_device.drop(columns=['sum_count', 'data_unit', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient'])
    row_data['fuel_type'] = '冷媒'
    # 合併所有的氣體
    row_data['device_name'] = row_data.groupby('fuel_type')['device_name'].transform(lambda x: ','.join(x))
    # # split將字串用逗號分割，然後再用set去除重複的
    row_data = row_data.groupby(['process_area', 'device_name', 'fuel_type', 'gas_name'])['emission'].sum().reset_index()
    return row_data


# 人天清冊
def personnel_inventory_inventory(years, factory_id, coefficient_source, gwp_version):
    df = personnel_inventory_count(years, factory_id, coefficient_source, gwp_version)
    row_data = df.drop(columns=['sum_count', 'data_unit', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient'])
    row_data = row_data.groupby(['process_area', 'device_name', 'fuel_type', 'gas_name'])['emission'].sum().reset_index()
    return row_data


# 委外人員
def employee_inventory(years, factory_id, coefficient_source, gwp_version):
    df = employee_count(years, factory_id, coefficient_source, gwp_version)
    row_data = df.drop(columns=['sum_count', 'data_unit', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient'])
    row_data = row_data.groupby(['process_area', 'device_name', 'fuel_type', 'gas_name'])['emission'].sum().reset_index()
    return row_data


# 滅火器
def extinguisher_inventory(years, factory_id, coefficient_source, gwp_version):
    df = extinguisher_count(years, factory_id, coefficient_source, gwp_version)
    row_data = df.drop(columns=['sum_count', 'data_unit', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient'])
    row_data = row_data.groupby(['process_area', 'device_name', 'fuel_type', 'gas_name'])['emission'].sum().reset_index()
    return row_data


# 厭氧廢水
def waste_water_inventory(years, factory_id, coefficient_source, gwp_version):
    df = waste_water_count(years, factory_id, coefficient_source, gwp_version)
    row_data = df.drop(columns=['sum_count', 'data_unit', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient'])
    row_data = row_data.groupby(['process_area', 'device_name', 'fuel_type', 'gas_name'])['emission'].sum().reset_index()
    return row_data


# 用電量
def electricity_inventory(years, factory_id, coefficient_source, gwp_version):
    df = electricity_count(years, factory_id, coefficient_source, gwp_version)
    row_data = df.drop(columns=['sum_count', 'data_unit', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient'])
    row_data = row_data.groupby(['process_area', 'device_name', 'fuel_type', 'gas_name'])['emission'].sum().reset_index()
    return row_data


# 員工通勤
def employee_commute_inventory(years, factory_id, coefficient_source, gwp_version):
    df = employee_commute_count(years, factory_id, coefficient_source, gwp_version)
    row_data = df.drop(columns=['sum_count', 'data_unit', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient'])
    row_data['device_name'] = '員工通勤'
    row_data = row_data.groupby(['process_area', 'device_name', 'fuel_type', 'gas_name'])['emission'].sum().reset_index()
    return row_data


# 員工出差
def employee_business_trip_inventory(years, factory_id, coefficient_source, gwp_version):
    df = employee_business_trip_count(years, factory_id, coefficient_source, gwp_version)
    row_data = df.drop(columns=['sum_count', 'data_unit', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient'])
    row_data['device_name'] = '員工出差'
    row_data = row_data.groupby(['process_area', 'device_name', 'fuel_type', 'gas_name'])['emission'].sum().reset_index()
    return row_data


# 廢棄物運輸
def waste_transport_inventory(years, factory_id, coefficient_source, gwp_version):
    df = waste_transport_count(years, factory_id, coefficient_source, gwp_version)
    row_data = df.drop(columns=['sum_count', 'data_unit', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient'])
    row_data['device_name'] = '廢棄物運輸'
    row_data['fuel_type'] = row_data['fuel_type'].str.split('(', 1).str[1].str.rstrip(')')
    row_data['fuel_type'] = row_data['fuel_type'].apply(lambda x: '運輸車輛-' + x)
    row_data = row_data.groupby(['process_area', 'device_name', 'fuel_type', 'gas_name'])['emission'].sum().reset_index()
    return row_data


# 廢棄物處理
def waste_process_inventory(years, factory_id, coefficient_source, gwp_version):
    df = waste_process_count(years, factory_id, coefficient_source, gwp_version)
    row_data = df.drop(columns=['sum_count', 'data_unit', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient'])
    row_data = row_data.groupby(['process_area', 'device_name', 'fuel_type', 'gas_name'])['emission'].sum().reset_index()
    return row_data


# 原物料採購
def purchase_material_inventory(years, factory_id, coefficient_source, gwp_version):
    df = purchase_material_count(years, factory_id, coefficient_source, gwp_version)
    row_data = df.drop(columns=['sum_count', 'data_unit', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient'])
    row_data = row_data.groupby(['process_area', 'device_name', 'fuel_type', 'gas_name'])['emission'].sum().reset_index()
    return row_data




