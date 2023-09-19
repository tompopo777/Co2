import datetime
from urllib import request, parse
import pandas as pd
from IPython.core.display import display
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Value, CharField, When, Case
from django.db.models.functions import Cast, Coalesce
from decimal import *
from django.http import HttpResponse

from .models import *
import json

from .views import carbon_system

pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.width', 200)


# getcontext().prec = 4

@login_required(login_url="/login/")
def calculate_summary(request):
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

    emergency_generators_device = emergency_generators_count(years, factory_id, coefficient_source, gwp_version)
    combustion_equipment_device = combustion_equipment_count(years, factory_id, coefficient_source, gwp_version)
    official_car_device = official_car_count(years, factory_id, coefficient_source, gwp_version)
    process_device = process_count(years, factory_id, coefficient_source, gwp_version)
    other_device_device = other_device_count(years, factory_id, coefficient_source, gwp_version)
    solvent_aerosol_emission_sources_device = solvent_aerosol_emission_sources_count(years, factory_id, coefficient_source, gwp_version)
    personnel_inventory_device = personnel_inventory_count(years, factory_id, coefficient_source, gwp_version)
    extinguisher_device = extinguisher_count(years, factory_id, coefficient_source, gwp_version)
    waste_water_device = waste_water_count(years, factory_id, coefficient_source, gwp_version)
    electricity_device = electricity_count(years, factory_id, coefficient_source, gwp_version)
    upstream_transport_device = upstream_transport_count(years, factory_id, coefficient_source, gwp_version)
    downstream_transport_device = downstream_transport_count(years, factory_id, coefficient_source, gwp_version)
    employee_commute_device = employee_commute_count(years, factory_id, coefficient_source, gwp_version)
    employee_business_trip_device = employee_business_trip_count(years, factory_id, coefficient_source, gwp_version)
    waste_transport_device = waste_transport_count(years, factory_id, coefficient_source, gwp_version)
    waste_process_device = waste_process_count(years, factory_id, coefficient_source, gwp_version)
    purchase_material_device = purchase_material_count(years, factory_id, coefficient_source, gwp_version)

    output = pd.concat([emergency_generators_device, combustion_equipment_device, official_car_device, process_device, other_device_device,
                        solvent_aerosol_emission_sources_device, personnel_inventory_device, extinguisher_device, waste_water_device,
                        electricity_device,
                        upstream_transport_device, downstream_transport_device, employee_commute_device, employee_business_trip_device, waste_transport_device,
                        waste_process_device, purchase_material_device])

    if output.empty:
        message = {
            'count_error': '沒有任何資料!'
        }
        request.method = "GET"
        return carbon_system(request, message)

    output = output.rename(
        columns={'process_area': '過程或區域', 'device_name': '排放源設施', 'fuel_type': '原燃物料', 'sum_count': '活動數據總量', 'data_unit': '數據單位', 'emission': '排放當量公噸(公噸/數據期間)', 'gas_name': '可能產生溫室氣體種類', 'coefficient': '排放係數', 'coefficient_unit': '排放係數單位',
                 'coefficient_source': '係數來源', 'gwp_coefficient': 'ICPP報告GWP值'})
    new_order = ['過程或區域', '排放源設施', '原燃物料', '活動數據總量', '數據單位', '排放當量公噸(公噸/數據期間)', '可能產生溫室氣體種類', '排放係數', '排放係數單位', '係數來源', 'ICPP報告GWP值']
    output = output.reindex(columns=new_order)
    display(output)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + parse.quote('溫室氣體排放量統計總表-' + company_name + '_' + years + '.xlsx', encoding="UTF-8")

    # 匯出Excel檔案
    output.to_excel(response, index=False)
    # return carbon_system(request, request)
    return response


