import datetime
from urllib import request, parse
import pandas as pd
from IPython.core.display import display
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Value, CharField
from django.db.models.functions import Cast
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
    if request.method == "POST":
        coefficient_source = request.POST.get("coefficient_source")
        gwp_version = request.POST.get("gwpVersion")
        gwp_version = int(gwp_version)
        # 判斷使用者是否為公司帳號。
        if request.user.groups.filter(name='公司帳號').exists():
            factory_id = request.session.get('company_id')
        else:
            factory_id = request.session.get('factory_id')
        years = request.session.get('years')
        if years is None:
            years = str(datetime.date.today().year)

        try:
            company_name = str(factory.objects.filter(id=factory_id).get())
            print('company_name', company_name)
        except:
            company_name = ''

        emergency_generators_device = emergency_generators_count(years, factory_id, coefficient_source, gwp_version)
        combustion_equipment_device = combustion_equipment_count(years, factory_id, coefficient_source, gwp_version)
        official_car_device = official_car_count(years, factory_id, coefficient_source, gwp_version)
        refrigerator_device = refrigerator_count(years, factory_id, coefficient_source, gwp_version)
        airconditioner_device = airconditioner_count(years, factory_id, coefficient_source, gwp_version)
        vehicle_device = vehicle_count(years, factory_id, coefficient_source, gwp_version)
        water_dispenser_device = water_dispenser_count(years, factory_id, coefficient_source, gwp_version)
        ice_water_dispenser_device = ice_water_dispenser_count(years, factory_id, coefficient_source, gwp_version)
        ice_maker_device = ice_maker_count(years, factory_id, coefficient_source, gwp_version)
        other_device_device = other_device_count(years, factory_id, coefficient_source, gwp_version)
        solvent_aerosol_emission_sources_device = solvent_aerosol_emission_sources_count(years, factory_id, coefficient_source, gwp_version)
        personnel_inventory_device = personnel_inventory_count(years, factory_id, coefficient_source, gwp_version)
        employee_device = employee_count(years, factory_id, coefficient_source, gwp_version)
        extinguisher_device = extinguisher_count(years, factory_id, coefficient_source, gwp_version)
        waste_water_device = waste_water_count(years, factory_id, coefficient_source, gwp_version)
        electricity_device = electricity_count(years, factory_id, coefficient_source, gwp_version)
        employee_commute_device = employee_commute_count(years, factory_id, coefficient_source, gwp_version)
        employee_business_trip_device = employee_business_trip_count(years, factory_id, coefficient_source, gwp_version)
        waste_transport_device = waste_transport_count(years, factory_id, coefficient_source, gwp_version)
        waste_process_device = waste_process_count(years, factory_id, coefficient_source, gwp_version)
        purchase_material_device = purchase_material_count(years, factory_id, coefficient_source, gwp_version)

        output = pd.concat([emergency_generators_device, combustion_equipment_device, official_car_device, refrigerator_device, airconditioner_device,
                            vehicle_device, water_dispenser_device, ice_water_dispenser_device, ice_maker_device, other_device_device, solvent_aerosol_emission_sources_device,
                            personnel_inventory_device, employee_device, extinguisher_device, waste_water_device, electricity_device, employee_commute_device,
                            employee_business_trip_device, waste_transport_device, waste_process_device, purchase_material_device])

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
        raw_data = combustion_equipment.objects.filter(years=years).filter(company_id=factory_id).values('device_name', 'fuel_type').annotate(
            process_area=Value('固定式燃燒', output_field=models.CharField(max_length=50)),
            sum_count=Cast(Sum(F('fuel_january') + F('fuel_february') + F('fuel_march') + F('fuel_april') + F('fuel_may') + F('fuel_june') + F('fuel_july') + F('fuel_august') + F('fuel_september') + F('fuel_october') + F('fuel_november') + F('fuel_december')) * 1.818 / 1000,
                           output_field=models.DecimalField(max_digits=20, decimal_places=4)),
            data_unit=Value('公秉', output_field=models.CharField(max_length=50))
        ).order_by('device_name', 'fuel_type')
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
        final['emission'] = final.apply(lambda x: (Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient'])).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP), axis=1)
        # final['emission'] = final.apply(lambda x: round(float(x['sum_count']) * float(x['coefficient']) * float(x['gwp_coefficient']), 4), axis=1)
        # display(final['emission'])
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
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
        raw_data = official_car.objects.filter(years=years).filter(company_id=factory_id).values('vehicle_type', 'fuel_type').annotate(
            process_area=Value('移動式式燃燒', output_field=models.CharField(max_length=50)),
            sum_count=Cast(Sum(F('january') + F('february') + F('march') + F('april') + F('may') + F('june') +
                               F('july') + F('august') + F('september') + F('october') + F('november') + F('december')) / 1000,
                           output_field=models.DecimalField(max_digits=20, decimal_places=4)),
            data_unit=Value('公秉', output_field=models.CharField(max_length=50))
        ).order_by('vehicle_type', 'fuel_type')
        coefficient_part = None
        for query in raw_data:
            fuel_type = query['fuel_type']
            if fuel_type in ['92汽油', '95汽油', '98汽油']:
                fuel_type = '車用汽油'
            coefficient_data = coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause=fuel_type).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(coefficient_unit=Value('公噸' + '/公秉', output_field=models.CharField(max_length=50)))
            coefficient_part = pd.DataFrame(list(coefficient_data))
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=coefficient_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        raw_data = pd.DataFrame(list(raw_data))
        a_b_part = pd.merge(raw_data, coefficient_part, left_on='fuel_type', right_on='cause', how='left')
        final = pd.merge(a_b_part, gwp, left_on='gas_name', right_on='gas_name', how='left')
        # 將(A)、(B)、(C)轉為float才能取round
        final['emission'] = final.apply(lambda x: round(Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        # final['emission'] = final.apply(lambda x: round(float(x['sum_count']) * float(x['coefficient']) * float(x['gwp_coefficient']), 4), axis=1)
        final = final.rename(columns={'vehicle_type': 'device_name'})
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        # display(final)
        # display(final.shape)
        return final
    except:
        print('沒有該公務車設備')
        return final


# 逸散(冰箱~其他設備)
# coefficient_source = '環保署溫室氣體排放係數管理表6.0.4'
# gwp_version = 6
# refrigerator = pd.DataFrame(list(refrigerator.objects.values("device_name", "refrigerant_type", "filling_volume")))
# airconditioner = pd.DataFrame(list(airconditioner.objects.values("device_name", "refrigerant_type", "filling_volume")))
# vehicle = pd.DataFrame(list(vehicle.objects.values("device_name", "refrigerant_type", "filling_volume")))
# ice_maker = pd.DataFrame(list(ice_maker.objects.values("device_name", "refrigerant_type", "filling_volume")))


# 冰箱
def refrigerator_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        raw_data = pd.DataFrame(list(refrigerator.objects.filter(years=years).filter(company_id=factory_id).values("refrigerant_type", "filling_volume").annotate(
            process_area=Value('逸散', output_field=models.CharField(max_length=50)),
            device_name=Value('冰箱', output_field=models.CharField(max_length=50)),
            data_unit=Value('公噸', output_field=models.CharField(max_length=50))))).assign(dummy='1')
        calculate = raw_data.groupby(["refrigerant_type"]).agg({'filling_volume': 'sum'}).reset_index()
        calculate['filling_volume'] = calculate['filling_volume'].apply(lambda x: round(Decimal(x) / Decimal(1000), 4))
        # 丟掉舊欄位，為了merge時欄位不會重複
        raw_data = raw_data.drop(columns=['filling_volume'])
        a_part = raw_data.merge(calculate, on=['refrigerant_type'], how='left').drop_duplicates()
        # 用dataframe欄位去filter queryset要用'欄位名稱__in'
        coefficient_part = pd.DataFrame(
            list(coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause__in=a_part['device_name']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(coefficient_unit=Value('公噸' + '/公噸', output_field=models.CharField(max_length=50))))).assign(
            dummy='1')
        ab_part = pd.merge(a_part, coefficient_part, on='dummy', how='left').drop(columns='dummy')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['refrigerant_type']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, left_on='refrigerant_type', right_on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['filling_volume']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        final = final.rename(columns={'refrigerant_type': 'fuel_type', 'filling_volume': 'sum_count', 'gas_name_x': 'gas_name'})
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        return final
    except:
        print('沒有該冰箱設備')
        return final


# 冷氣機
def airconditioner_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        raw_data = pd.DataFrame(
            list(airconditioner.objects.filter(years=years).filter(company_id=factory_id).values("refrigerant_type", "filling_volume").annotate(process_area=Value('逸散', output_field=models.CharField(max_length=50)), device_name=Value('冷氣機', output_field=models.CharField(max_length=50)),
                                                                                                                                                data_unit=Value('公噸', output_field=models.CharField(max_length=50))))).assign(dummy='1')
        calculate = raw_data.groupby(["refrigerant_type"]).agg({'filling_volume': 'sum'}).reset_index()
        calculate['filling_volume'] = calculate['filling_volume'].apply(lambda x: round(Decimal(x) / Decimal(1000), 4))
        # 丟掉舊欄位，為了merge時欄位不會重複
        raw_data = raw_data.drop(columns=['filling_volume'])
        a_part = raw_data.merge(calculate, on=['refrigerant_type'], how='left').drop_duplicates()
        # 用dataframe欄位去filter queryset要用'欄位名稱__in'
        coefficient_part = pd.DataFrame(
            list(coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause__in=a_part['device_name']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(coefficient_unit=Value('公噸' + '/公噸', output_field=models.CharField(max_length=50))))).assign(
            dummy='1')
        ab_part = pd.merge(a_part, coefficient_part, on='dummy', how='left').drop(columns='dummy')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['refrigerant_type']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, left_on='refrigerant_type', right_on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['filling_volume']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        final = final.rename(columns={'refrigerant_type': 'fuel_type', 'filling_volume': 'sum_count', 'gas_name_x': 'gas_name'})
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        return final
    except:
        print('沒有該冷氣機設備')
        return final


# 車輛清單
def vehicle_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        # coefficient_source = '環保署溫室氣體排放係數管理表6.0.4'
        # gwp_version = 6
        raw_data = pd.DataFrame(list(vehicle.objects.filter(years=years).filter(company_id=factory_id).values("refrigerant_type", "filling_volume").annotate(
            process_area=Value('逸散', output_field=models.CharField(max_length=50)),
            device_name=Value('車輛', output_field=models.CharField(max_length=50)),
            data_unit=Value('公噸', output_field=models.CharField(max_length=50))))).assign(dummy='1')
        calculate = raw_data.groupby(["refrigerant_type"]).agg({'filling_volume': 'sum'}).reset_index()
        calculate['filling_volume'] = calculate['filling_volume'].apply(lambda x: round(Decimal(x) / Decimal(1000), 4))
        # 丟掉舊欄位，為了merge時欄位不會重複
        raw_data = raw_data.drop(columns=['filling_volume'])
        a_part = raw_data.merge(calculate, on=['refrigerant_type'], how='left').drop_duplicates()
        # 用dataframe欄位去filter queryset要用'欄位名稱__in'
        coefficient_part = pd.DataFrame(
            list(coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause__in=a_part['device_name']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(coefficient_unit=Value('公噸' + '/公噸', output_field=models.CharField(max_length=50))))).assign(
            dummy='1')
        ab_part = pd.merge(a_part, coefficient_part, on='dummy', how='left').drop(columns='dummy')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['refrigerant_type']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, left_on='refrigerant_type', right_on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['filling_volume']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        final = final.rename(columns={'refrigerant_type': 'fuel_type', 'filling_volume': 'sum_count', 'gas_name_x': 'gas_name'})
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        return final
    except:
        print('沒有該車輛設備')
        return final


# 飲水機
def water_dispenser_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        raw_data = pd.DataFrame(
            list(water_dispenser.objects.filter(years=years).filter(company_id=factory_id).values("refrigerant_type", "filling_volume").annotate(process_area=Value('逸散', output_field=models.CharField(max_length=50)), device_name=Value('飲水機', output_field=models.CharField(max_length=50)),
                                                                                                                                                 data_unit=Value('公噸', output_field=models.CharField(max_length=50))))).assign(dummy='1')
        calculate = raw_data.groupby(["refrigerant_type"]).agg({'filling_volume': 'sum'}).reset_index()
        calculate['filling_volume'] = calculate['filling_volume'].apply(lambda x: round(Decimal(x) / Decimal(1000), 4))
        # 丟掉舊欄位，為了merge時欄位不會重複
        raw_data = raw_data.drop(columns=['filling_volume'])
        a_part = raw_data.merge(calculate, on=['refrigerant_type'], how='left').drop_duplicates()
        # 用dataframe欄位去filter queryset要用'欄位名稱__in'
        coefficient_part = pd.DataFrame(
            list(coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause__in=a_part['device_name']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(coefficient_unit=Value('公噸' + '/公噸', output_field=models.CharField(max_length=50))))).assign(
            dummy='1')
        ab_part = pd.merge(a_part, coefficient_part, on='dummy', how='left').drop(columns='dummy')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['refrigerant_type']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, left_on='refrigerant_type', right_on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['filling_volume']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        final = final.rename(columns={'refrigerant_type': 'fuel_type', 'filling_volume': 'sum_count', 'gas_name_x': 'gas_name'})
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        # display(final)
        # display(final.shape)
        return final
    except KeyError:
        print('沒有該設備')
        return final


# 冰水機清單
def ice_water_dispenser_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        raw_data = pd.DataFrame(list(ice_water_dispenser.objects.filter(years=years).filter(company_id=factory_id).values("refrigerant_type", "filling_volume").annotate(
            process_area=Value('逸散', output_field=models.CharField(max_length=50)),
            device_name=Value('冰水機', output_field=models.CharField(max_length=50)),
            data_unit=Value('公噸', output_field=models.CharField(max_length=50))))).assign(dummy='1')
        calculate = raw_data.groupby(["refrigerant_type"]).agg({'filling_volume': 'sum'}).reset_index()
        calculate['filling_volume'] = calculate['filling_volume'].apply(lambda x: round(Decimal(x) / Decimal(1000), 4))
        # 丟掉舊欄位，為了merge時欄位不會重複
        raw_data = raw_data.drop(columns=['filling_volume'])
        a_part = raw_data.merge(calculate, on=['refrigerant_type'], how='left').drop_duplicates()
        # 用dataframe欄位去filter queryset要用'欄位名稱__in'
        coefficient_part = pd.DataFrame(
            list(coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause__in=a_part['device_name']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(coefficient_unit=Value('公噸' + '/公噸', output_field=models.CharField(max_length=50))))).assign(
            dummy='1')
        ab_part = pd.merge(a_part, coefficient_part, on='dummy', how='left').drop(columns='dummy')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['refrigerant_type']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, left_on='refrigerant_type', right_on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['filling_volume']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        final = final.rename(columns={'refrigerant_type': 'fuel_type', 'filling_volume': 'sum_count', 'gas_name_x': 'gas_name'})
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        return final
    except:
        print('沒有該冰水機設備')
        return final


# 製冰機
def ice_maker_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        raw_data = pd.DataFrame(list(ice_maker.objects.filter(years=years).filter(company_id=factory_id).values("refrigerant_type", "filling_volume").annotate(
            process_area=Value('逸散', output_field=models.CharField(max_length=50)),
            device_name=Value('製冰機', output_field=models.CharField(max_length=50)),
            data_unit=Value('公噸', output_field=models.CharField(max_length=50))))).assign(dummy='1')
        calculate = raw_data.groupby(["refrigerant_type"]).agg({'filling_volume': 'sum'}).reset_index()
        calculate['filling_volume'] = calculate['filling_volume'].apply(lambda x: round(Decimal(x) / Decimal(1000), 4))
        # 丟掉舊欄位，為了merge時欄位不會重複
        raw_data = raw_data.drop(columns=['filling_volume'])
        a_part = raw_data.merge(calculate, on=['refrigerant_type'], how='left').drop_duplicates()
        # 用dataframe欄位去filter queryset要用'欄位名稱__in'
        coefficient_part = pd.DataFrame(
            list(coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause__in=a_part['device_name']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(coefficient_unit=Value('公噸' + '/公噸', output_field=models.CharField(max_length=50))))).assign(
            dummy='1')
        ab_part = pd.merge(a_part, coefficient_part, on='dummy', how='left').drop(columns='dummy')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['refrigerant_type']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, left_on='refrigerant_type', right_on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['filling_volume']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        final = final.rename(columns={'refrigerant_type': 'fuel_type', 'filling_volume': 'sum_count', 'gas_name_x': 'gas_name'})
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        # display(final)
        # display(final.shape)
        return final
    except KeyError:
        print('沒有該製冰機設備')
        return final


# 其他設備
def other_device_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        raw_data = pd.DataFrame(
            list(other_device.objects.filter(years=years).filter(company_id=factory_id).values('device_name', "refrigerant_type", "filling_volume").annotate(
                process_area=Value('逸散', output_field=models.CharField(max_length=50)),
                data_unit=Value('公噸', output_field=models.CharField(max_length=50))))).assign(dummy='1')
        calculate = raw_data.groupby(["refrigerant_type"]).agg({'filling_volume': 'sum'}).reset_index()
        calculate['filling_volume'] = calculate['filling_volume'].apply(lambda x: round(Decimal(x) / Decimal(1000), 4))
        # 丟掉舊欄位，為了merge時欄位不會重複
        raw_data = raw_data.drop(columns=['filling_volume'])
        a_part = raw_data.merge(calculate, on=['refrigerant_type'], how='left').drop_duplicates()
        coefficient_part = pd.DataFrame(
            list(coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause='其他設備').values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(coefficient_unit=Value('公噸' + '/公噸', output_field=models.CharField(max_length=50))))).assign(dummy='1')
        ab_part = pd.merge(a_part, coefficient_part, on='dummy', how='left').drop(columns='dummy')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['refrigerant_type']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, left_on='refrigerant_type', right_on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['filling_volume']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        # 102行做merge兩個表都有'gas_name'欄位, 原本的(左邊)被系統改名叫'gas_name_x'
        final = final.rename(columns={'refrigerant_type': 'fuel_type', 'filling_volume': 'sum_count', 'gas_name_x': 'gas_name'})
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        # display(final)
        # display(final.shape)
        return final
    except:
        print('沒有該其他設備設備')
        return final


# 溶劑、噴霧劑
def solvent_aerosol_emission_sources_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        raw_part = pd.DataFrame(list(solvent_aerosol_emission_sources.objects.filter(years=years).filter(company_id=factory_id).values('solvent_name', 'solvent_amount', 'solvent_capacity', 'solvent_capacity_unit', 'gas_name', 'gas_ratio', 'density').annotate(
            process_area=Value('逸散', output_field=models.CharField(max_length=50)),
            device_name=Value('溶劑、噴霧劑', output_field=models.CharField(max_length=50)),
            data_unit=Value('公噸', output_field=models.CharField(max_length=50))))
        )
        # 溶劑名稱、添加物名稱相同的，將數量做總和
        a_part = raw_part.groupby(["solvent_name", "solvent_capacity", "solvent_capacity_unit", "gas_name", "gas_ratio", "density", ]).agg({'solvent_amount': 'sum', 'process_area': 'first', 'device_name': 'first', 'data_unit': 'first'}).reset_index()

        # display(a_part)

        # 根據溶劑單位不同判斷相乘係數(oz要*28.3495231換算成g)
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
        # display(a_part)
        a_part = a_part.drop(columns=['solvent_capacity_unit', 'solvent_capacity', 'gas_ratio', 'density']).drop_duplicates()
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source='質量平衡法').filter(cause__in=a_part['device_name']).filter(gas_name__in=a_part['gas_name']).values('gas_name', 'coefficient', 'coefficient_source').annotate(
            coefficient_unit=Value('公噸' + '/公噸', output_field=models.CharField(max_length=50)))))
        ab_part = pd.merge(a_part, coefficient_part, left_on='gas_name', right_on='gas_name', how='left')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['solvent_amount']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        final = final.rename(columns={'solvent_name': 'fuel_type', 'solvent_amount': 'sum_count'})
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        # display(final)
        # display(final.shape)
        return final
    except:
        print('沒有該溶劑、噴霧劑設備')
        return final


