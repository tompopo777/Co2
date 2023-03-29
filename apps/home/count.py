import pandas as pd
from IPython.core.display import display
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Value, CharField
from django.db.models.functions import Cast
from decimal import *
from .models import *
import re

pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.width', 200)

getcontext().prec = 4


# 發電機
@login_required(login_url="/login/")
def emergency_generators(coefficient_source, gwp_version):
    try:
        coefficient_source = '環保署溫室氣體排放係數管理表6.0.4'
        gwp_version = 6
        generators = emergency_generators.objects.values('did').annotate(
            process_area=Value('固定式燃燒', output_field=models.CharField(max_length=50)),
            device_name=Value('柴油發電機', output_field=CharField(max_length=20)),
            fuel_type=Value('柴油', output_field=CharField(max_length=20)),
            sum_count=Cast(Sum(F('january') + F('february') + F('march') + F('april') + F('may') + F('june') +
                               F('july') + F('august') + F('september') + F('october') + F('november') + F('december')) / 1000,
                           output_field=models.DecimalField(max_digits=20, decimal_places=4)),
            data_unit=Value('公秉', output_field=models.CharField(max_length=50))
        )
        coefficient_part = None
        for query in generators:
            fuel_type = query['fuel_type']
            coefficient_data = coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause=fuel_type).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(coefficient_unit=Value('公噸' + '/公秉', output_field=models.CharField(max_length=50)))
            coefficient_part = pd.DataFrame(list(coefficient_data))
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=coefficient_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        generators = pd.DataFrame(list(generators))
        a_b_part = pd.merge(generators, coefficient_part, left_on='fuel_type', right_on='cause', how='left')
        final = pd.merge(a_b_part, gwp, left_on='gas_name', right_on='gas_name', how='left')
        # 將(A)、(B)、(C)轉為float才能取round
        final['emission'] = final.apply(lambda x: float(x['sum_count']) * float(x['coefficient']) * float(x['gwp_coefficient']), axis=1)
        final['emission'] = final['emission'].round(4)
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        display(final)
        display(final.shape)
    except KeyError:
        print('沒有該設備')
        pass


# 燃燒設備
@login_required(login_url="/login/")
def combustion_equipment(coefficient_source, gwp_version):
    try:
        coefficient_source = '環保署溫室氣體排放係數管理表6.0.4'
        gwp_version = 6
        combustion = combustion_equipment.objects.values('device_name', 'fuel_type').annotate(
            process_area=Value('固定式燃燒', output_field=models.CharField(max_length=50)),
            sum_count=Cast(Sum(F('fuel_january') + F('fuel_february') + F('fuel_march') + F('fuel_april') + F('fuel_may') + F('fuel_june') + F('fuel_july') + F('fuel_august') + F('fuel_september') + F('fuel_october') + F('fuel_november') + F('fuel_december')) * 1.818 / 1000,
                           output_field=models.DecimalField(max_digits=20, decimal_places=4)),
            data_unit=Value('公秉', output_field=models.CharField(max_length=50))
        ).order_by('device_name', 'fuel_type')
        coefficient_part = None
        for query in combustion:
            fuel_type = query['fuel_type']
            coefficient_data = coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause=fuel_type).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(coefficient_unit=Value('公噸' + '/公秉', output_field=models.CharField(max_length=50)))
            coefficient_part = pd.DataFrame(list(coefficient_data))
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=coefficient_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        combustion = pd.DataFrame(list(combustion))
        a_b_part = pd.merge(combustion, coefficient_part, left_on='fuel_type', right_on='cause', how='left')
        final = pd.merge(a_b_part, gwp, left_on='gas_name', right_on='gas_name', how='left')
        display(final['sum_count'])
        display(final['coefficient'])
        display(final['gwp_coefficient'])
        # final['sum_count'] = final['sum_count'].apply(lambda x: Decimal(str(x)))
        # final['coefficient'] = final['coefficient'].apply(lambda x: Decimal(str(x)))
        # final['gwp_coefficient'] = final['gwp_coefficient'].apply(lambda x: Decimal(str(x)))
        # 將(A)、(B)、(C)轉為float才能取round
        # final['emission'] = final.apply(lambda x: round(Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        # final['emission'] = final.apply(lambda x: (Decimal(x['sum_count']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient'])).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP), axis=1)
        final['emission'] = final.apply(lambda x: round(float(x['sum_count']) * float(x['coefficient']) * float(x['gwp_coefficient']), 4), axis=1)
        display(final['emission'])
        new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        display(final)
        display(final.shape)
    except KeyError:
        print('沒有該設備')
        pass