# 發電機
def emergency_generators_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        raw_data = emergency_generators.objects.filter(years=years).filter(company_id=factory_id).values('did').annotate(
            process_area=Value('固定式燃燒', output_field=models.CharField(max_length=50)),
            device_name=Value('柴油發電機', output_field=CharField(max_length=20)),
            fuel_type=Value('柴油', output_field=CharField(max_length=20)),
            sum_count=Cast(Sum(F('january') + F('february') + F('march') + F('april') + F('may') + F('june') +
                               F('july') + F('august') + F('september') + F('october') + F('november') + F('december')) / 1000,
                           output_field=models.DecimalField(max_digits=20, decimal_places=4)),
            data_unit=Value('公秉', output_field=models.CharField(max_length=50))
        )
        coefficient_part = None
        for query in raw_data:
            fuel_type = query['fuel_type']
            coefficient_data = coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause=fuel_type).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(coefficient_unit=Value('公噸' + '/公秉', output_field=models.CharField(max_length=50)))
            coefficient_part = pd.DataFrame(list(coefficient_data))
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=coefficient_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        raw_data = pd.DataFrame(list(raw_data))
        a_b_part = pd.merge(raw_data, coefficient_part, left_on='fuel_type', right_on='cause', how='left')
        final = pd.merge(a_b_part, gwp, left_on='gas_name', right_on='gas_name', how='left')
        # 將(A)、(B)、(C)轉為float才能取round
        final['emission'] = final.apply(lambda x: round(Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        # display(final)
        # display(final.shape)
        return final
    except:
        print('沒有該發電機設備')
        return final


# 燃燒設備
def combustion_equipment_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        # years = 2023
        # factory_id = 1
        # coefficient_source = '環保署溫室氣體排放係數管理表6.0.4'
        # gwp_version = 6
        raw_data = pd.DataFrame(list(combustion_equipment.objects.filter(years=years).filter(company_id=factory_id).values('device_name', 'fuel_type').annotate(
            process_area=Value('固定式燃燒', output_field=models.CharField(max_length=50)),
            sum_count=Cast(Sum(F('fuel_january') + F('fuel_february') + F('fuel_march') + F('fuel_april') + F('fuel_may') + F('fuel_june') + F('fuel_july') + F('fuel_august') + F('fuel_september') + F('fuel_october') + F('fuel_november') + F('fuel_december')) * 1.818 / 1000,
                           output_field=models.DecimalField(max_digits=20, decimal_places=4)),
            heat_count=Cast(Sum(F('heat_january') + F('heat_february') + F('heat_march') + F('heat_april') + F('heat_may') + F('heat_june') + F('heat_july') + F('heat_august') + F('heat_september') + F('heat_october') + F('heat_november') + F('heat_december')) * 0.9,
                            output_field=models.DecimalField(max_digits=20, decimal_places=4)),
            data_unit=Value('公秉', output_field=models.CharField(max_length=50))
        ).order_by('device_name', 'fuel_type')))
        coefficient_part = pd.DataFrame(
            list(coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause__in=raw_data['fuel_type']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(coefficient_unit=Value('公噸' + '/公秉', output_field=models.CharField(max_length=50)))))
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=coefficient_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        a_b_part = pd.merge(raw_data, coefficient_part, left_on='fuel_type', right_on='cause', how='left')
        co2_formular = Decimal(56100 * (4186.8 * (10 ** (-9)) * (10 ** (-3))))
        ch4_formular = Decimal(1 * (4186.8 * (10 ** (-9)) * (10 ** (-3))))
        n2o_formular = Decimal(0.1 * (4186.8 * (10 ** (-9)) * (10 ** (-3))))

        def calculate_coefficient(row):
            if row['fuel_type'] == '天然氣':
                if row['gas_name'] == 'CO2':
                    return row['heat_count'] * co2_formular
                elif row['gas_name'] == 'CH4':
                    return row['heat_count'] * ch4_formular
                elif row['gas_name'] == 'N2O':
                    return row['heat_count'] * n2o_formular
            else:
                return row['coefficient']

        a_b_part['coefficient'] = a_b_part.apply(calculate_coefficient, axis=1)
        a_b_part['coefficient'] = a_b_part['coefficient'].apply(lambda x: round(x, 10))
        final = pd.merge(a_b_part, gwp, left_on='gas_name', right_on='gas_name', how='left')
        # 將(A)、(B)、(C)轉為float才能取round
        final['emission'] = final.apply(lambda x: (Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient'])).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP), axis=1)
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        print(final)
        # display(final)
        # display(final.shape)
        return final
    except:
        print('沒有該燃燒設備設備')
        return final


# 公務車
def official_car_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        raw_data = pd.DataFrame(list(official_car.objects.filter(years=years).filter(company_id=factory_id).values('vehicle_type', 'fuel_type', 'urea_content_median', 'urea_water_median').annotate(
            process_area=Value('移動式式燃燒', output_field=models.CharField(max_length=50)),
            device_name=Value('公務車', output_field=models.CharField(max_length=30)),
            sum_count=Cast(Sum(F('january') + F('february') + F('march') + F('april') + F('may') + F('june') +
                               F('july') + F('august') + F('september') + F('october') + F('november') + F('december')) / 1000,
                           output_field=models.DecimalField(max_digits=20, decimal_places=4)),
            urea_count=Cast(Sum(F('urea_january') + F('urea_february') + F('urea_march') + F('urea_april') + F('urea_may') + F('urea_june') +
                                F('urea_july') + F('urea_august') + F('urea_september') + F('urea_october') + F('urea_november') + F('urea_december')) / 1000,
                            output_field=models.DecimalField(max_digits=20, decimal_places=4)),
            data_unit=Value('公秉', output_field=models.CharField(max_length=50))
        ).order_by('vehicle_type', 'fuel_type')))
        raw_data['fuel_type'] = raw_data['fuel_type'].replace(['汽油'], '車用汽油')
        # 尿素輸出
        urea_data = raw_data[raw_data['fuel_type'] == '柴油'].copy()
        urea_data['fuel_type'] = raw_data['fuel_type'].replace(['柴油'], '尿素')
        urea_data['sum_count'] = (urea_data['urea_count'] * urea_data['urea_water_median'] * (urea_data['urea_content_median'] / 100) / 1000)
        urea_data['sum_count'] = urea_data['sum_count'].apply(lambda x: round(x, 4))
        a_part = pd.concat([raw_data, urea_data])
        print(a_part)
        coefficient_part = pd.DataFrame(
            list(coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause__in=a_part['fuel_type']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(coefficient_unit=Value('公噸' + '/公秉', output_field=models.CharField(max_length=50)))))
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=coefficient_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        a_b_part = pd.merge(a_part, coefficient_part, left_on='fuel_type', right_on='cause', how='left')
        final = pd.merge(a_b_part, gwp, left_on='gas_name', right_on='gas_name', how='left')
        # 將(A)、(B)、(C)轉為float才能取round
        final['emission'] = final.apply(lambda x: round(Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        print(final)
        return final
    except:
        print('沒有該公務車設備')
        return final


# 化學品
def process_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        # years = 2023
        # factory_id = 1
        # coefficient_source = '環保署溫室氣體排放係數管理表6.0.4'
        # gwp_version = 6
        raw_data = pd.DataFrame(list(process.objects.filter(years=years).filter(company_id=factory_id).values("process_stage", "process_add_name", "chemical_coefficient").annotate(
            process_area=Value('產業過程之直接過程排放與移除', output_field=models.CharField(max_length=50)),
            device_name=Value('製程化學品', output_field=models.CharField(max_length=50)),
            sum_count=Cast(Sum(F('january') + F('february') + F('march') + F('april') + F('may') + F('june') +
                               F('july') + F('august') + F('september') + F('october') + F('november') + F('december')) / 1000,
                           output_field=models.DecimalField(max_digits=20, decimal_places=4)),
            data_unit=Value('公噸', output_field=models.CharField(max_length=50)),
            gas_name=Value('CO2', output_field=models.CharField(max_length=10)),
            coefficient_unit=Value('公噸/公秉', output_field=models.CharField(max_length=20)),
            coefficient_source=Value('質量平衡法', output_field=models.CharField(max_length=50)),
        )))
        raw_data['device_name'] = raw_data.apply(lambda x: f"{x['device_name']} - {x['process_stage']}", axis=1)
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=raw_data['gas_name']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(raw_data, gwp, left_on='gas_name', right_on='gas_name', how='left')
        final = final.rename(columns={'process_add_name': 'fuel_type', 'chemical_coefficient': 'coefficient'})
        final['emission'] = final.apply(lambda x: round(Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        print(final)
        return final
    except:
        print('沒有該化學品設備')
        return final


# 冷媒
def other_device_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        # years = 2023
        # factory_id = 1
        # coefficient_source = '環保署溫室氣體排放係數管理表6.0.4'
        # gwp_version = 6
        raw_data = pd.DataFrame(
            list(other_device.objects.filter(years=years).filter(company_id=factory_id).values('refrigerant_type', 'filling_volume', 'device_type', 'device_amount').annotate(
                process_area=Value('人為系統所釋放的溫室氣體產生的直接暫時性排放', output_field=models.CharField(max_length=50)),
                data_unit=Value('公噸', output_field=models.CharField(max_length=50)))))
        raw_data['sum_count'] = raw_data.apply(lambda x: x['filling_volume'] * x['device_amount'], axis=1)
        raw_data['sum_count'] = raw_data.groupby(["refrigerant_type"])['sum_count'].transform('sum')

        def refrigerant_coefficient(row):
            if row['device_type'] == '車輛、家用除濕機':
                row['device_name'] = f"移動式空氣清靜機-{row['device_type']}"
                return row
            elif row['device_type'] == '冷氣':
                row['device_name'] = f"住宅及商業建築冷氣機-{row['device_type']}"
                return row
            elif row['device_type'] == '冰箱、飲水機':
                row['device_name'] = f"家用冷凍、冷藏裝備-{row['device_type']}"
                return row
            elif row['device_type'] == '落地形大型冷氣機':
                row['device_name'] = f"獨立商用冷凍、冷藏裝備-{row['device_type']}"
                return row
            elif row['device_type'] == '大型冷凍櫃':
                row['device_name'] = f"中、大型冷凍、冷藏裝備-{row['device_type']}"
                return row
            elif row['device_type'] == '冷凍物流車':
                row['device_name'] = f"交通用冷凍、冷藏裝備-{row['device_type']}"
                return row
            elif row['device_type'] == '製冰機、切削液冷卻機、工業用除濕機、空氣乾燥機':
                row['device_name'] = f"工業冷凍、冷藏裝備，包括食品加工及冷藏-{row['device_type']}"
                return row
            elif row['device_type'] == '冰水機':
                row['device_name'] = "冰水機"
                return row
            else:
                row['device_name'] = "其他"

        # 使用apply函数应用refrigerant_coefficient函数
        raw_data = raw_data.apply(refrigerant_coefficient, axis=1)
        raw_data['refrigerant'] = raw_data['device_name'].apply(lambda x: x.split('-')[0])
        raw_data = raw_data.rename(columns={'refrigerant_type': 'fuel_type'})
        coefficient_part = pd.DataFrame(
            list(coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause__in=raw_data['refrigerant']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(coefficient_unit=Value('公噸' + '/公噸', output_field=models.CharField(max_length=50)))))
        ab_part = pd.merge(raw_data, coefficient_part, left_on='refrigerant', right_on='cause', how='left')
        ab_part = ab_part.drop(columns=['filling_volume', 'device_amount', 'cause', 'refrigerant']).drop_duplicates()
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=raw_data['fuel_type']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, left_on='fuel_type', right_on='gas_name', how='left')
        final = final.rename(columns={'gas_name_x': 'gas_name'})
        final['emission'] = final.apply(lambda x: round(Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        return final
    except:
        print('沒有該其他設備設備')
        return final


# 溶劑、噴霧劑
def solvent_aerosol_emission_sources_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        # years = 2023
        # factory_id = 1
        # coefficient_source = '環保署溫室氣體排放係數管理表6.0.4'
        # gwp_version = 6
        raw_part = pd.DataFrame(list(solvent_aerosol_emission_sources.objects.filter(years=years).filter(company_id=factory_id).values('id', 'solvent_name', 'solvent_amount').annotate(
            process_area=Value('人為系統所釋放的溫室氣體產生的直接暫時性排放', output_field=models.CharField(max_length=50)),
            device_name=Value('溶劑、噴霧劑', output_field=models.CharField(max_length=50)),
            data_unit=Value('公噸', output_field=models.CharField(max_length=50))))
        )
        gas_add_data = pd.DataFrame(list(gas_add.objects.values('solvent_capacity', 'solvent_capacity_unit', 'gas_ratio', 'density', 'gas_id')))
        a_part = pd.merge(raw_part, gas_add_data, left_on='id', right_on='gas_id', how='left')
        # 溶劑名稱、添加物名稱相同的，將數量做總和
        a_part = a_part.groupby(['solvent_name', 'solvent_capacity', 'solvent_capacity_unit', 'gas_ratio', 'density', ]).agg({'solvent_amount': 'sum', 'process_area': 'first', 'device_name': 'first', 'data_unit': 'first'}).reset_index()

        def multiply(row):
            if row['solvent_capacity_unit'] == '毫升':
                row['solvent_amount'] = Decimal(str(row['solvent_amount'])) * Decimal(str(row['solvent_capacity'])) * Decimal(str(row['density'])) * Decimal(str(row['gas_ratio'])) / Decimal('100') / Decimal('1000') / Decimal('1000')
                row['solvent_amount'] = round(Decimal(row['solvent_amount']), 4)
                return row['solvent_amount']

            if row['solvent_capacity_unit'] == 'oz':
                row['solvent_amount'] = Decimal(row['solvent_amount']) * Decimal(row['solvent_capacity']) * Decimal(28.3495231) * Decimal(row['density']) * Decimal(row['gas_ratio']) / Decimal(100) / Decimal(1000) / Decimal(1000)
                row['solvent_amount'] = round(Decimal(row['solvent_amount']), 4)
                return row['solvent_amount']

            if row['solvent_capacity_unit'] == '公升':
                row['solvent_amount'] = Decimal(row['solvent_amount']) * Decimal(row['solvent_capacity']) * Decimal(row['density']) * Decimal(row['gas_ratio']) / Decimal(100) / Decimal(1000)
                row['solvent_amount'] = round(Decimal(row['solvent_amount']), 4)
                return row['solvent_amount']

        a_part['solvent_amount'] = a_part.apply(multiply, axis=1)
        a_part = a_part.drop(columns=['solvent_capacity_unit', 'solvent_capacity', 'gas_ratio', 'density']).drop_duplicates()
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source='質量平衡法').filter(cause__in=a_part['device_name']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(
            coefficient_unit=Value('公噸' + '/公噸', output_field=models.CharField(max_length=50)))))
        ab_part = pd.merge(a_part, coefficient_part, left_on='device_name', right_on='cause', how='left')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['solvent_amount']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        final = final.rename(columns={'solvent_name': 'fuel_type', 'solvent_amount': 'sum_count'})
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        return final
    except:
        print('沒有該溶劑、噴霧劑設備')
        return final


# 人天清冊
def personnel_inventory_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        raw_data = pd.DataFrame(list(personnel_inventory.objects.filter(years=years).filter(company_id=factory_id).values().annotate(
            process_area=Value('人為系統所釋放的溫室氣體產生的直接暫時性排放', output_field=models.CharField(max_length=50)),
            device_name=Value('化糞池', output_field=CharField(max_length=20)),
            fuel_type=Value('水肥', output_field=CharField(max_length=20)),
            data_unit=Value('人/時', output_field=models.CharField(max_length=50)),
        )))

        def classification_count(row):
            # 內部人員公式= 當月人數 * 當月每日工時 * 當月工作天數 + 當月加班時數 - 當月請假時數 - 當月補休時數
            if row['classification'] == '內部人員':
                sum_count = \
                    (Decimal(str(row['people_number_jan'])) * Decimal(str(row['daily_working_hours_jan'])) * Decimal(str(row['work_day_jan'])) + row['overtime_jan'] - row['leave_hours_jan'] - row['compensatory_leave_hours_jan']) + \
                    (Decimal(str(row['people_number_feb'])) * Decimal(str(row['daily_working_hours_feb'])) * Decimal(str(row['work_day_feb'])) + row['overtime_feb'] - row['leave_hours_feb'] - row['compensatory_leave_hours_feb']) + \
                    (Decimal(str(row['people_number_mar'])) * Decimal(str(row['daily_working_hours_mar'])) * Decimal(str(row['work_day_mar'])) + row['overtime_mar'] - row['leave_hours_mar'] - row['compensatory_leave_hours_mar']) + \
                    (Decimal(str(row['people_number_apr'])) * Decimal(str(row['daily_working_hours_apr'])) * Decimal(str(row['work_day_apr'])) + row['overtime_apr'] - row['leave_hours_apr'] - row['compensatory_leave_hours_apr']) + \
                    (Decimal(str(row['people_number_may'])) * Decimal(str(row['daily_working_hours_may'])) * Decimal(str(row['work_day_may'])) + row['overtime_may'] - row['leave_hours_may'] - row['compensatory_leave_hours_may']) + \
                    (Decimal(str(row['people_number_jun'])) * Decimal(str(row['daily_working_hours_jun'])) * Decimal(str(row['work_day_jun'])) + row['overtime_jun'] - row['leave_hours_jun'] - row['compensatory_leave_hours_jun']) + \
                    (Decimal(str(row['people_number_jul'])) * Decimal(str(row['daily_working_hours_jul'])) * Decimal(str(row['work_day_jul'])) + row['overtime_jul'] - row['leave_hours_jul'] - row['compensatory_leave_hours_jul']) + \
                    (Decimal(str(row['people_number_aug'])) * Decimal(str(row['daily_working_hours_aug'])) * Decimal(str(row['work_day_aug'])) + row['overtime_aug'] - row['leave_hours_aug'] - row['compensatory_leave_hours_aug']) + \
                    (Decimal(str(row['people_number_sept'])) * Decimal(str(row['daily_working_hours_sept'])) * Decimal(str(row['work_day_sept'])) + row['overtime_sept'] - row['leave_hours_sept'] - row['compensatory_leave_hours_sept']) + \
                    (Decimal(str(row['people_number_oct'])) * Decimal(str(row['daily_working_hours_oct'])) * Decimal(str(row['work_day_oct'])) + row['overtime_oct'] - row['leave_hours_oct'] - row['compensatory_leave_hours_oct']) + \
                    (Decimal(str(row['people_number_nov'])) * Decimal(str(row['daily_working_hours_nov'])) * Decimal(str(row['work_day_nov'])) + row['overtime_nov'] - row['leave_hours_nov'] - row['compensatory_leave_hours_nov']) + \
                    (Decimal(str(row['people_number_dec'])) * Decimal(str(row['daily_working_hours_dec'])) * Decimal(str(row['work_day_dec'])) + row['overtime_dec'] - row['leave_hours_dec'] - row['compensatory_leave_hours_dec'])
                return sum_count
            # 外部人員公式= 當月人數 * 當月每日工時 * 當月工作天數
            elif row['classification'] == '外部人員':
                sum_count = \
                    (Decimal(str(row['people_number_jan'])) * Decimal(str(row['daily_working_hours_jan'])) * Decimal(str(row['work_day_jan']))) + \
                    (Decimal(str(row['people_number_feb'])) * Decimal(str(row['daily_working_hours_feb'])) * Decimal(str(row['work_day_feb']))) + \
                    (Decimal(str(row['people_number_mar'])) * Decimal(str(row['daily_working_hours_mar'])) * Decimal(str(row['work_day_mar']))) + \
                    (Decimal(str(row['people_number_apr'])) * Decimal(str(row['daily_working_hours_apr'])) * Decimal(str(row['work_day_apr']))) + \
                    (Decimal(str(row['people_number_may'])) * Decimal(str(row['daily_working_hours_may'])) * Decimal(str(row['work_day_may']))) + \
                    (Decimal(str(row['people_number_jun'])) * Decimal(str(row['daily_working_hours_jun'])) * Decimal(str(row['work_day_jun']))) + \
                    (Decimal(str(row['people_number_jul'])) * Decimal(str(row['daily_working_hours_jul'])) * Decimal(str(row['work_day_jul']))) + \
                    (Decimal(str(row['people_number_aug'])) * Decimal(str(row['daily_working_hours_aug'])) * Decimal(str(row['work_day_aug']))) + \
                    (Decimal(str(row['people_number_sept'])) * Decimal(str(row['daily_working_hours_sept'])) * Decimal(str(row['work_day_sept']))) + \
                    (Decimal(str(row['people_number_oct'])) * Decimal(str(row['daily_working_hours_oct'])) * Decimal(str(row['work_day_oct']))) + \
                    (Decimal(str(row['people_number_nov'])) * Decimal(str(row['daily_working_hours_nov'])) * Decimal(str(row['work_day_nov']))) + \
                    (Decimal(str(row['people_number_dec'])) * Decimal(str(row['daily_working_hours_dec'])) * Decimal(str(row['work_day_dec'])))
                return sum_count
            # 宿舍公式= 當月人數 * (當月工作天數 + 當月公休天數) * 24 - (內部人員公式：當月人數 * 當月每日工時 * 當月工作天數 + 當月加班時數 - 當月請假時數 - 當月補休時數)
            elif row['classification'] == '宿舍':
                work_total =  \
                    (Decimal(str(row['people_number_jan'])) * Decimal(str(row['daily_working_hours_jan'])) * Decimal(str(row['work_day_jan'])) + row['overtime_jan'] - row['leave_hours_jan'] - row['compensatory_leave_hours_jan']) + \
                    (Decimal(str(row['people_number_feb'])) * Decimal(str(row['daily_working_hours_feb'])) * Decimal(str(row['work_day_feb'])) + row['overtime_feb'] - row['leave_hours_feb'] - row['compensatory_leave_hours_feb']) + \
                    (Decimal(str(row['people_number_mar'])) * Decimal(str(row['daily_working_hours_mar'])) * Decimal(str(row['work_day_mar'])) + row['overtime_mar'] - row['leave_hours_mar'] - row['compensatory_leave_hours_mar']) + \
                    (Decimal(str(row['people_number_apr'])) * Decimal(str(row['daily_working_hours_apr'])) * Decimal(str(row['work_day_apr'])) + row['overtime_apr'] - row['leave_hours_apr'] - row['compensatory_leave_hours_apr']) + \
                    (Decimal(str(row['people_number_may'])) * Decimal(str(row['daily_working_hours_may'])) * Decimal(str(row['work_day_may'])) + row['overtime_may'] - row['leave_hours_may'] - row['compensatory_leave_hours_may']) + \
                    (Decimal(str(row['people_number_jun'])) * Decimal(str(row['daily_working_hours_jun'])) * Decimal(str(row['work_day_jun'])) + row['overtime_jun'] - row['leave_hours_jun'] - row['compensatory_leave_hours_jun']) + \
                    (Decimal(str(row['people_number_jul'])) * Decimal(str(row['daily_working_hours_jul'])) * Decimal(str(row['work_day_jul'])) + row['overtime_jul'] - row['leave_hours_jul'] - row['compensatory_leave_hours_jul']) + \
                    (Decimal(str(row['people_number_aug'])) * Decimal(str(row['daily_working_hours_aug'])) * Decimal(str(row['work_day_aug'])) + row['overtime_aug'] - row['leave_hours_aug'] - row['compensatory_leave_hours_aug']) + \
                    (Decimal(str(row['people_number_sept'])) * Decimal(str(row['daily_working_hours_sept'])) * Decimal(str(row['work_day_sept'])) + row['overtime_sept'] - row['leave_hours_sept'] - row['compensatory_leave_hours_sept']) + \
                    (Decimal(str(row['people_number_oct'])) * Decimal(str(row['daily_working_hours_oct'])) * Decimal(str(row['work_day_oct'])) + row['overtime_oct'] - row['leave_hours_oct'] - row['compensatory_leave_hours_oct']) + \
                    (Decimal(str(row['people_number_nov'])) * Decimal(str(row['daily_working_hours_nov'])) * Decimal(str(row['work_day_nov'])) + row['overtime_nov'] - row['leave_hours_nov'] - row['compensatory_leave_hours_nov']) + \
                    (Decimal(str(row['people_number_dec'])) * Decimal(str(row['daily_working_hours_dec'])) * Decimal(str(row['work_day_dec'])) + row['overtime_dec'] - row['leave_hours_dec'] - row['compensatory_leave_hours_dec'])
                sum_count = \
                    (Decimal(str(row['people_number_jan'])) * (Decimal(str(row['work_day_jan'])) + row['holidays_jan']) * 24) + \
                    (Decimal(str(row['people_number_feb'])) * (Decimal(str(row['work_day_feb'])) + row['holidays_feb']) * 24) + \
                    (Decimal(str(row['people_number_mar'])) * (Decimal(str(row['work_day_mar'])) + row['holidays_mar']) * 24) + \
                    (Decimal(str(row['people_number_apr'])) * (Decimal(str(row['work_day_apr'])) + row['holidays_apr']) * 24) + \
                    (Decimal(str(row['people_number_may'])) * (Decimal(str(row['work_day_may'])) + row['holidays_may']) * 24) + \
                    (Decimal(str(row['people_number_jun'])) * (Decimal(str(row['work_day_jun'])) + row['holidays_jun']) * 24) + \
                    (Decimal(str(row['people_number_jul'])) * (Decimal(str(row['work_day_jul'])) + row['holidays_jul']) * 24) + \
                    (Decimal(str(row['people_number_aug'])) * (Decimal(str(row['work_day_aug'])) + row['holidays_aug']) * 24) + \
                    (Decimal(str(row['people_number_sept'])) * (Decimal(str(row['work_day_sept'])) + row['holidays_sept']) * 24) + \
                    (Decimal(str(row['people_number_oct'])) * (Decimal(str(row['work_day_oct'])) + row['holidays_oct']) * 24) + \
                    (Decimal(str(row['people_number_nov'])) * (Decimal(str(row['work_day_nov'])) + row['holidays_nov']) * 24) + \
                    (Decimal(str(row['people_number_dec'])) * (Decimal(str(row['work_day_dec'])) + row['holidays_dec']) * 24) - work_total
                return sum_count

        raw_data['sum_count'] = raw_data.apply(classification_count, axis=1)
        raw_data['sum_count'] = raw_data['sum_count'].apply(lambda x: round(x, 4))
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause__in=raw_data['fuel_type']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(
            coefficient_unit=Value('公噸' + '/人時', output_field=models.CharField(max_length=50)))))
        ab_part = pd.merge(raw_data, coefficient_part, left_on='fuel_type', right_on='cause', how='left')
        ab_part['fuel_type'] = ab_part.apply(lambda x: f"{x['fuel_type']} - {x['classification']}", axis=1)
        ab_part = ab_part.drop(columns=['cause'])
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        return final
    except:
        print('沒有該滅火器設備')
        return final


# 滅火器
def extinguisher_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        raw_data = pd.DataFrame(list(extinguisher.objects.filter(years=years).filter(company_id=factory_id).values('extinguisher_type').annotate(
            process_area=Value('逸散', output_field=models.CharField(max_length=50)),
            device_name=Value('滅火器', output_field=models.CharField(max_length=50)),
            sum_count=Cast(Sum(F('chemical_weight') * F('inventory')) / 1000, output_field=models.DecimalField(max_digits=20, decimal_places=4)),
            data_unit=Value('公噸', output_field=models.CharField(max_length=50))))
        )
        a_part = raw_data

        def extinguisher_gas(row):
            if row['extinguisher_type'] == 'CO2滅火器':
                return 'CO2'
            else:
                return 'HFCs'

        a_part['gas_name'] = a_part.apply(extinguisher_gas, axis=1)
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source='質量平衡法').filter(cause__in=a_part['device_name']).values('gas_name', 'coefficient', 'coefficient_source').annotate(
            coefficient_unit=Value('公噸' + '/公噸', output_field=models.CharField(max_length=50)))))
        ab_part = pd.merge(a_part, coefficient_part, on='gas_name', how='left')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        final = final.rename(columns={'extinguisher_type': 'fuel_type'})
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        return final
    except:
        print('沒有該滅火器設備')
        return final


# 厭氧廢水
def waste_water_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        # years = 2023
        # factory_id = 1
        # coefficient_source = '環保署溫室氣體排放係數管理表6.0.4'
        # gwp_version = 6
        # raw_data = pd.DataFrame(list(waste_water.objects.filter(years=years).filter(company_id=factory_id).values('did').annotate(
        #     process_area=Value('逸散', output_field=models.CharField(max_length=50)),
        #     device_name=Value('厭氧廢水處理', output_field=models.CharField(max_length=50)),
        #     fuel_type=Value('厭氧處理', output_field=models.CharField(max_length=50)),
        #     sum_count=Sum(F('Pi') * F('Wi') * F('CODi') - F('Si')) * (F('Bo') * F('MCFj') - F('Ri')),
        #     data_unit=Value('公噸', output_field=models.CharField(max_length=50))))).assign(dummy='1')
        data = waste_water.objects.filter(years=years).filter(company_id=factory_id).values('did').annotate(
            process_area=Value('逸散', output_field=CharField(max_length=50)),
            device_name=Value('厭氧廢水處理', output_field=CharField(max_length=50)),
            fuel_type=Value('厭氧處理', output_field=CharField(max_length=50)),
            Pi=F('Pi'),
            Wi=F('Wi'),
            CODi=F('CODi'),
            Si=F('Si'),
            Bo=F('Bo'),
            MCFj=F('MCFj'),
            Ri=F('Ri'),
            data_unit=Value('公噸', output_field=CharField(max_length=50))
        )

        # DataFrame
        raw_data = pd.DataFrame(list(data))

        # 計算 sum_count
        for i in raw_data.index:
            Pi = raw_data.loc[i, 'Pi']
            Wi = raw_data.loc[i, 'Wi']
            CODi = raw_data.loc[i, 'CODi']
            Si = raw_data.loc[i, 'Si']
            Bo = raw_data.loc[i, 'Bo']
            MCFj = raw_data.loc[i, 'MCFj']
            Ri = raw_data.loc[i, 'Ri']

            if Pi is not None:
                ch4 = (Pi * Wi * CODi - Si) * (Bo * MCFj) - Ri
            else:
                ch4 = (Wi * CODi - Si) * (Bo * MCFj) - Ri

            consumption_total = Decimal(ch4).quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
            raw_data.loc[i, 'sum_count'] = consumption_total
        a_part = raw_data
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause__in=a_part['fuel_type']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(
            coefficient_unit=Value('公噸' + '/公噸', output_field=models.CharField(max_length=50)))))
        ab_part = pd.merge(a_part, coefficient_part, left_on='fuel_type', right_on='cause', how='left').drop(columns=['cause', 'did', 'Pi', 'Wi', 'CODi', 'Si', 'Bo', 'MCFj', 'Ri'])
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        final = final.rename(columns={'meter_location': 'device_name'})
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        return final
    except:
        print('沒有該厭氧廢水設備')
        return final


