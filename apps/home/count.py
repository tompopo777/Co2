from urllib import request, parse
import pandas as pd
from IPython.core.display import display
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Value, CharField
from django.db.models.functions import Cast
from decimal import *
from django.http import HttpResponse
from .models import *

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
        company_id = request.session.get('company_dropdown')
        years = request.session.get('years')

        company_dic = {
            2: '雲科A廠',
            3: '雲科B廠',
        }
        if company_id in company_dic:
            company_name = company_dic[company_id]
        else:
            company_name = ''

        emergency_generators_device = emergency_generators_count(years, company_id, coefficient_source, gwp_version)
        combustion_equipment_device = combustion_equipment_count(years, company_id, coefficient_source, gwp_version)
        official_car_device = official_car_count(years, company_id, coefficient_source, gwp_version)
        water_dispenser_device = water_dispenser_count(years, company_id, coefficient_source, gwp_version)
        ice_maker_device = ice_maker_count(years, company_id, coefficient_source, gwp_version)
        other_device_device = other_device_count(years, company_id, coefficient_source, gwp_version)
        solvent_aerosol_emission_sources_device = solvent_aerosol_emission_sources_count(years, company_id, coefficient_source, gwp_version)
        personnel_inventory_device = personnel_inventory_count(years, company_id, coefficient_source, gwp_version)
        # extinguisher_device = extinguisher_count(years, company_id, coefficient_source, gwp_version)
        output = pd.concat([emergency_generators_device, combustion_equipment_device, official_car_device, water_dispenser_device, ice_maker_device, other_device_device, solvent_aerosol_emission_sources_device, personnel_inventory_device])
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
        # return None