# 公務車
@login_required(login_url="/login/")
def official_car(coefficient_source, gwp_version):
    try:
        coefficient_source = '環保署溫室氣體排放係數管理表6.0.4'
        gwp_version = 6
        officialCar = official_car.objects.values('vehicle_type', 'fuel_type').annotate(
            process_area=Value('移動式式燃燒', output_field=models.CharField(max_length=50)),
            sum_count=Cast(Sum(F('january') + F('february') + F('march') + F('april') + F('may') + F('june') +
                               F('july') + F('august') + F('september') + F('october') + F('november') + F('december')) / 1000,
                           output_field=models.DecimalField(max_digits=20, decimal_places=4)),
            data_unit=Value('公秉', output_field=models.CharField(max_length=50))
        ).order_by('vehicle_type', 'fuel_type')
        coefficient_part = None
        for query in officialCar:
            fuel_type = query['fuel_type']
            coefficient_data = coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause=fuel_type).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(coefficient_unit=Value('公噸' + '/公秉', output_field=models.CharField(max_length=50)))
            coefficient_part = pd.DataFrame(list(coefficient_data))
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=coefficient_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        officialCar = pd.DataFrame(list(officialCar))
        a_b_part = pd.merge(officialCar, coefficient_part, left_on='fuel_type', right_on='cause', how='left')
        final = pd.merge(a_b_part, gwp, left_on='gas_name', right_on='gas_name', how='left')
        # 將(A)、(B)、(C)轉為float才能取round
        final['emission'] = final.apply(lambda x: float(x['sum_count']) * float(x['coefficient']) * float(x['gwp_coefficient']), axis=1)
        final['emission'] = final['emission'].round(4)
        new_order = ['process_area', 'vehicle_type', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        display(final)
        display(final.shape)
    except KeyError:
        print('沒有該設備')
        pass

# 逸散(冰箱~其他設備)
# coefficient_source = '環保署溫室氣體排放係數管理表6.0.4'
# gwp_version = 6
# refrigerator = pd.DataFrame(list(refrigerator.objects.values("device_name", "refrigerant_type", "filling_volume")))
# airconditioner = pd.DataFrame(list(airconditioner.objects.values("device_name", "refrigerant_type", "filling_volume")))
# vehicle = pd.DataFrame(list(vehicle.objects.values("device_name", "refrigerant_type", "filling_volume")))
# ice_maker = pd.DataFrame(list(ice_maker.objects.values("device_name", "refrigerant_type", "filling_volume")))
#

# 製冰機
@login_required(login_url="/login/")
def water_dispenser_count(coefficient_source, gwp_version):
    try:
        raw_data = pd.DataFrame(list(ice_maker.objects.values("refrigerant_type", "filling_volume").annotate(process_area=Value('逸散', output_field=models.CharField(max_length=50)), device_name=Value('製冰機', output_field=models.CharField(max_length=50)), data_unit=Value('公噸', output_field=models.CharField(max_length=50))))).assign(dummy='1')

        calculate = raw_data.groupby(["refrigerant_type"]).agg({'filling_volume': 'sum'}).reset_index()
        calculate['filling_volume'] = calculate['filling_volume'].apply(lambda x: round(Decimal(x) / Decimal(1000), 4))
        # 丟掉舊欄位，為了merge時欄位不會重複
        raw_data = raw_data.drop(columns=['filling_volume'])
        a_part = raw_data.merge(calculate, on=['refrigerant_type'], how='left').drop_duplicates()
        # 用dataframe欄位去filter queryset要用'欄位名稱__in'
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause__in=a_part['device_name']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(coefficient_unit=Value('公噸' + '/公噸', output_field=models.CharField(max_length=50))))).assign(dummy='1')
        ab_part = pd.merge(a_part, coefficient_part, on='dummy', how='left').drop(columns='dummy')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['refrigerant_type']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, left_on='refrigerant_type', right_on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['filling_volume']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        new_order = ['process_area', 'device_name', 'refrigerant_type', 'filling_volume', 'data_unit', 'emission', 'gas_name_x', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        display(final)
        display(final.shape)
    except KeyError:
        print('沒有該設備')
        pass

# 飲水機
@login_required(login_url="/login/")
def water_dispenser_count(coefficient_source, gwp_version):
    try:
        raw_data = pd.DataFrame(list(water_dispenser.objects.values("refrigerant_type", "filling_volume").annotate(process_area=Value('逸散', output_field=models.CharField(max_length=50)), device_name=Value('飲水機', output_field=models.CharField(max_length=50)), data_unit=Value('公噸', output_field=models.CharField(max_length=50))))).assign(dummy='1')
        calculate = raw_data.groupby(["refrigerant_type"]).agg({'filling_volume': 'sum'}).reset_index()
        calculate['filling_volume'] = calculate['filling_volume'].apply(lambda x: round(Decimal(x) / Decimal(1000), 4))
        # 丟掉舊欄位，為了merge時欄位不會重複
        raw_data = raw_data.drop(columns=['filling_volume'])
        a_part = raw_data.merge(calculate, on=['refrigerant_type'], how='left').drop_duplicates()
        # 用dataframe欄位去filter queryset要用'欄位名稱__in'
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause__in=a_part['device_name']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(coefficient_unit=Value('公噸' + '/公噸', output_field=models.CharField(max_length=50))))).assign(dummy='1')
        ab_part = pd.merge(a_part, coefficient_part, on='dummy', how='left').drop(columns='dummy')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['refrigerant_type']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, left_on='refrigerant_type', right_on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['filling_volume']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        new_order = ['process_area', 'device_name', 'refrigerant_type', 'filling_volume', 'data_unit', 'emission', 'gas_name_x', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        display(final)
        display(final.shape)
    except KeyError:
            print('沒有該設備')
            pass

# 冷氣機
@login_required(login_url="/login/")
def airconditioner_count(coefficient_source, gwp_version):
    try:
        raw_data = pd.DataFrame(list(airconditioner.objects.values("refrigerant_type", "filling_volume").annotate(process_area=Value('逸散', output_field=models.CharField(max_length=50)), device_name=Value('冷氣機', output_field=models.CharField(max_length=50)), data_unit=Value('公噸', output_field=models.CharField(max_length=50))))).assign(dummy='1')
        calculate = raw_data.groupby(["refrigerant_type"]).agg({'filling_volume': 'sum'}).reset_index()
        calculate['filling_volume'] = calculate['filling_volume'].apply(lambda x: round(Decimal(x) / Decimal(1000), 4))
        # 丟掉舊欄位，為了merge時欄位不會重複
        raw_data = raw_data.drop(columns=['filling_volume'])
        a_part = raw_data.merge(calculate, on=['refrigerant_type'], how='left').drop_duplicates()
        # 用dataframe欄位去filter queryset要用'欄位名稱__in'
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause__in=a_part['device_name']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(coefficient_unit=Value('公噸' + '/公噸', output_field=models.CharField(max_length=50))))).assign(dummy='1')
        ab_part = pd.merge(a_part, coefficient_part, on='dummy', how='left').drop(columns='dummy')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['refrigerant_type']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, left_on='refrigerant_type', right_on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['filling_volume']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        new_order = ['process_area', 'device_name', 'refrigerant_type', 'filling_volume', 'data_unit', 'emission', 'gas_name_x', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        display(final)
        display(final.shape)
    except KeyError:
        print('沒有該設備')
        pass

# 其他設備
@login_required(login_url="/login/")
def other_device_count(coefficient_source, gwp_version):
    try:
        raw_data = pd.DataFrame(list(other_device.objects.values('device_name', "refrigerant_type", "filling_volume").annotate(process_area=Value('逸散', output_field=models.CharField(max_length=50)), data_unit=Value('公噸', output_field=models.CharField(max_length=50))))).assign(dummy='1')
        calculate = raw_data.groupby(["refrigerant_type"]).agg({'filling_volume': 'sum'}).reset_index()
        calculate['filling_volume'] = calculate['filling_volume'].apply(lambda x: round(Decimal(x) / Decimal(1000), 4))
        # 丟掉舊欄位，為了merge時欄位不會重複
        raw_data = raw_data.drop(columns=['filling_volume'])
        a_part = raw_data.merge(calculate, on=['refrigerant_type'], how='left').drop_duplicates()
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause='其他設備').values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(coefficient_unit=Value('公噸' + '/公噸', output_field=models.CharField(max_length=50))))).assign(dummy='1')
        ab_part = pd.merge(a_part, coefficient_part, on='dummy', how='left').drop(columns='dummy')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['refrigerant_type']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, left_on='refrigerant_type', right_on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['filling_volume']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        # 102行做merge兩個表都有'gas_name'欄位, 原本的(左邊)被系統改名叫'gas_name_x'
        new_order = ['process_area', 'device_name', 'refrigerant_type', 'filling_volume', 'data_unit', 'emission', 'gas_name_x', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        display(final)
        display(final.shape)
    except KeyError:
        print('沒有該設備')
        pass


# 溶劑、噴霧劑
@login_required(login_url="/login/")
def solvent_aerosol_emission_sources_count(coefficient_source, gwp_version):
    coefficient_source = '質量平衡法'
    gwp_version = 6
    try:
        raw_main = pd.DataFrame(list(solvent_aerosol_emission_sources.objects.values('id', 'solvent_name', 'solvent_amount').annotate(process_area=Value('溶劑、噴霧劑', output_field=models.CharField(max_length=50)), data_unit=Value('公噸', output_field=models.CharField(max_length=50)))))
        raw_sub = pd.DataFrame(list(additive_section.objects.values('additive_id_id', 'additive_name', 'additive_amount')))
        union_part = pd.merge(raw_sub, raw_main, left_on=['additive_id_id'], right_on=['id'],  how='left').drop(columns=['additive_id_id', 'id'])
        # 溶劑名稱、添加物名稱相同的，將數量做總和
        a_part = union_part.groupby(["solvent_name", "additive_name"]).agg({'solvent_amount': 'sum', 'additive_amount': 'first', 'process_area': 'first', 'data_unit': 'first'}).reset_index()
        # 溶劑數量*比重(0.82)*CO2含量(0.03)
        a_part['solvent_amount'] = a_part['solvent_amount'].apply(lambda x: round(Decimal(x) * Decimal(0.82) * Decimal(0.03), 4))
        # 再跟添加量相乘
        a_part['solvent_amount'] = a_part['solvent_amount'].multiply(a_part['additive_amount'])
        a_part['solvent_amount'] = a_part['solvent_amount'].apply(lambda x: round(x, 4))
        a_part = a_part.drop(columns=['additive_amount']).drop_duplicates()
        coefficient_part = pd.DataFrame(list(coefficient.objects.filter(coefficient_source=coefficient_source).filter(cause__in=a_part['process_area']).values('cause', 'gas_name', 'coefficient', 'coefficient_source').annotate(coefficient_unit=Value('公噸' + '/公噸', output_field=models.CharField(max_length=50)))))
        ab_part = pd.merge(a_part, coefficient_part, left_on='process_area', right_on='cause', how='left')
        gwp = pd.DataFrame(list(coefficient_gwp.objects.filter(version=gwp_version).filter(gas_name__in=ab_part['gas_name']).values('gas_name', 'gwp_coefficient')))
        final = pd.merge(ab_part, gwp, on='gas_name', how='left')
        final['emission'] = final.apply(lambda x: round(Decimal(x['solvent_amount']) * Decimal(x['coefficient']) * Decimal(x['gwp_coefficient']), 4), axis=1)
        new_order = ['process_area', 'solvent_name', 'additive_name', 'solvent_amount', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
        final = final.reindex(columns=new_order)
        display(final)
        display(final.shape)
        print('\n')
    except KeyError:
                print('沒有該設備')
                pass

#
# # 人天清冊/委外人員
# personnel = pd.DataFrame(list(personnel_inventory.objects.values('did').annotate(
#     device_name=Value('化糞池', output_field=CharField(max_length=20)),
#     fuel_type=Value('水肥', output_field=CharField(max_length=20)),
#     total_usage=Cast(Sum(F('WKhours_january') + F('WKhours_february') + F('WKhours_march') + F('WKhours_april') + F('WKhours_may') + F('WKhours_june') +
#                          F('WKhours_july') + F('WKhours_august') + F('WKhours_september') + F('WKhours_october') + F('WKhours_november') + F('WKhours_december')), output_field=models.DecimalField(max_digits=20, decimal_places=4)),
# )))
# personnel = personnel.drop(columns=['did'])
# display(personnel.to_string(index=False))

# # 滅火器
# extinguisher = pd.DataFrame(list(extinguisher.objects.values('extinguisher_type').annotate(
#     sum_count=Cast(Sum(F('chemical_weight') * F('inventory')) / 1000, output_field=models.DecimalField(max_digits=20, decimal_places=4))
# ).order_by('extinguisher_type')))
# display(extinguisher.to_string(index=False))
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