# 用電量 (第二類)
def electricity_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        raw_data = pd.DataFrame(list(electricity.objects.filter(years=years).filter(company_id=factory_id).values('meter_location').annotate(
            process_area=Value('輸入能源', output_field=models.CharField(max_length=50)),
            sum_count=Cast(Sum(F('january') + F('february') + F('march') + F('april') + F('may') + F('june') +
                               F('july') + F('august') + F('september') + F('october') + F('november') + F('december')) / 1000, output_field=models.DecimalField(max_digits=20, decimal_places=4)),
            fuel_type=Value('外購電力', output_field=models.CharField(max_length=50)),
            data_unit=Value('千度', output_field=models.CharField(max_length=50))))).assign(dummy='1')
        a_part = raw_data
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source='111年度電力排碳係數').filter(cause__in=a_part['fuel_type']).values('gas_name', 'coefficient', 'coefficient_source').annotate(
            coefficient_unit=Value('公噸' + '/千度', output_field=models.CharField(max_length=50))))).assign(dummy='1')
        ab_part = pd.merge(a_part, coefficient_part, on='dummy', how='left').drop(columns='dummy')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        final = final.rename(columns={'meter_location': 'device_name'})
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        return final
    except:
        print('沒有該用電量設備')
        return final


# 上游運輸 (第三類)
def upstream_transport_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        # years = 2023
        # factory_id = 1
        # coefficient_source = '環保署溫室氣體排放係數管理表6.0.4'
        # gwp_version = 6
        # 陸運資料
        transport_raw_data = pd.DataFrame(list(upstream_transportation.objects.filter(years=years).filter(company_id=factory_id).values('commodity_NW', 'transport_type', 'transport_fuel', 'transport_distance', 'trips').annotate(
            process_area=Value('由貨物上游運輸與分配產生之排放', output_field=models.CharField(max_length=50)),
            device_name=Value('陸運運輸', output_field=models.CharField(max_length=50)),
            data_unit=Value('延噸公里', output_field=models.CharField(max_length=50)))))
        downstream_transport_raw_data = pd.DataFrame(list(downstream_transportation.objects.filter(years=years).filter(company_id=factory_id).filter(paid='客戶支付(上游計算)').values('commodity_NW', 'transport_type', 'transport_fuel', 'transport_distance', 'trips').annotate(
            process_area=Value('由貨物上游運輸與分配產生之排放(下游運輸我方支付)', output_field=models.CharField(max_length=50)),
            device_name=Value('陸運運輸', output_field=models.CharField(max_length=50)),
            data_unit=Value('延噸公里', output_field=models.CharField(max_length=50)))))
        transport_part = pd.concat([transport_raw_data, downstream_transport_raw_data])
        transport_part['fuel_type'] = transport_part.apply(lambda x: f"{x['transport_type']}({x['transport_fuel']})", axis=1)
        transport_part['sum_count'] = transport_part.apply(lambda x: round(Decimal(x['commodity_NW']) * Decimal(x['transport_distance']) * Decimal(x['trips']), 4), axis=1)
        transport_part = transport_part.groupby(['process_area', 'fuel_type']).agg({'device_name': 'first', 'sum_count': 'sum', 'data_unit': 'first'}).reset_index()

        # 海運資料
        overseas_raw_data = pd.DataFrame(list(upstream_transportation.objects.filter(years=years).filter(company_id=factory_id).values('commodity_NW', 'overseas_transport_distance_km', 'overseas_trips').annotate(
            process_area=Value('由貨物上游運輸與分配產生之排放', output_field=models.CharField(max_length=50)),
            device_name=Value('海運運輸', output_field=models.CharField(max_length=50)),
            fuel_type=Value('國際海運貨物運輸服務(本國籍貨櫃船，歐美長程航線)', output_field=models.CharField(max_length=50)),
            data_unit=Value('延噸公里', output_field=models.CharField(max_length=50)))))
        downstream_overseas_raw_data = pd.DataFrame(list(downstream_transportation.objects.filter(years=years).filter(company_id=factory_id).filter(paid='客戶支付(上游計算)').values('commodity_NW', 'overseas_transport_distance_km', 'overseas_trips').annotate(
            process_area=Value('由貨物上游運輸與分配產生之排放', output_field=models.CharField(max_length=50)),
            device_name=Value('海運運輸', output_field=models.CharField(max_length=50)),
            fuel_type=Value('國際海運貨物運輸服務(本國籍貨櫃船，歐美長程航線)', output_field=models.CharField(max_length=50)),
            data_unit=Value('延噸公里', output_field=models.CharField(max_length=50)))))
        overseas_part = pd.concat([overseas_raw_data, downstream_overseas_raw_data])
        # 删除包含空值的行
        overseas_part.dropna(subset=['overseas_transport_distance_km', 'overseas_trips'], inplace=True)
        overseas_part['sum_count'] = overseas_part.apply(lambda x: round(Decimal(x['commodity_NW']) * Decimal(x['overseas_transport_distance_km']) * Decimal(x['overseas_trips']), 4), axis=1)
        overseas_part = overseas_part.groupby(['process_area', 'fuel_type']).agg({'device_name': 'first', 'sum_count': 'sum', 'data_unit': 'first'}).reset_index()

        # 二段陸運資料
        second_transport_raw_data = pd.DataFrame(list(upstream_transportation.objects.filter(years=years).filter(company_id=factory_id).values('commodity_NW', 'special_transport_type', 'special_transport_fuel', 'special_transport_distance', 'special_trips').annotate(
            process_area=Value('由貨物上游運輸與分配產生之排放', output_field=models.CharField(max_length=50)),
            device_name=Value('二段陸運運輸', output_field=models.CharField(max_length=50)),
            data_unit=Value('延噸公里', output_field=models.CharField(max_length=50)))))
        downstream_second_transport_raw_data = pd.DataFrame(list(downstream_transportation.objects.filter(years=years).filter(company_id=factory_id).filter(special_paid='客戶支付(上游計算)').values('commodity_NW', 'special_transport_type', 'special_transport_fuel', 'special_transport_distance', 'special_trips').annotate(
            process_area=Value('由貨物上游運輸與分配產生之排放(下游運輸我方支付)', output_field=models.CharField(max_length=50)),
            device_name=Value('二段陸運運輸', output_field=models.CharField(max_length=50)),
            data_unit=Value('延噸公里', output_field=models.CharField(max_length=50)))))
        special_part = pd.concat([second_transport_raw_data, downstream_second_transport_raw_data])
        # 删除包含空值的行
        special_part.dropna(subset=['special_transport_distance', 'special_trips'], inplace=True)
        special_part['fuel_type'] = special_part.apply(lambda x: f"{x['special_transport_type']}({x['special_transport_fuel']})", axis=1)
        special_part['sum_count'] = special_part.apply(lambda x: round(Decimal(x['commodity_NW']) * Decimal(x['special_transport_distance']) * Decimal(x['special_trips']), 4), axis=1)
        special_part = special_part.groupby(['process_area', 'fuel_type']).agg({'device_name': 'first', 'sum_count': 'sum', 'data_unit': 'first'}).reset_index()

        # 空運資料
        air_raw_data = pd.DataFrame(list(upstream_transportation.objects.filter(years=years).filter(company_id=factory_id).values('commodity_NW', 'air_transport_distance', 'air_trips').annotate(
            process_area=Value('由貨物上游運輸與分配產生之排放', output_field=models.CharField(max_length=50)),
            device_name=Value('空運運輸', output_field=models.CharField(max_length=50)),
            fuel_type=Value('航空貨物運輸服務', output_field=models.CharField(max_length=50)),
            data_unit=Value('延噸公里', output_field=models.CharField(max_length=50)))))
        downstream_air_raw_data = pd.DataFrame(list(downstream_transportation.objects.filter(years=years).filter(company_id=factory_id).filter(paid='客戶支付(上游計算)').values('commodity_NW', 'air_transport_distance', 'air_trips').annotate(
            process_area=Value('由貨物上游運輸與分配產生之排放', output_field=models.CharField(max_length=50)),
            device_name=Value('空運運輸', output_field=models.CharField(max_length=50)),
            fuel_type=Value('航空貨物運輸服務', output_field=models.CharField(max_length=50)),
            data_unit=Value('延噸公里', output_field=models.CharField(max_length=50)))))
        air_part = pd.concat([air_raw_data, downstream_air_raw_data])
        # 删除包含空值的行
        air_part.dropna(subset=['air_transport_distance', 'air_trips'], inplace=True)
        air_part['sum_count'] = air_part.apply(lambda x: round(Decimal(x['commodity_NW']) * Decimal(x['air_transport_distance']) * Decimal(x['air_trips']), 4), axis=1)
        air_part = air_part.groupby(['process_area', 'fuel_type']).agg({'device_name': 'first', 'sum_count': 'sum', 'data_unit': 'first'}).reset_index()

        # 將四種運輸方式合併起來抓取係數並輸出
        a_part = pd.concat([transport_part, overseas_part, special_part, air_part])
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source='產品碳足跡資訊網').filter(cause__in=a_part['fuel_type']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(
                    coefficient_unit=Value('公噸' + '/延噸公里', output_field=models.CharField(max_length=50)))))
        ab_part = pd.merge(a_part, coefficient_part, left_on='fuel_type', right_on='cause', how='left')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        print(final)
        return final
    except:
        print('沒有該上游運輸設備')
        return final