# 人天清冊
def personnel_inventory_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        employee_raw_data = pd.DataFrame(list(personnel_inventory.objects.filter(years=years).filter(company_id=factory_id).filter(classification='員工').values('did').annotate(
            process_area=Value('逸散', output_field=models.CharField(max_length=50)),
            device_name=Value('人天清冊', output_field=CharField(max_length=20)),
            fuel_type=Value('水肥', output_field=CharField(max_length=20)),
            data_unit=Value('年/時', output_field=models.CharField(max_length=50)),
            total_usage=Sum(F('WKhours_january') + F('WKhours_february') + F('WKhours_march') + F('WKhours_april') + F('WKhours_may') + F('WKhours_june') + F('WKhours_july') + F('WKhours_august') + F('WKhours_september') + F('WKhours_october') + F('WKhours_november') + F('WKhours_december')),
        )))
        employee_raw_data = employee_raw_data.drop(columns=['did'])
        # 員工宿舍dataframe
        dormitory_raw_data = pd.DataFrame(list(personnel_inventory.objects.filter(years=years).filter(company_id=factory_id).filter(classification='員工宿舍').values(
            'WKhours_january', 'WKhours_february', 'WKhours_march', 'WKhours_april', 'WKhours_may', 'WKhours_june', 'WKhours_july', 'WKhours_august', 'WKhours_september', 'WKhours_october', 'WKhours_november', 'WKhours_december',
            'WKnum_january', 'WKnum_february', 'WKnum_march', 'WKnum_april', 'WKnum_may', 'WKnum_june', 'WKnum_july', 'WKnum_august', 'WKnum_september', 'WKnum_october', 'WKnum_november', 'WKnum_december').annotate(
            process_area=Value('逸散', output_field=models.CharField(max_length=50)),
            device_name=Value('人天清冊', output_field=CharField(max_length=20)),
            fuel_type=Value('水肥', output_field=CharField(max_length=20)),
        )))

        def dormitory_count(row):
            row['dormitory_total_usage'] = \
                ((Decimal(str(row['WKnum_january'])) * Decimal('31') * Decimal('24')) - Decimal(str(row['WKhours_january']))) + \
                ((Decimal(str(row['WKnum_february'])) * Decimal('28') * Decimal('24')) - Decimal(str(row['WKhours_february']))) + \
                ((Decimal(str(row['WKnum_march'])) * Decimal('31') * Decimal('24')) - Decimal(str(row['WKhours_march']))) + \
                ((Decimal(str(row['WKnum_april'])) * Decimal('30') * Decimal('24')) - Decimal(str(row['WKhours_april']))) + \
                ((Decimal(str(row['WKnum_may'])) * Decimal('31') * Decimal('24')) - Decimal(str(row['WKhours_may']))) + \
                ((Decimal(str(row['WKnum_june'])) * Decimal('30') * Decimal('24')) - Decimal(str(row['WKhours_june']))) + \
                ((Decimal(str(row['WKnum_july'])) * Decimal('31') * Decimal('24')) - Decimal(str(row['WKhours_july']))) + \
                ((Decimal(str(row['WKnum_august'])) * Decimal('31') * Decimal('24')) - Decimal(str(row['WKhours_august']))) + \
                ((Decimal(str(row['WKnum_september'])) * Decimal('30') * Decimal('24')) - Decimal(str(row['WKhours_september']))) + \
                ((Decimal(str(row['WKnum_october'])) * Decimal('31') * Decimal('24')) - Decimal(str(row['WKhours_october']))) + \
                ((Decimal(str(row['WKnum_november'])) * Decimal('30') * Decimal('24')) - Decimal(str(row['WKhours_november']))) + \
                ((Decimal(str(row['WKnum_december'])) * Decimal('31') * Decimal('24')) - Decimal(str(row['WKhours_december'])))
            return row['dormitory_total_usage']

        if not dormitory_raw_data.empty:
            dormitory_raw_data['dormitory_total_usage'] = dormitory_raw_data.apply(dormitory_count, axis=1)
            dormitory_raw_data = dormitory_raw_data.drop(columns=['WKhours_january', 'WKhours_february', 'WKhours_march', 'WKhours_april', 'WKhours_may', 'WKhours_june', 'WKhours_july', 'WKhours_august', 'WKhours_september', 'WKhours_october', 'WKhours_november', 'WKhours_december',
                                                                  'WKnum_january', 'WKnum_february', 'WKnum_march', 'WKnum_april', 'WKnum_may', 'WKnum_june', 'WKnum_july', 'WKnum_august', 'WKnum_september', 'WKnum_october', 'WKnum_november', 'WKnum_december'])
            # 宿舍總人天
            dormitory_raw_data = dormitory_raw_data.groupby(["process_area", "device_name", "fuel_type"]).agg({'dormitory_total_usage': 'sum'}).reset_index()
            employee_raw_data['total_usage'] = employee_raw_data['total_usage'] + dormitory_raw_data['dormitory_total_usage']
        a_part = employee_raw_data
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause__in=a_part['fuel_type']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(
            coefficient_unit=Value('公噸' + '/人時', output_field=models.CharField(max_length=50)))))
        ab_part = pd.merge(a_part, coefficient_part, left_on='fuel_type', right_on='cause', how='left')
        ab_part = ab_part.drop(columns=['cause'])
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['total_usage']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        final = final.rename(columns={'total_usage': 'sum_count'})
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        # display(final)
        # display(final.shape)
        return final
    except:
        print('沒有該人天清冊設備')
        return final