# 發電機
def emergency_generators_count(years, company_id, coefficient_source, gwp_version):
    try:
        raw_data = emergency_generators.objects.filter(years=years).filter(company_id=company_id).values('did').annotate(
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
        pass


# 燃燒設備
def combustion_equipment_count(years, company_id, coefficient_source, gwp_version):
    try:
        raw_data = combustion_equipment.objects.filter(years=years).filter(company_id=company_id).values('device_name', 'fuel_type').annotate(
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
        pass


# 公務車
def official_car_count(years, company_id, coefficient_source, gwp_version):
    try:
        raw_data = official_car.objects.filter(years=years).filter(company_id=company_id).values('vehicle_type', 'fuel_type').annotate(
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
        pass


# 逸散(冰箱~其他設備)
# coefficient_source = '環保署溫室氣體排放係數管理表6.0.4'
# gwp_version = 6
# refrigerator = pd.DataFrame(list(refrigerator.objects.values("device_name", "refrigerant_type", "filling_volume")))
# airconditioner = pd.DataFrame(list(airconditioner.objects.values("device_name", "refrigerant_type", "filling_volume")))
# vehicle = pd.DataFrame(list(vehicle.objects.values("device_name", "refrigerant_type", "filling_volume")))
# ice_maker = pd.DataFrame(list(ice_maker.objects.values("device_name", "refrigerant_type", "filling_volume")))


# 製冰機
def ice_maker_count(years, company_id, coefficient_source, gwp_version):
    try:
        raw_data = pd.DataFrame(
            list(ice_maker.objects.filter(years=years).filter(company_id=company_id).values("refrigerant_type", "filling_volume").annotate(process_area=Value('逸散', output_field=models.CharField(max_length=50)), device_name=Value('製冰機', output_field=models.CharField(max_length=50)),
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
        pass


# 飲水機
def water_dispenser_count(years, company_id, coefficient_source, gwp_version):
    try:
        raw_data = pd.DataFrame(
            list(water_dispenser.objects.filter(years=years).filter(company_id=company_id).values("refrigerant_type", "filling_volume").annotate(process_area=Value('逸散', output_field=models.CharField(max_length=50)), device_name=Value('飲水機', output_field=models.CharField(max_length=50)),
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
        pass


# 冷氣機
def airconditioner_count(years, company_id, coefficient_source, gwp_version):
    try:
        raw_data = pd.DataFrame(
            list(airconditioner.objects.filter(years=years).filter(company_id=company_id).values("refrigerant_type", "filling_volume").annotate(process_area=Value('逸散', output_field=models.CharField(max_length=50)), device_name=Value('冷氣機', output_field=models.CharField(max_length=50)),
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
        display(final)
        display(final.shape)
    except:
        print('沒有該冷氣機設備')
        pass


# 其他設備
def other_device_count(years, company_id, coefficient_source, gwp_version):
    try:
        raw_data = pd.DataFrame(
            list(other_device.objects.filter(years=years).filter(company_id=company_id).values('device_name', "refrigerant_type", "filling_volume").annotate(process_area=Value('逸散', output_field=models.CharField(max_length=50)),
                                                                                                                                                             data_unit=Value('公噸', output_field=models.CharField(max_length=50))))).assign(
            dummy='1')
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
        pass


# 溶劑、噴霧劑
def solvent_aerosol_emission_sources_count(years, company_id, coefficient_source, gwp_version):
    try:
        raw_part = pd.DataFrame(list(solvent_aerosol_emission_sources.objects.filter(years=years).filter(company_id=company_id).values('solvent_name', 'solvent_amount', 'solvent_capacity', 'solvent_capacity_unit', 'gas_name', 'gas_ratio', 'density').annotate(
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
        pass


# 人天清冊
def personnel_inventory_count(years, company_id, coefficient_source, gwp_version):
    try:
        employee_raw_data = pd.DataFrame(list(personnel_inventory.objects.filter(years=years).filter(company_id=company_id).filter(classification='員工').values('did').annotate(
            process_area=Value('逸散', output_field=models.CharField(max_length=50)),
            device_name=Value('人天清冊', output_field=CharField(max_length=20)),
            fuel_type=Value('水肥', output_field=CharField(max_length=20)),
            data_unit=Value('時/人', output_field=models.CharField(max_length=50)),
            total_usage=Sum(F('WKhours_january') + F('WKhours_february') + F('WKhours_march') + F('WKhours_april') + F('WKhours_may') + F('WKhours_june') + F('WKhours_july') + F('WKhours_august') + F('WKhours_september') + F('WKhours_october') + F('WKhours_november') + F('WKhours_december')),
        )))
        employee_raw_data = employee_raw_data.drop(columns=['did'])
        # 員工宿舍dataframe
        dormitory_raw_data = pd.DataFrame(list(personnel_inventory.objects.filter(years=years).filter(company_id=company_id).filter(classification='員工宿舍').values(
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
        pass


# 滅火器
# def extinguisher_count(years, company_id, coefficient_source, gwp_version):
#     try:
# coefficient_source = "質量平衡法"
# gwp_version = 6
# raw_data = pd.DataFrame(list(extinguisher.objects.values("extinguisher_type").annotate(
#     process_area=Value('逸散', output_field=models.CharField(max_length=50)),
#     device_name=Value('滅火器', output_field=models.CharField(max_length=50)),
#     sum_count=Cast(Sum(F('chemical_weight')*F('inventory')) / 1000, output_field=models.DecimalField(max_digits=20, decimal_places=4)),
#     data_unit=Value('公噸', output_field=models.CharField(max_length=50))))
# )
# print(raw_data)
# a_part = raw_data
# print(a_part)
# coefficient_part = None
# for query in raw_data:
#     fuel_type = query['extinguisher_type']
#     coefficient_data = coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause=fuel_type).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(coefficient_unit=Value('公噸' + '/公秉', output_field=models.CharField(max_length=50)))
#     coefficient_part = pd.DataFrame(list(coefficient_data))
# gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=coefficient_part['gas_name']).values('gas_name', 'gwp_coefficient')))
# raw_data = pd.DataFrame(list(raw_data))
# a_b_part = pd.merge(raw_data, coefficient_part, left_on='fuel_type', right_on='cause', how='left')
# final = pd.merge(a_b_part, gwp, left_on='gas_name', right_on='gas_name', how='left')
# final['emission'] = final.apply(lambda x: (Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient'])).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP), axis=1)
# new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
# final = final.reindex(columns=new_order)
    # except:
    #     print('沒有該滅火器設備')
    #     pass
#
# # 原物料
# material = pd.DataFrame(list(material.objects.values('material_name').annotate(
#     sum_count=Cast(Sum(F('january') + F('february') + F('march') + F('april') + F('may') + F('june') +
#                        F('july') + F('august') + F('september') + F('october') + F('november') + F('december')), output_field=models.DecimalField(max_digits=20, decimal_places=4))
# )))
# display(material.to_string(index=False))
#
# # 新增 material_type 欄位，提取 material_name 中的中文字，並將其相同的類型歸為一類
# material['material_type'] = material['material_name'].apply(lambda x: re.findall('[\u4e00-\u9fa5]+', x)[0])
#
# # 以 material_type 為分組依據，計算 sum_count 的加總
# total_sum_count_by_type = material.groupby('material_type')['sum_count'].sum()
#
# # 印出加總結果
# print('相同中文字的 sum_count 欄位加總結果為:', total_sum_count_by_type)