# 下游運輸 (第三類)
def downstream_transport_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        # years = 2023
        # factory_id = 1
        # coefficient_source = '環保署溫室氣體排放係數管理表6.0.4'
        # gwp_version = 6
        # 陸運資料
        transport_part = pd.DataFrame(list(downstream_transportation.objects.filter(years=years).filter(company_id=factory_id).filter(paid='我方支付').values('commodity_NW', 'transport_type', 'transport_fuel', 'transport_distance', 'trips').annotate(
            process_area=Value('由貨物下游運輸與分配產生之排放', output_field=models.CharField(max_length=50)),
            device_name=Value('陸運運輸', output_field=models.CharField(max_length=50)),
            data_unit=Value('延噸公里', output_field=models.CharField(max_length=50)))))
        transport_part['fuel_type'] = transport_part.apply(lambda x: f"{x['transport_type']}({x['transport_fuel']})", axis=1)
        transport_part['sum_count'] = transport_part.apply(lambda x: round(Decimal(x['commodity_NW']) * Decimal(x['transport_distance']) * Decimal(x['trips']), 4), axis=1)
        transport_part = transport_part.groupby(['process_area', 'fuel_type']).agg({'device_name': 'first', 'sum_count': 'sum', 'data_unit': 'first'}).reset_index()
        # 海運資料
        overseas_part = pd.DataFrame(list(downstream_transportation.objects.filter(years=years).filter(company_id=factory_id).filter(paid='我方支付').values('commodity_NW', 'overseas_transport_distance_km', 'overseas_trips').annotate(
            process_area=Value('由貨物上游運輸與分配產生之排放', output_field=models.CharField(max_length=50)),
            device_name=Value('海運運輸', output_field=models.CharField(max_length=50)),
            fuel_type=Value('國際海運貨物運輸服務(本國籍貨櫃船，歐美長程航線)', output_field=models.CharField(max_length=50)),
            data_unit=Value('延噸公里', output_field=models.CharField(max_length=50)))))
        # 删除包含空值的行
        overseas_part.dropna(subset=['overseas_transport_distance_km', 'overseas_trips'], inplace=True)
        overseas_part['sum_count'] = overseas_part.apply(lambda x: round(Decimal(x['commodity_NW']) * Decimal(x['overseas_transport_distance_km']) * Decimal(x['overseas_trips']), 4), axis=1)
        overseas_part = overseas_part.groupby(['process_area', 'fuel_type']).agg({'device_name': 'first', 'sum_count': 'sum', 'data_unit': 'first'}).reset_index()

        # 二段陸運資料
        special_part = pd.DataFrame(list(downstream_transportation.objects.filter(years=years).filter(company_id=factory_id).filter(special_paid='我方支付').values('commodity_NW', 'special_transport_type', 'special_transport_fuel', 'special_transport_distance', 'special_trips').annotate(
            process_area=Value('由貨物上游運輸與分配產生之排放(下游運輸我方支付)', output_field=models.CharField(max_length=50)),
            device_name=Value('二段陸運運輸', output_field=models.CharField(max_length=50)),
            data_unit=Value('延噸公里', output_field=models.CharField(max_length=50)))))
        # 删除包含空值的行
        special_part.dropna(subset=['special_transport_distance', 'special_trips'], inplace=True)
        special_part['fuel_type'] = special_part.apply(lambda x: f"{x['special_transport_type']}({x['special_transport_fuel']})", axis=1)
        special_part['sum_count'] = special_part.apply(lambda x: round(Decimal(x['commodity_NW']) * Decimal(x['special_transport_distance']) * Decimal(x['special_trips']), 4), axis=1)
        special_part = special_part.groupby(['process_area', 'fuel_type']).agg({'device_name': 'first', 'sum_count': 'sum', 'data_unit': 'first'}).reset_index()

        # 空運資料
        air_part = pd.DataFrame(list(downstream_transportation.objects.filter(years=years).filter(company_id=factory_id).filter(paid='我方支付').values('commodity_NW', 'air_transport_distance', 'air_trips').annotate(
            process_area=Value('由貨物上游運輸與分配產生之排放', output_field=models.CharField(max_length=50)),
            device_name=Value('空運運輸', output_field=models.CharField(max_length=50)),
            fuel_type=Value('航空貨物運輸服務', output_field=models.CharField(max_length=50)),
            data_unit=Value('延噸公里', output_field=models.CharField(max_length=50)))))
        # 删除包含空值的行
        air_part.dropna(subset=['air_transport_distance', 'air_trips'], inplace=True)
        air_part['sum_count'] = air_part.apply(lambda x: round(Decimal(x['commodity_NW']) * Decimal(x['air_transport_distance']) * Decimal(x['air_trips']), 4), axis=1)
        air_part = air_part.groupby(['process_area', 'fuel_type']).agg({'device_name': 'first', 'sum_count': 'sum', 'data_unit': 'first'}).reset_index()

        # 將四種運輸方式合併起來抓取係數並輸出
        a_part = pd.concat([transport_part, overseas_part, special_part, air_part])
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source='產品碳足跡資訊網').filter(cause__in=a_part['fuel_type']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(
                    coefficient_unit=Value('公噸' + '/延噸公里', output_field=models.CharField(max_length=50)))))
        ab_part = pd.merge(a_part, coefficient_part, left_on='fuel_type', right_on='cause', how='left')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        return final
    except:
        print('沒有該上游運輸設備')
        return final