# 委外人員
def employee_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        raw_data = pd.DataFrame(list(employee.objects.filter(years=years).filter(company_id=factory_id).values('career').annotate(
            process_area=Value('逸散', output_field=models.CharField(max_length=50)),
            device_name=Value('委外人員清冊', output_field=CharField(max_length=20)),
            fuel_type=Value('水肥', output_field=CharField(max_length=20)),
            data_unit=Value('年/時 ', output_field=models.CharField(max_length=50)),
            total_employeeNum=Sum(
                F('employeeNum_january') + F('employeeNum_february') + F('employeeNum_march') + F('employeeNum_april') + F('employeeNum_may') + F('employeeNum_june') + F('employeeNum_july') + F('employeeNum_august') + F('employeeNum_september') + F('employeeNum_october') + F('employeeNum_november') + F(
                    'employeeNum_december')),
            total_WKdays=Sum(F('WKdays_january') + F('WKdays_february') + F('WKdays_march') + F('WKdays_april') + F('WKdays_may') + F('WKdays_june') + F('WKdays_july') + F('WKdays_august') + F('WKdays_september') + F('WKdays_october') + F('WKdays_november') + F('WKdays_december')),
            total_WKhours=Sum(F('WKhours_january') + F('WKhours_february') + F('WKhours_march') + F('WKhours_april') + F('WKhours_may') + F('WKhours_june') + F('WKhours_july') + F('WKhours_august') + F('WKhours_september') + F('WKhours_october') + F('WKhours_november') + F('WKhours_december')),
            sum_count=Sum(
                F('employeeNum_january') * F('WKdays_january') * F('WKhours_january') +
                F('employeeNum_february') * F('WKdays_february') * F('WKhours_february') +
                F('employeeNum_march') * F('WKdays_march') * F('WKhours_march') +
                F('employeeNum_april') * F('WKdays_april') * F('WKhours_april') +
                F('employeeNum_may') * F('WKdays_may') * F('WKhours_may') +
                F('employeeNum_june') * F('WKdays_june') * F('WKhours_june') +
                F('employeeNum_july') * F('WKdays_july') * F('WKhours_july') +
                F('employeeNum_august') * F('WKdays_august') * F('WKhours_august') +
                F('employeeNum_september') * F('WKdays_september') * F('WKhours_september') +
                F('employeeNum_october') * F('WKdays_october') * F('WKhours_october') +
                F('employeeNum_november') * F('WKdays_november') * F('WKhours_november') +
                F('employeeNum_december') * F('WKdays_december') * F('WKhours_december')),
        )))
        a_part = raw_data
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause__in=a_part['fuel_type']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(
            coefficient_unit=Value('公噸' + '/公噸', output_field=models.CharField(max_length=50)))))
        ab_part = pd.merge(a_part, coefficient_part, left_on='fuel_type', right_on='cause', how='left')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        return final
    except:
        print('沒有該委外人員設備')
        return final


