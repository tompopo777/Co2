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
# generators = pd.DataFrame(list(emergency_generators.objects.values('did').annotate(
#     process_area=Value('固定式燃燒', output_field=models.CharField(max_length=50)),
#     device_name=Value('柴油發電機', output_field=CharField(max_length=20)),
#     fuel_type=Value('柴油', output_field=CharField(max_length=20)),
#     sum_count=Cast(Sum(F('january') + F('february') + F('march') + F('april') + F('may') + F('june') +
#                        F('july') + F('august') + F('september') + F('october') + F('november') + F('december')) / 1000,
#                    output_field=models.DecimalField(max_digits=20, decimal_places=4)),
#     data_unit=Value('公秉', output_field=models.CharField(max_length=50))
# )))
# generators = generators.drop(columns=['did'])
# display(generators.to_string(index=False))
#
#

# 燃燒設備
@login_required(login_url="/login/")
def combustion_equipment(coefficient_source, gwp_version):
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
    final = pd.merge(combustion, coefficient_part, left_on='fuel_type', right_on='cause', how='left')
    final = pd.merge(final, gwp, left_on='gas_name', right_on='gas_name', how='left')
    # 將(A)、(B)、(C)轉為float才能取round
    final['emission'] = final.apply(lambda x: float(x['sum_count']) * float(x['coefficient']) * float(x['gwp_coefficient']), axis=1)
    final['emission'] = final['emission'].round(4)
    new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count', 'data_unit', 'emission', 'gas_name', 'coefficient', 'coefficient_unit', 'coefficient_source', 'gwp_coefficient']
    final = final.reindex(columns=new_order)
    display(final)
    display(final.shape)

# @login_required(login_url="/login/")
# def combustion_equipment(gwp):
#     combustion = pd.DataFrame(list(combustion_equipment.objects.values('device_name', 'fuel_type').annotate(
#         process_area=Value('固定式燃燒', output_field=models.CharField(max_length=50)),
#         sum_count=Cast(Sum(F('fuel_january') + F('fuel_february') + F('fuel_march') + F('fuel_april') + F('fuel_may') + F('fuel_june') + F('fuel_july') + F('fuel_august') + F('fuel_september') + F('fuel_october') + F('fuel_november') + F('fuel_december')) * 1.818 / 1000,
#                        output_field=models.DecimalField(max_digits=20, decimal_places=4)),
#     ).order_by('device_name', 'fuel_type')))
#     new_order = ['process_area', 'device_name', 'fuel_type', 'sum_count']
#     combustion = combustion.reindex(columns=new_order).to_string(index=False)
#     display(combustion)
#     return combustion
#
#
# # 公務車
# official_car = pd.DataFrame(list(official_car.objects.values('vehicle_type', 'fuel_type').annotate(
#     sum_count=Cast(Sum(F('january') + F('february') + F('march') + F('april') + F('may') + F('june') +
#                        F('july') + F('august') + F('september') + F('october') + F('november') + F('december')) / 1000, output_field=models.DecimalField(max_digits=20, decimal_places=4))
# ).order_by('vehicle_type', 'fuel_type')))
# display(official_car.to_string(index=False))
#
# # 逸散(冰箱~其他設備)
# refrigerator = pd.DataFrame(list(refrigerator.objects.values("device_name", "refrigerant_type", "filling_volume")))
# airconditioner = pd.DataFrame(list(airconditioner.objects.values("device_name", "refrigerant_type", "filling_volume")))
# vehicle = pd.DataFrame(list(vehicle.objects.values("device_name", "refrigerant_type", "filling_volume")))
# water_dispenser = pd.DataFrame(list(water_dispenser.objects.values("device_name", "refrigerant_type", "filling_volume")))
# ice_water_dispenser = pd.DataFrame(list(ice_water_dispenser.objects.values("device_name", "refrigerant_type", "filling_volume")))
# ice_maker = pd.DataFrame(list(ice_maker.objects.values("device_name", "refrigerant_type", "filling_volume")))
# other_device = pd.DataFrame(list(other_device.objects.values("device_name", "refrigerant_type", "filling_volume")))
# refrigerant = pd.concat([refrigerator, airconditioner, vehicle, water_dispenser, ice_water_dispenser, ice_maker, other_device])
# calculate = refrigerant.groupby(["device_name", "refrigerant_type"]).agg({'filling_volume': 'sum'}).apply(lambda x: x / 1000)
# refrigerant = refrigerant.drop(columns=['filling_volume'])
# final = refrigerant.merge(calculate, on=["device_name", 'refrigerant_type'], how='left').drop_duplicates()
# display(final.reset_index().to_string(index=False))
#
# # 溶劑、噴霧劑
# solvent = pd.DataFrame(list(solvent_aerosol_emission_sources.objects.values('id', 'solvent_name', 'solvent_amount')))
# addition = pd.DataFrame(list(additive_section.objects.values('additive_id_id', 'additive_name', 'additive_amount')))
# total = pd.merge(addition, solvent, left_on=['additive_id_id'], right_on=['id'],  how='left')
# count = total.groupby(["solvent_name", "additive_name"]).agg({'solvent_amount': 'sum'}).apply(lambda x: x * Decimal(0.82) * Decimal(0.03))
# total = total.drop(columns=['additive_id_id', 'id', 'solvent_amount'])
# final = pd.merge(total, count, on='solvent_name', how='left')
# final['solvent_amount'] = final['solvent_amount'].multiply(final['additive_amount'])
# display(final.drop(columns=['additive_amount']).drop_duplicates().to_string(index=False))
# print('\n')
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