# 員工通勤 (第三類)
def employee_commute_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        # years = 2023
        # factory_id = 1
        # coefficient_source = '環保署溫室氣體排放係數管理表6.0.4'
        # gwp_version = 6
        raw_data = pd.DataFrame(list(employee_commute.objects.filter(years=years).filter(company_id=factory_id).values('id', 'commute_distance', 'work_days').annotate(
            process_area=Value('員工通勤產生之排放', output_field=models.CharField(max_length=50)),
            fuel_type=Value('汽油', output_field=CharField(max_length=20)),
            data_unit=Value('延人公里', output_field=models.CharField(max_length=50)))))
        transportation_data = pd.DataFrame(list(transportation_way.objects.values('transportation', 'commute_id')))
        a_part = pd.merge(raw_data, transportation_data, left_on='id', right_on='commute_id', how='left')
        a_part['sum_count'] = a_part.apply(lambda x: round(Decimal(x['commute_distance']) * Decimal(x['work_days']) * Decimal('2'), 4), axis=1)

        def transportations(row):
            if row['transportation'] == '機車':
                return '機器腳踏車(汽油)'
            elif row['transportation'] == '電動機車':
                return '電動機車'
            elif row['transportation'] == '汽車(汽油)':
                return '自用小客車(汽油)'
            elif row['transportation'] == '汽車(柴油)':
                return '汽車(柴油)'
            elif row['transportation'] == '汽車(油電)':
                return '汽車(油電)'
            elif row['transportation'] == '公車':
                return '公車'
            elif row['transportation'] == '火車':
                return '臺灣鐵路運輸服務(電聯車)'
            elif row['transportation'] == '捷運':
                return '捷運'
            elif row['transportation'] == '高鐵':
                return '高速鐵路運輸服務'
            else:
                return row['transportation']

        a_part['transportation'] = a_part.apply(transportations, axis=1)
        a_part = a_part.groupby(['transportation']).agg({'sum_count': 'sum', 'process_area': 'first', 'fuel_type': 'first', 'data_unit': 'first'}).reset_index()
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source='產品碳足跡資訊網').filter(cause__in=a_part['transportation']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(
            coefficient_unit=Value('公斤' + '/延人公里', output_field=models.CharField(max_length=50)))))
        ab_part = pd.merge(a_part, coefficient_part, left_on='transportation', right_on='cause', how='left')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']) / Decimal('1000'), 4), axis=1)
        final = final.rename(columns={'transportation': 'device_name'})
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        return final
    except:
        print('沒有該員工通勤設備')
        return final