# 滅火器
def extinguisher_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        # years = 2023
        # factory_id = 1
        # coefficient_source = '環保署溫室氣體排放係數管理表6.0.4'
        # gwp_version = 6
        raw_data = pd.DataFrame(list(extinguisher.objects.filter(years=years).filter(company_id=factory_id).values('extinguisher_type').annotate(
            process_area=Value('逸散', output_field=models.CharField(max_length=50)),
            device_name=Value('滅火器', output_field=models.CharField(max_length=50)),
            sum_count=Cast(Sum(F('chemical_weight') * F('inventory')) / 1000, output_field=models.DecimalField(max_digits=20, decimal_places=4)),
            data_unit=Value('公噸', output_field=models.CharField(max_length=50))))
        )
        a_part = raw_data

        def extinguisher_gas(row):
            if row['extinguisher_type'] == '二氧化碳滅火器':
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
        raw_data = pd.DataFrame(list(waste_water.objects.filter(years=years).filter(company_id=factory_id).values('did').annotate(
            process_area=Value('逸散', output_field=models.CharField(max_length=50)),
            device_name=Value('厭氧廢水處理', output_field=models.CharField(max_length=50)),
            fuel_type=Value('厭氧處理', output_field=models.CharField(max_length=50)),
            sum_count=Cast(Sum(F('Pi') * F('Wi') * F('CODi') - F('Si')) * (F('Bo') * F('MCFj') - F('Ri')), output_field=models.DecimalField(max_digits=20, decimal_places=4)),
            data_unit=Value('公噸', output_field=models.CharField(max_length=50))))).assign(dummy='1')
        a_part = raw_data
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause__in=a_part['fuel_type']).values('gas_name', 'coefficient', 'coefficient_source').annotate(
            coefficient_unit=Value('公噸' + '/公噸', output_field=models.CharField(max_length=50))))).assign(dummy='1')
        ab_part = pd.merge(a_part, coefficient_part, on='dummy', how='left').drop(columns=['dummy', 'did'])
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
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source='110年度電力排碳係數').filter(cause__in=a_part['fuel_type']).values('gas_name', 'coefficient', 'coefficient_source').annotate(
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
# def upstream_transport_count(years, factory_id, coefficient_source, gwp_version):
#     final = pd.DataFrame()
#     try:
# gwp_version = 6
# transport_raw_data = pd.DataFrame(list(upstream_transportation.objects.filter(customer='國內').filter(paid='公司支付').values('commodity_NW', 'transport_type', 'transport_fuel', 'transport_distance', 'trips').annotate(
#     process_area=Value('上游運輸產生之排放', output_field=models.CharField(max_length=50)),
#     device_name=Value('陸運運輸', output_field=models.CharField(max_length=50)),
#     sum_count=Cast(Sum(F('commodity_NW') * F('transport_distance') * F('trips')), output_field=models.DecimalField(max_digits=20, decimal_places=4)),
#     data_unit=Value('延噸公里', output_field=models.CharField(max_length=50)))))
# transport_raw_data['fuel_type'] = transport_raw_data.apply(lambda x: f"{x['transport_type']}({x['transport_fuel']})", axis=1)
# transport_raw_data = transport_raw_data.groupby(['transport_type', 'transport_fuel']).agg({'process_area': 'first', 'device_name': 'first', 'fuel_type': 'first', 'sum_count': 'sum', 'data_unit': 'first'}).reset_index()
# a_part = transport_raw_data
# print(a_part)
# coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source='產品碳足跡資訊網').filter(cause__in=a_part['transport_type']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(
#             coefficient_unit=Value('公噸' + '/延噸公里', output_field=models.CharField(max_length=50)))))
# ab_part = pd.merge(a_part, coefficient_part, left_on='transport_type', right_on='cause', how='left')
# gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['gas_name']).values('gas_name', 'gwp_coefficient')))
# final = pd.merge(ab_part, gwp, on='gas_name', how='left')
# final['emission'] = final.apply(lambda x: round(Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
# new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
# final = final.reindex(columns=new_order)
# print(final)
# #
# overseas_raw_data = pd.DataFrame(list(upstream_transportation.objects.values('commodity_NW', 'overseas_transport_distance', 'overseas_trips').annotate(
#     process_area=Value('上游運輸產生之排放', output_field=models.CharField(max_length=50)),
#     fuel_type=Value('海運運輸', output_field=models.CharField(max_length=50)),
#     data_unit=Value('延噸公里', output_field=models.CharField(max_length=50)))))
# overseas_raw_data = overseas_raw_data.fillna(0)
# overseas_raw_data['sum_count'] = overseas_raw_data.apply(lambda x: round(Decimal(x['commodity_NW']) * Decimal(x['overseas_transport_distance']) * Decimal(x['overseas_trips']), 4), axis=1)
# print(overseas_raw_data)


# 員工通勤 (第三類)
def employee_commute_count(years, factory_id, coefficient_source, gwp_version):
    final = pd.DataFrame()
    try:
        raw_data = pd.DataFrame(list(employee_commute.objects.filter(years=years).filter(company_id=factory_id).values('id', 'commute_distance', 'work_days').annotate(
            process_area=Value('員工通勤產生之排放', output_field=models.CharField(max_length=50)),
            fuel_type=Value('汽油', output_field=CharField(max_length=20)),
            data_unit=Value('延人公里', output_field=models.CharField(max_length=50)))))
        transportation_data = pd.DataFrame(list(transportation_way.objects.values('transportation', 'commute_id')))
        a_part = pd.merge(raw_data, transportation_data, left_on='id', right_on='commute_id', how='left')
        a_part['sum_count'] = a_part.apply(lambda x: round(Decimal(x['commute_distance']) * Decimal(x['work_days']) * Decimal('2'), 4), axis=1)

        def transportations(row):
            if row['transportation'] == '自駕汽車':
                return '自用小客車(汽油)'
            elif row['transportation'] == '高鐵':
                return '高速鐵路運輸服務'
            elif row['transportation'] == '火車(電聯)':
                return '臺灣鐵路運輸服務(電聯車)'
            elif row['transportation'] == '火車(柴聯)':
                return '臺灣鐵路運輸服務(柴聯車)'
            elif row['transportation'] == '計程車':
                return '營業小客車(汽油)'
            elif row['transportation'] == '高鐵':
                return '高速鐵路運輸服務'
            elif row['transportation'] == '機車':
                return '機器腳踏車(汽油)'
            elif row['transportation'] == '捷運':
                return '捷運'
            elif row['transportation'] == '飛機':
                return '飛機'
            elif row['transportation'] == '船舶':
                return '船舶'
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
            if row['transportation'] == '自駕汽車':
                return '自用小客車(汽油)'
            elif row['transportation'] == '高鐵':
                return '高速鐵路運輸服務'
            elif row['transportation'] == '火車(電聯)':
                return '臺灣鐵路運輸服務(電聯車)'
            elif row['transportation'] == '火車(柴聯)':
                return '臺灣鐵路運輸服務(柴聯車)'
            elif row['transportation'] == '計程車':
                return '營業小客車(汽油)'
            elif row['transportation'] == '高鐵':
                return '高速鐵路運輸服務'
            elif row['transportation'] == '機車':
                return '機器腳踏車(汽油)'
            elif row['transportation'] == '捷運':
                return '捷運'
            elif row['transportation'] == '飛機':
                return '飛機'
            elif row['transportation'] == '船舶':
                return '船舶'
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
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source='產品碳足跡資訊網').filter(cause__in=a_part['transport_type']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(
            coefficient_unit=Value('公噸' + '/延噸公里', output_field=models.CharField(max_length=50)))))
        ab_part = pd.merge(a_part, coefficient_part, left_on='transport_type', right_on='cause', how='left')
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
        raw_data = pd.DataFrame(list(waste.objects.filter(years=years).filter(company_id=factory_id).values('waste_disposal', 'waste_name', 'waste_weigh').annotate(
            process_area=Value('公司營運所產生廢棄物處置', output_field=models.CharField(max_length=50)),
            data_unit=Value('公噸', output_field=models.CharField(max_length=50)))))
        raw_data = raw_data.groupby(['waste_disposal']).agg({'waste_name': 'first', 'waste_weigh': 'sum', 'process_area': 'first', 'data_unit': 'first'}).reset_index()
        a_part = raw_data.rename(columns={'waste_weigh': 'sum_count'})
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source='產品碳足跡資訊網').filter(cause__in=a_part['waste_disposal']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(
            coefficient_unit=Value('公噸' + '/延噸公里', output_field=models.CharField(max_length=50)))))
        ab_part = pd.merge(a_part, coefficient_part, left_on='waste_disposal', right_on='cause', how='left')
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