# 員工出差 (第三類)
def employee_business_trip_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        raw_data = pd.DataFrame(list(employee_business_trip.objects.filter(years=years).filter(company_id=factory_id).values('id').annotate(
            process_area=Value('員工出差產生之排放', output_field=models.CharField(max_length=50)),
            fuel_type=Value('汽油', output_field=CharField(max_length=20)),
            data_unit=Value('延人公里', output_field=models.CharField(max_length=50)))))
        trip_section_data = pd.DataFrame(list(trip_section.objects.values('transportation', 'distance', 'trip_id')))
        a_part = pd.merge(raw_data, trip_section_data, left_on='id', right_on='trip_id', how='left')

        def transportations(row):
            if row['transportation'] == '汽車':
                return '自用小客車(汽油)'
            elif row['transportation'] == '火車':
                return '臺灣鐵路運輸服務(電聯車)'
            elif row['transportation'] == '高鐵':
                return '高速鐵路運輸服務'
            elif row['transportation'] == '捷運':
                return '捷運'
            elif row['transportation'] == '船舶':
                return '船舶'
            elif row['transportation'] == '飛機':
                return '飛機'
            else:
                return row['transportation']

        a_part['transportation'] = a_part.apply(transportations, axis=1)
        a_part = a_part.groupby(['transportation']).agg({'distance': 'sum', 'process_area': 'first', 'fuel_type': 'first', 'data_unit': 'first'}).reset_index()
        a_part = a_part.rename(columns={'distance': 'sum_count'})
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source='產品碳足跡資訊網').filter(cause__in=a_part['transportation']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(
            coefficient_unit=Value('公斤' + '/延人公里', output_field=models.CharField(max_length=50)))))
        ab_part = pd.merge(a_part, coefficient_part, left_on='transportation', right_on='cause', how='left')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']) / Decimal('1000'), 4), axis=1)
        final = final.rename(columns={'transportation': 'device_name'})
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        return final
    except:
        print('沒有該員工出差設備')
        return final


# 廢棄物運輸 (第三類)
def waste_transport_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        raw_data = pd.DataFrame(list(
            waste.objects.filter(years=years).filter(company_id=factory_id).exclude(transport_type__isnull=True).exclude(transport_fuel__isnull=True).exclude(transport_distance__isnull=True).values('waste_weigh', 'waste_disposal', 'transport_type', 'transport_fuel', 'transport_distance').annotate(
                process_area=Value('由廢棄物運輸產生之排放', output_field=models.CharField(max_length=50)),
                sum_count=Cast(Sum(F('waste_weigh') * F('transport_distance')), output_field=models.DecimalField(max_digits=20, decimal_places=4)),
                data_unit=Value('延噸公里', output_field=models.CharField(max_length=50)))))
        raw_data = raw_data.assign(
            waste_disposal=raw_data['waste_disposal'].apply(lambda x: '廢棄物運輸- ' + x)
        )
        raw_data = raw_data.groupby(['waste_disposal', 'transport_type', 'transport_fuel']).agg({'waste_weigh': 'first', 'transport_distance': 'sum', 'sum_count': 'sum', 'process_area': 'first', 'data_unit': 'first'}).reset_index()
        raw_data['new_transport'] = raw_data.apply(lambda x: f"{x['transport_type']}({x['transport_fuel']})", axis=1)
        a_part = raw_data
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source='產品碳足跡資訊網').filter(cause__in=a_part['new_transport']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(
            coefficient_unit=Value('公噸' + '/延噸公里', output_field=models.CharField(max_length=50)))))
        ab_part = pd.merge(a_part, coefficient_part, left_on='new_transport', right_on='cause', how='left')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        final = final.rename(columns={'waste_disposal': 'device_name', 'new_transport': 'fuel_type'})
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        return final
    except:
        print('沒有該廢棄物運輸設備')
        return final


# 廢棄物處理 (第四類)
def waste_process_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        raw_data = pd.DataFrame(list(waste.objects.filter(years=years).filter(company_id=factory_id).values('waste_disposal', 'waste_name', 'waste_location', 'waste_weigh').annotate(
            process_area=Value('公司營運所產生廢棄物處置', output_field=models.CharField(max_length=50)),
            data_unit=Value('公噸', output_field=models.CharField(max_length=50)))))
        raw_data = raw_data.groupby(['waste_disposal']).agg({'waste_name': 'first', 'waste_weigh': 'sum', 'process_area': 'first', 'data_unit': 'first', 'waste_location': 'first'}).reset_index()
        a_part = raw_data.rename(columns={'waste_weigh': 'sum_count'})
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source='產品碳足跡資訊網').filter(cause__in=a_part['waste_location']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(
            coefficient_unit=Value('公噸' + '/延噸公里', output_field=models.CharField(max_length=50)))))
        ab_part = pd.merge(a_part, coefficient_part, left_on='waste_location', right_on='cause', how='left')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        final = final.rename(columns={'waste_disposal': 'device_name', 'waste_name': 'fuel_type'})
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        return final
    except:
        print('沒有該廢棄物處理設備')
        return final


# 採購原物料 (第四類)
def purchase_material_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        raw_data = pd.DataFrame(list(purchase_material.objects.filter(years=years).filter(company_id=factory_id).values('product_name', 'category_name').annotate(
            process_area=Value('組織購買原物料', output_field=models.CharField(max_length=50)),
            device_name=Value('原物料採購', output_field=models.CharField(max_length=50)),
            sum_count=Cast(Sum(F('january') + F('february') + F('march') + F('april') + F('may') + F('june') +
                               F('july') + F('august') + F('september') + F('october') + F('november') + F('december')), output_field=models.DecimalField(max_digits=20, decimal_places=4)),
            data_unit=Value('公噸', output_field=models.CharField(max_length=50)))))
        a_part = raw_data
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source='產品碳足跡資訊網').filter(cause__in=a_part['category_name']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(
            coefficient_unit=Value('公噸' + '/延噸公里', output_field=models.CharField(max_length=50)))))
        ab_part = pd.merge(a_part, coefficient_part, left_on='category_name', right_on='cause', how='left')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        final = final.rename(columns={'product_name': 'fuel_type'})
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        return final
    except:
        print('沒有該原物料採購設備')
        return final
