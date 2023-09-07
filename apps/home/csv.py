import io
import os

import django.forms
import numpy as np
import openpyxl
import pandas as pd
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from urllib import parse
from datetime import datetime
from IPython.core.display import display

from .decorators import register_model_action, model_actions
# from .resource import *
from .forms import *
from django.contrib import messages
from openpyxl import load_workbook
from tablib import Dataset

# from .views import current_user_group_id

from .models import *
from .resource import *

COLUMN_MAPPING = {
    'emergency_generators': {
        'columns': ['years', 'device_id', 'device_capacity', 'position', 'department', 'estimate',
                    'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
                    'september', 'october', 'november', 'december', 'message_board'],  # 欄位清單1
        'column_names': ['年度', '設備編號', '容量(𝓁)', '地點', '部門', '是否推估', '一月', '二月', '三月',
                         '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月', '備註欄'],  # 欄位中文名稱1
        'prefix': '類別一_'
    },
    'combustion_equipment': {
        'columns': ['years', 'device_name', 'device_id', 'fuel_type',
                    'fuel_january', 'fuel_february', 'fuel_march', 'fuel_april', 'fuel_may', 'fuel_june',
                    'fuel_july', 'fuel_august', 'fuel_september', 'fuel_october', 'fuel_november', 'fuel_december',
                    'heat_january', 'heat_february', 'heat_march', 'heat_april', 'heat_may', 'heat_june', 'heat_july',
                    'heat_august', 'heat_september', 'heat_october', 'heat_november', 'heat_december', 'message_board'],
        'column_names': ['年度', '名稱', '編號', '燃料種類', '一月 使用量', '二月 使用量', '三月 使用量', '四月 使用量', '五月 使用量', '六月 使用量',
                         '七月 使用量', '八月 使用量', '九月 使用量', '十月 使用量', '十一月 使用量', '十二月 使用量',
                         '一月 熱值(Kcal/kg)', '二月 熱值(Kcal/kg)', '三月 熱值(Kcal/kg)', '四月 熱值(Kcal/kg)', '五月 熱值(Kcal/kg)', '六月 熱值(Kcal/kg)',
                         '七月 熱值(Kcal/kg)', '八月 熱值(Kcal/kg)', '九月 熱值(Kcal/kg)', '十月 熱值(Kcal/kg)', '十一月 熱值(Kcal/kg)', '十二月 熱值(Kcal/kg)', '備註欄'],
        'prefix': '類別一_'
    },
    'official_car': {
        'columns': ['years', 'vehicle_type', 'device_id', 'fuel_type', 'department',
                    'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
                    'september', 'october', 'november', 'december',
                    'urea_january', 'urea_february', 'urea_march', 'urea_april', 'urea_may', 'urea_june', 'urea_july',
                    'urea_august', 'urea_september', 'urea_october', 'urea_november', 'urea_december',
                    'urea_content_median', 'urea_water_median', 'message_board'],
        'column_names': ['年度', '類別', '編號', '燃料種類', '所屬單位',
                         '耗用量 一月', '耗用量 二月', '耗用量 三月', '耗用量 四月', '耗用量 五月', '耗用量 六月',
                         '耗用量 七月', '耗用量 八月', '耗用量 九月', '耗用量 十月', '耗用量 十一月', '耗用量 十二月',
                         '尿素 一月', '尿素 二月', '尿素 三月', '尿素 四月', '尿素 五月', '尿素 六月',
                         '尿素 七月', '尿素 八月', '尿素 九月', '尿素 十月', '尿素 十一月', '尿素 十二月',
                         '尿素含量中間值(%)', '尿素水換算中間值(g/cm3)', '備註欄'],
        'prefix': '類別一_'
    },
    'material': {
        'columns': ['years', 'material_name', 'material_id', 'material_type', 'welding_rod', 'welding_rod_id', 'welding_rod_name', 'welding_rod_format', 'carbon_content',
                    'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'message_board'],
        'column_names': ['年度', '名稱', '原物料號', '原/物料', '是否為焊條', '焊條料號', '焊條品名', '焊條規格', '含碳量(%)', '一月', '二月', '三月', '四月', '五月',
                         '六月', '七月', '八月', '九月', '十月', '十一月', '十二月', '備註欄'],
        'prefix': '類別一_'
    },
    'process': {
        'columns': ['years', 'process_stage', 'chemical_id', 'chemical_coefficient', 'burn', 'process_add_name', 'chemical_name', 'chemical_formula', 'CAS_NO', 'unit',
                    'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'message_board'],
        'column_names': ['年度', '製程使用階段', '化學品料號', '化學品系數', '是否燃燒', '製程添加名稱', '化學品名', '化學式', 'CAS編號', '使用量單位',
                         '一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月', '備註欄'],
        'prefix': '類別一_'
    },
    'process_gas': {
        'columns': ['years', 'receipt_number', 'department', 'receipt_date', 'gas_name', 'amount', 'unit', 'per_amount', 'per_unit', 'message_board'],
        'column_names': ['年度', '單號', '所屬部門', '領用日期', '氣體名稱', '數量', '數量單位', '每單位規格', '單位', '備註欄'],
        'prefix': '類別一_'
    },
    'refrigerator': {
        'columns': ['years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                    'filling_volume', 'refrigerant_type', 'filling_fix_volume', 'effusion_rate', 'message_board'],
        'column_names': ['年度', '編號', '名稱', '品牌', '型號', '位置', '購買年份', '規格填充量', '冷媒類型', '維修填充量(kg)', '逸散率(%)', '備註欄'],
        'prefix': '類別一_'
    },
    'airconditioner': {
        'columns': ['years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                    'filling_volume', 'refrigerant_type', 'filling_fix_volume', 'effusion_rate', 'message_board'],
        'column_names': ['年度', '編號', '名稱', '品牌', '型號', '位置', '購買年份', '規格填充量', '冷媒類型', '維修填充量(kg)', '逸散率(%)', '備註欄'],
        'prefix': '類別一_'
    },
    'vehicle': {
        'columns': ['years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                    'filling_volume', 'refrigerant_type', 'filling_fix_volume', 'effusion_rate', 'message_board'],
        'column_names': ['年度', '編號', '名稱', '品牌', '型號', '位置', '購買年份', '規格填充量', '冷媒類型', '維修填充量(kg)', '逸散率(%)', '備註欄'],
        'prefix': '類別一_'
    },
    'water_dispenser': {
        'columns': ['years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                    'filling_volume', 'refrigerant_type', 'filling_fix_volume', 'effusion_rate', 'message_board'],
        'column_names': ['年度', '編號', '名稱', '品牌', '型號', '位置', '購買年份', '規格填充量', '冷媒類型', '維修填充量(kg)', '逸散率(%)', '備註欄'],
        'prefix': '類別一_'
    },
    'ice_water_dispenser': {
        'columns': ['years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                    'filling_volume', 'refrigerant_type', 'filling_fix_volume', 'effusion_rate', 'message_board'],
        'column_names': ['年度', '編號', '名稱', '品牌', '型號', '位置', '購買年份', '規格填充量', '冷媒類型', '維修填充量(kg)', '逸散率(%)', '備註欄'],
        'prefix': '類別一_'
    },
    'ice_maker': {
        'columns': ['years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                    'filling_volume', 'refrigerant_type', 'filling_fix_volume', 'effusion_rate', 'message_board'],
        'column_names': ['年度', '編號', '名稱', '品牌', '型號', '位置', '購買年份', '規格填充量', '冷媒類型', '維修填充量(kg)', '逸散率(%)', '備註欄'],
        'prefix': '類別一_'
    },
    'other_device': {
        'columns': ['years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                    'filling_volume', 'effusion_rate', 'device_type', 'refrigerant_type', 'filling_fix_volume', 'message_board'],
        'column_names': ['年度', '設備編號', '設備名稱', '設備品牌', '型號', '放置位置', '該設備購買年月', '規格填充量', '冷媒類型', '維修填充量(kg)', '設備種類', '逸散率(%)', '備註欄'],
        'prefix': '類別一_'
    },
    'extinguisher': {
        'columns': ['years', 'device_id', 'extinguisher_vendor', 'extinguisher_type', 'position', 'inventory',
                    'chemical_weight', 'using_amount', 'monthly', 'replace_filling_amount', 'replace_filling_date', 'message_board'],
        'column_names': ['年度', '設備編號', '廠商', '類型', '擺放位置(廠別)', '庫存量', '藥劑重量(單位:kg)', '使用量數量', '使用月份', '更換/填充量', '更換/填充日期', '備註欄'],
        'prefix': '類別一_'
    },
    'personnel_inventory': {
        'columns': ['years', 'classification',
                    'people_number_jan', 'people_number_feb', 'people_number_mar', 'people_number_apr', 'people_number_may', 'people_number_jun',
                    'people_number_jul', 'people_number_aug', 'people_number_sept', 'people_number_oct', 'people_number_nov', 'people_number_dec',
                    'daily_working_hours_jan', 'daily_working_hours_feb', 'daily_working_hours_mar', 'daily_working_hours_apr', 'daily_working_hours_may', 'daily_working_hours_jun',
                    'daily_working_hours_jul', 'daily_working_hours_aug', 'daily_working_hours_sept', 'daily_working_hours_oct', 'daily_working_hours_nov', 'daily_working_hours_dec',
                    'work_day_jan', 'work_day_feb', 'work_day_mar', 'work_day_apr', 'work_day_may', 'work_day_jun',
                    'work_day_jul', 'work_day_aug', 'work_day_sept', 'work_day_oct', 'work_day_nov', 'work_day_dec',
                    'holidays_jan', 'holidays_feb', 'holidays_mar', 'holidays_apr', 'holidays_may', 'holidays_jun',
                    'holidays_jul', 'holidays_aug', 'holidays_sept', 'holidays_oct', 'holidays_nov', 'holidays_dec',
                    'overtime_jan', 'overtime_feb', 'overtime_mar', 'overtime_apr', 'overtime_may', 'overtime_jun',
                    'overtime_jul', 'overtime_aug', 'overtime_sept', 'overtime_oct', 'overtime_nov', 'overtime_dec',
                    'leave_hours_jan', 'leave_hours_feb', 'leave_hours_mar', 'leave_hours_apr', 'leave_hours_may', 'leave_hours_jun',
                    'leave_hours_jul', 'leave_hours_aug', 'leave_hours_sept', 'leave_hours_oct', 'leave_hours_nov', 'leave_hours_dec',
                    'compensatory_leave_hours_jan', 'compensatory_leave_hours_feb', 'compensatory_leave_hours_mar', 'compensatory_leave_hours_apr', 'compensatory_leave_hours_may', 'compensatory_leave_hours_jun',
                    'compensatory_leave_hours_jul', 'compensatory_leave_hours_aug', 'compensatory_leave_hours_sept', 'compensatory_leave_hours_oct', 'compensatory_leave_hours_nov', 'compensatory_leave_hours_dec',
                    'message_board'],
        'column_names': ['年度', '人員類別',
                         '一月人數', '二月人數', '三月人數', '四月人數', '五月人數', '六月人數',
                         '七月人數', '八月人數', '九月人數', '十月人數', '十一月人數', '十二月人數',
                         '一月每日工時', '二月每日工時', '三月每日工時', '四月每日工時', '五月每日工時', '六月每日工時',
                         '七月每日工時', '八月每日工時', '九月每日工時', '十月每日工時', '十一月每日工時', '十二月每日工時',
                         '一月工作天數', '二月工作天數', '三月工作天數', '四月工作天數', '五月工作天數', '六月工作天數',
                         '七月工作天數', '八月工作天數', '九月工作天數', '十月工作天數', '十一月工作天數', '十二月工作天數',
                         '一月公休天數', '二月公休天數', '三月公休天數', '四月公休天數', '五月公休天數', '六月公休天數',
                         '七月公休天數', '八月公休天數', '九月公休天數', '十月公休天數', '十一月公休天數', '十二月公休天數',
                         '一月加班天數', '二月加班天數', '三月加班天數', '四月加班天數', '五月加班天數', '六月加班天數',
                         '七月加班天數', '八月加班天數', '九月加班天數', '十月加班天數', '十一月加班天數', '十二月加班天數',
                         '一月請假天數', '二月請假天數', '三月請假天數', '四月請假天數', '五月請假天數', '六月請假天數',
                         '七月請假天數', '八月請假天數', '九月請假天數', '十月請假天數', '十一月請假天數', '十二月請假天數',
                         '一月補休天數', '二月補休天數', '三月補休天數', '四月補休天數', '五月補休天數', '六月補休天數',
                         '七月補休天數', '八月補休天數', '九月補休天數', '十月補休天數', '十一月補休天數', '十二月補休天數', '備註欄'],
        'prefix': '類別一_'
    },
    'waste_water': {
        'columns': ['years', 'Pi', 'Wi', 'CODi', 'COD_total', 'Si', 'MCFj', 'Bo', 'Ri', 'message_board'],
        'column_names': ['年度', 'Pi:工業部門生產量', 'Wi:廢水產生量', 'CODi:化學需氧量', '每年事業廢水之COD總量', 'Si:污泥移除量', 'MCFj:甲烷修正係數', 'Bo:最大CH4產生量', 'Ri:甲烷移除量', '備註欄'],
        'prefix': '類別一_'
    },
    'waste_sludge': {
        'columns': ['years', 'waste_sludge_treatment_name', 'waste_sludge_inflow_rate', 'average_inlet_MLSS_concentration',
                    'CH4_capture_system_rate', 'combustion_equipment_efficiency', 'message_board'],
        'column_names': ['年度', '廢棄污泥厭氧處理單元名稱', '污泥進流量(立方公尺/年)', '平均進流MLSS濃度(mg/L)', u'CH\u2084捕集系統捕集率', '燃燒設備效率', '備註欄'],
        'prefix': '類別一_'
    },
    'solvent_aerosol_emission_sources': {
        'columns': ['years', 'solvent_name', 'solvent_amount', 'solvent_capacity', 'solvent_capacity_unit', 'gas_name', 'gas_ratio', 'density', 'message_board'],
        'column_names': ['年度', '溶劑、噴霧劑名稱', '數量', '容量', '單位', '氣體名稱', '氣體含量(%)', '密度', '備註欄'],
        'prefix': '類別一_'
    },
    'VOCs_one': {
        'columns': ['years', 'emission', 'concentration_ch4', 'message_board'],
        'column_names': ['年度', 'VOCs排放量(千立方公尺/年)', u'CH\u2084濃度(ppm)', '備註欄'],
        'prefix': '類別一_'
    },
    'VOCs_two': {
        'columns': ['years', 'disposal_volume', 'concentration_ch4', 'voc_capture_rate', 'combustion_equipment_rate',
                    'concentration_entrance', 'concentration_exit', 'builtIn_rate', 'custom_rate', 'message_board'],
        'column_names': ['年度', 'VOCs排放量(千立方公尺/年)', u'CH\u2084濃度', 'VOCs設備補集率', '燃燒設備效率', '入口濃度', '出口濃度', '內設值', '自訂值', '備註欄'],
        'prefix': '類別一_'
    },
    'electricity': {
        'columns': ['years', 'EMI_id', 'meter_location', 'address', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
                    'september', 'october', 'november', 'december', 'message_board'],
        'column_names': ['年度', '電表編號', '電表位置', '地址', '一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月', '備註欄'],
        'prefix': '類別二_'
    },
    'upstream_transportation': {
        'columns': ['years', 'acceptance_receipt', 'commodity_name', 'weight', 'commodity_NW',
                    'organizational_use_products', 'customer', 'supplier', 'supplier_address',
                    'trade_term', 'receiving_address', 'delivery_address',
                    'transport_distance', 'transport_country', 'transport_type', 'transport_fuel', 'paid', 'trips',
                    'overseas_transport_distance', 'overseas_delivery', 'overseas_arrive', 'overseas_paid', 'overseas_trips',
                    'special_transport_distance', 'special_transport_country', 'special_transport_type', 'special_transport_fuel', 'special_paid', 'special_trips',
                    'air_transport_distance', 'air_delivery', 'air_arrive', 'air_paid', 'air_trips', 'message_board'],
        'column_names': ['年度', '單號', '商品', '淨/毛重', '重量(噸)', '組織使用產品', '客戶', '供應商名稱', '供應商地址', '貿易條件', '接貨地點', '送貨地點',
                         '陸運運輸距離(km)', '陸運運輸國家', '陸運交通工具', '陸運燃料', '陸運支付方', '陸運趟次',
                         '海運運輸距離距離(nm)', '出貨港口', '到達港口', '海運支付方', '海運趟次',
                         '特殊陸運運輸距離(km)', '特殊陸運運輸國家', '特殊陸運交通工具', '特殊陸運燃料', '特殊陸運支付方', '特殊陸運趟次',
                         '空運運輸距離(km)', '出貨機場', '到達機場', '空運支付方', '空運趟次', '備註欄'],
        'prefix': '類別三_'
    },
    'downstream_transportation': {
        'columns': ['years', 'acceptance_receipt', 'commodity_name', 'weight', 'commodity_NW',
                    'customer', 'supplier', 'supplier_address',
                    'trade_term', 'receiving_address', 'delivery_address',
                    'transport_distance', 'transport_country', 'transport_type', 'transport_fuel', 'paid', 'trips',
                    'overseas_transport_distance', 'overseas_delivery', 'overseas_arrive', 'overseas_paid', 'overseas_trips',
                    'special_transport_distance', 'special_transport_country', 'special_transport_type', 'special_transport_fuel', 'special_paid', 'special_trips',
                    'air_transport_distance', 'air_delivery', 'air_arrive', 'air_paid', 'air_trips', 'message_board'],
        'column_names': ['年度', '單號', '商品', '淨/毛重', '重量(噸)', '客戶', '供應商名稱', '供應商地址', '貿易條件', '接貨地點', '送貨地點',
                         '陸運運輸距離(km)', '陸運運輸國家', '陸運交通工具', '陸運燃料', '陸運支付方', '陸運趟次',
                         '海運運輸距離距離(nm)', '出貨港口', '到達港口', '海運支付方', '海運趟次',
                         '特殊陸運運輸距離(km)', '特殊陸運運輸國家', '特殊陸運交通工具', '特殊陸運燃料', '特殊陸運支付方', '特殊陸運趟次',
                         '空運運輸距離(km)', '出貨機場', '到達機場', '空運支付方', '空運趟次', '備註欄'],
        'prefix': '類別三_'
    },
    'waste_process': {
        'columns': ['years', 'waste_name', 'waste_weigh', 'waste_date', 'waste_location', 'waste_disposal', 'waste_disposal_vendor',
                    'transport_type', 'transport_fuel', 'transport_distance', 'message_board'],
        'column_names': ['年度', '名稱', '重量(噸)', '運送時間', '處置地點', '處理方式', '處理廠商名稱', '運輸方式', '運輸燃料', '運輸距離(km)', '備註欄'],
        'prefix': '類別四_'
    },
    'waste': {
        'columns': ['years', 'waste_name', 'waste_weigh', 'waste_date', 'waste_location', 'waste_disposal', 'waste_disposal_vendor',
                    'message_board'],
        'column_names': ['年度', '名稱', '重量(噸)', '運送時間', '處置地點', '處理方式', '處理廠商名稱', '備註欄'],
        'prefix': '類別四_'
    },
    'pipe_wastewater': {
        'columns': ['years', 'pipe_id', 'address', 'factory', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
                    'september', 'october', 'november', 'december', 'message_board'],
        'column_names': ['年度', '納管編號', '廠別', '地址', '一月', '二月', '三月', '四月', '五月', '六月',
                         '七月', '八月', '九月', '十月', '十一月', '十二月', '備註欄'],
        'prefix': '類別四_'
    },
    'purchase_material': {
        'columns': ['years', 'product_id', 'product_name', 'vendor', 'category_name', 'material_type',
                    'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
                    'september', 'october', 'november', 'december', 'message_board'],
        'column_names': ['年度', '產品編號', '產品名稱', '廠商', '大類名稱', '原/物料',
                         '一月', '二月', '三月', '四月', '五月', '六月',
                         '七月', '八月', '九月', '十月', '十一月', '十二月', '備註欄'],
        'prefix': '類別四_'
    },
    'product_indirect_emissions': {
        'columns': ['years', 'product_id', 'product_name', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
                    'september', 'october', 'november', 'december', 'message_board'],
        'column_names': ['年度', '產品編號', '產品名稱', '一月', '二月', '三月', '四月', '五月', '六月',
                         '七月', '八月', '九月', '十月', '十一月', '十二月', '備註欄'],
        'prefix': '類別五_'
    },
    'employee_business_trip': {
        'columns': ['id', 'years', 'business_trip_number', 'employee_id', 'department', 'employee_name', 'business_trip_location', 'business_trip_date', 'message_board'],
        'column_names': ['出差行程編號', '年度', '出差單號', '員工編號', '部門', '姓名', '出差地點', '啟程日期', '備註欄'],
        'prefix': '類別三_'
    },
    'trip_section': {
        'columns': ['departure', 'transportation', 'distance', 'trip_id'],
        'column_names': ['出發地', '交通工具', '距離', '出差行程編號'],
    },
    'employee_commute': {
        'columns': ['id', 'years', 'employee_id', 'department', 'employee_name', 'city', 'township', 'address', 'commute_distance', 'work_days', 'message_board'],
        'column_names': ['員工通勤編號', '年度', '員工編號', '部門', '姓名', '居住城市', '鄉鎮市區', '行政區公家機關地址', '至公司距離(km)', '年工作天數', '備註欄'],
        'prefix': '類別三_'
    },
    'transportation_way': {
        'columns': ['transportation', 'commute'],
        'column_names': ['交通工具', '員工通勤編號'],
    },

    # ... 其他資料庫表格和欄位清單映射
}


# 匯出功能
@csrf_exempt
@require_http_methods(["GET"])
def export_excel(request):
    if request.method == "GET":
        # did = request.POST.get('did')
        # year = request.POST.get('yearInput')
        device_id = request.session.get('dropdown_three')
        year = request.session.get('years')
        factory_id = request.session.get('factory_id')
        excel_did = section_two.objects.filter(did__exact=int(device_id))

        # 取得欄位清單和欄位中文名稱
        table_name = excel_did[0].t_name
        column_mapping = COLUMN_MAPPING[table_name]
        prefix = column_mapping.get('prefix', '')
        columns = column_mapping['columns']
        column_names = column_mapping['column_names']
        device_name = excel_did[0].d_name

        # 根據所需欄位清單查詢資料
        data = globals()[table_name].objects.all().filter(company_id=factory_id, years=year).values(*columns)

        # 將查詢結果轉換為DataFrame
        df = pd.DataFrame(list(data))

        if df.empty:
            print("empty")
            export_message = {
                'export_error': f'{device_name}沒有任何資料可以匯出!'
            }
            return export_message
        else:
            # 將欄位名稱改成中文
            df.columns = column_names

            if table_name == 'employee_business_trip':
                # 取得母表和子表的欄位資訊
                mother_columns = COLUMN_MAPPING['employee_business_trip']['columns']
                child_columns = COLUMN_MAPPING['trip_section']['columns']

                # 取得母表和子表的資料
                mother_data = employee_business_trip.objects.all().filter(company_id=factory_id, years=year).values(*mother_columns)
                child_data = trip_section.objects.all().values(*child_columns)

                # 將母表和子表的資料轉換為 DataFrame
                mother_df = pd.DataFrame(list(mother_data))
                child_df = pd.DataFrame(list(child_data))

                # 將子表的資料加入到母表的資料中
                df = pd.merge(mother_df, child_df, left_on='id', right_on='trip_id', how='left')

                df.drop(columns=['id'], inplace=True)
                df.rename(columns={'years': '年度', 'business_trip_number': '出差單號', 'employee_id': '員工編號', 'department': '部門', 'employee_name': '姓名', 'business_trip_location': '出差地點', 'business_trip_date': '啟程日期',
                                   'departure': '出發地', 'transportation': '交通工具', 'distance': '距離', 'trip_id': '出差行程編號', 'message_board': '備註欄'}, inplace=True)

                # 欄位順序列表（自訂順序）
                custom_column_order = ['年度', '出差單號', '員工編號', '部門', '姓名', '出差地點', '啟程日期', '出發地', '交通工具', '距離', '出差行程編號', '備註欄']

                # 將 DataFrame 欄位順序重新排列
                df = df.reindex(columns=custom_column_order)

            elif table_name == 'employee_commute':
                # 取得母表和子表的欄位資訊
                mother_columns = COLUMN_MAPPING['employee_commute']['columns']
                child_columns = COLUMN_MAPPING['transportation_way']['columns']

                # 取得母表和子表的資料
                mother_data = employee_commute.objects.all().filter(company_id=factory_id, years=year).values(*mother_columns)
                child_data = transportation_way.objects.all().values(*child_columns)

                # 將母表和子表的資料轉換為 DataFrame
                mother_df = pd.DataFrame(list(mother_data))
                child_df = pd.DataFrame(list(child_data))

                # 將子表的資料加入到母表的資料中
                df = pd.merge(mother_df, child_df, left_on='id', right_on='commute', how='left')

                df.drop(columns=['id'], inplace=True)

                df.rename(columns={'years': '年度', 'employee_id': '員工編號', 'department': '部門', 'employee_name': '姓名', 'city': '居住城市', 'township': '鄉鎮市區', 'address': '行政區公家機關地址',
                                   'commute_distance': '至公司距離(km)', 'work_days': '年工作天數', 'transportation': '交通工具', 'commute': '員工通勤編號', 'message_board': '備註欄'}, inplace=True)

                # 欄位順序列表（自訂順序）
                custom_column_order = ['年度', '員工編號', '部門', '姓名', '居住城市', '鄉鎮市區', '行政區公家機關地址', '至公司距離(km)', '年工作天數', '交通工具', '員工通勤編號', '備註欄']

                # 將 DataFrame 欄位順序重新排列
                df = df.reindex(columns=custom_column_order)

            excel_name = prefix + excel_did[0].d_name + '.xlsx'
            output = df
            display(output)

            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=' + parse.quote(excel_name, encoding="UTF-8")

            print("output!!!!", output)

            # 匯出Excel檔案
            output.to_excel(response, index=False)
            return response

    else:
        # 呈現選擇保存位置的表格
        return render(request, 'home/carbon-system.html')

        # 創建Excel文件
        # excel_name = prefix + excel_did[0].d_name + '.xlsx'
        # output = io.BytesIO()
        # writer = pd.ExcelWriter(output, engine='xlsxwriter')
        # df.to_excel(writer, index=False, sheet_name='Sheet1')
        # writer.save()
        # output.seek(0)

        # 下載 Excel 文件
        # response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
        # response['Content-Disposition'] = 'attachment; filename=' + parse.quote(excel_name, encoding="UTF-8")


# 下載公版
@csrf_exempt
@require_http_methods(["GET"])
def public_version(request):
    if request.method == 'GET':
        # 取得設備編號、公司編號、檔案
        device_id = request.session.get('dropdown_three')
        excel_did = section_two.objects.filter(did__exact=int(device_id))

        # 取得欄位清單和欄位中文名稱
        table_name = excel_did[0].t_name
        column_mapping = COLUMN_MAPPING[table_name]
        prefix = column_mapping.get('prefix', '')
        columns = column_mapping['columns']
        column_names = column_mapping['column_names']

        # 創建空的DataFrame
        df = pd.DataFrame(columns=columns)

        # 將欄位名稱改成中文
        df.columns = column_names

        if table_name == 'employee_business_trip':
            column_names = ['年度', '出差單號', '員工編號', '部門', '姓名', '出差地點', '啟程日期', '出發地', '交通工具', '距離', '出差行程編號', '備註欄']
        elif table_name == 'employee_commute':
            column_names = ['年度', '員工編號', '部門', '姓名', '居住城市', '鄉鎮市區', '行政區公家機關地址', '至公司距離(km)', '年工作天數', '交通工具', '員工通勤編號', '備註欄']

        # 創建空的DataFrame
        df = pd.DataFrame(columns=column_names)

        # 創建Excel文件
        excel_name = prefix + excel_did[0].d_name + '.xlsx'
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.save()
        output.seek(0)

        # 下載 Excel 文件
        response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=' + parse.quote(excel_name, encoding="UTF-8")

        return response

    else:
        # 呈現選擇保存位置的表格
        return render(request, 'home/carbon-system.html')


def cut_horizontal_df(df):
    pass


# def cut_vertical_df(excel_file):
#     df = pd.read_excel(excel_file)

class CutVerticalDF:
    def __init__(self, excel_file, sheet_name):
        self.excel_file = excel_file
        self.sheet_name = sheet_name
        self.df = None

    def read_excel(self):
        self.df = pd.read_excel(self.excel_file, sheet_name=self.sheet_name)
        self.df = self.df.dropna(axis=0, how='all')
        self.df = self.df.dropna(axis=1, how='all')

    def find_column_names(self):
        # 找到'提供單位'column中值為'例'的row
        idx = self.df[self.df['提供單位'] == '例'].index[0]
        column_names = self.df.loc[idx - 1].fillna(self.df.loc[idx - 2])
        self.df = self.df.iloc[idx:]
        self.df.columns = column_names

    def filter_data(self):
        # 將['序號']欄位型態不為int的row刪除
        self.df = self.df[self.df['序號'].apply(lambda x: isinstance(x, int))]
        # 刪除整個為空的column
        self.df = self.df.loc[:, ~self.df.columns.isna()]
        # 除了['序號']欄位以外，刪除整個為空的row
        self.df = self.df.dropna(subset=self.df.columns.difference(['序號']), how='all')

    def final_rebuild(self):
        # 刪除'序號'欄位
        self.df.drop(['序號'], axis=1, inplace=True)
        # 重製索引
        self.df.reset_index(drop=True, inplace=True)


class CutEmergencyGenerator(CutVerticalDF):
    def drop_column(self):
        # 删除特定統計欄位: '佐證資料'和'合計'
        self.df.drop(['佐證資料', '合計'], axis=1, inplace=True)

    def process(self):
        # self.read_excel()
        # self.find_column_names()
        # self.drop_column()
        # self.filter_data()
        # self.final_rebuild()
        super().read_excel()
        super().find_column_names()
        self.drop_column()
        super().filter_data()
        super().final_rebuild()


class CutOfficialCar(CutVerticalDF):
    def drop_column(self):
        # 删除特定統計欄位: '佐證資料'和'合計'
        self.df.drop(['佐證資料', '合計'], axis=1, inplace=True)

    def find_urea_median(self):
        # 找到'尿素含量'跟'尿素水'欄位
        content = self.df[self.df['是否添加尿素'] == '尿素含量\n中間值 (%)'].index[0]
        self.df['尿素含量\n中間值 (%)'] = self.df.at[content + 1, '是否添加尿素']

        water = self.df[self.df[self.df.columns[pd.isna(self.df.columns)][0]] == '尿素水換算\n中間值 (g/cm3)'].index[0]
        self.df['尿素水換算\n中間值 (g/cm3)'] = self.df.at[water + 1, '是否添加尿素']

        # 將'添加尿素'!='有'的'尿素含量'、'尿素水'欄位資料轉成null
        self.df.loc[self.df['是否添加尿素'] != '有', ['尿素含量\n中間值 (%)', '尿素水換算\n中間值 (g/cm3)']] = None

    def urea_drop_column(self):
        # 删除特定統計欄位: '佐證資料'和'合計'
        self.df.drop(['是否添加尿素', '尿素佐證資料'], axis=1, inplace=True)

    def gas_process(self):
        super().read_excel()
        super().find_column_names()
        self.drop_column()
        self.filter_data()

    def diesel_process(self):
        super().read_excel()
        super().find_column_names()
        self.drop_column()
        self.find_urea_median()
        self.urea_drop_column()
        self.filter_data()


class CutProcess(CutVerticalDF):
    def drop_column(self):
        # 删除特定統計欄位: '佐證資料'和'合計'
        self.df.drop(['合計', '佐證資料'], axis=1, inplace=True)

    def replace_data(self):
        # 使用replace方法将值替换为True和False
        self.df['是否燃燒'] = self.df['是否燃燒'].replace({'是': True, '否': False})

    def process(self):
        # self.read_excel()
        # self.find_column_names()
        # self.drop_column()
        # self.filter_data()
        # self.final_rebuild()
        super().read_excel()
        super().find_column_names()
        self.drop_column()
        super().filter_data()
        self.replace_data()
        super().final_rebuild()


class CutPersonInventory(CutVerticalDF):
    def find_column_names(self):
        # 找到'提供單位'column中值為'例1月'的row
        idx = self.df[self.df['提供單位'] == '例1月'].index[0]
        column_names = self.df.loc[idx - 1].fillna(self.df.loc[idx - 2])
        self.df = self.df.iloc[idx:]
        self.df.columns = column_names

    def drop_column(self):
        # 删除特定統計欄位: '當月總工作時數', '當月總工作人天', '佐證資料'，只有宿舍有'當月總宿舍時數'
        drop_list = ['當月總工作時數', '當月總工作人天', '佐證資料', '當月總宿舍時數']
        column_name = [col for col in drop_list if col in self.df.columns]
        self.df.drop(columns=column_name, inplace=True)

    def filter_data(self):
        # 將['序號']欄位型態不為int的row刪除
        keep_months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
        self.df = self.df[self.df['月份'].isin(keep_months)]
        # 刪除整個為空的column
        self.df = self.df.loc[:, ~self.df.columns.isna()]
        # 將空欄位補0
        self.df.fillna(0, inplace=True)

    def final_rebuild(self):
        # 重製索引
        self.df.reset_index(drop=True, inplace=True)

    def process(self):
        super().read_excel()
        self.find_column_names()
        self.drop_column()
        self.filter_data()
        self.final_rebuild()


def import_excel(request, myfile):
    if request.method == 'POST':
        message = {}
        factory_id = request.session.get('factory_id')
        did = request.session.get('dropdown_three')
        model_name = section_two.objects.get(did=did).t_name
        model = apps.get_model('home', model_name)
        years = timezone.now().year
        rename = {
            'emergency_generators': {
                '緊急發電機編號': 'device_id',
                '緊急發電機容量\n(千瓦)': 'device_capacity',
                '所屬單位': 'department',
                '設置地點': 'position',
                '1月': 'january',
                '2月': 'february',
                '3月': 'march',
                '4月': 'april',
                '5月': 'may',
                '6月': 'june',
                '7月': 'july',
                '8月': 'august',
                '9月': 'september',
                '10月': 'october',
                '11月': 'november',
                '12月': 'december',
            },
            'combustion_equipment': {

            },
            'official_car': {
                '車輛類別': 'vehicle_type',
                '設備編號/車牌號碼': 'device_id',
                '所屬部門': 'department',
                '1月': 'january',
                '2月': 'february',
                '3月': 'march',
                '4月': 'april',
                '5月': 'may',
                '6月': 'june',
                '7月': 'july',
                '8月': 'august',
                '9月': 'september',
                '10月': 'october',
                '11月': 'november',
                '12月': 'december',
                '添加量 (公升)': 'urea_total',
                '尿素含量\n中間值 (%)': 'urea_content_median',
                '尿素水換算\n中間值 (g/cm3)': 'urea_water_median',
            },
            'material': {

            },
            'process': {
                '製程使用階段': 'process_stage',
                '料號': 'chemical_id',
                '是否燃燒': 'burn',
                '製程添加物名稱(學名)': 'process_add_name',
                '化學品名': 'chemical_name',
                '化學式': 'chemical_formula',
                'CAS 編號': 'CAS_NO',
                '1月': 'january',
                '2月': 'february',
                '3月': 'march',
                '4月': 'april',
                '5月': 'may',
                '6月': 'june',
                '7月': 'july',
                '8月': 'august',
                '9月': 'september',
                '10月': 'october',
                '11月': 'november',
                '12月': 'december',
            },
            'refrigerator': {

            },
            'airconditioner': {

            },
            'vehicle': {

            },
            'water_dispenser': {

            },
            'ice_water_dispenser': {

            },
            'ice_maker': {

            },
            'other_device': {

            },
            'extinguisher': {

            },
            'personnel_inventory': {
                '外1月': 'people_number_jan',
                '外2月': 'people_number_feb',
                '外3月': 'people_number_mar',
                '外4月': 'people_number_apr',
                '外5月': 'people_number_may',
                '外6月': 'people_number_jun',
                '外7月': 'people_number_jul',
                '外8月': 'people_number_aug',
                '外9月': 'people_number_sept',
                '外10月': 'people_number_oct',
                '外11月': 'people_number_nov',
                '外12月': 'people_number_dec',
                '外1月': 'daily_working_hours_jan',
                '外2月': 'daily_working_hours_feb',
                '外3月': 'daily_working_hours_mar',
                '外4月': 'daily_working_hours_apr',
                '外5月': 'daily_working_hours_may',
                '外6月': 'daily_working_hours_jun',
                '外7月': 'daily_working_hours_jul',
                '外8月': 'daily_working_hours_aug',
                '外9月': 'daily_working_hours_sep',
                '外10月': 'daily_working_hours_oct',
                '外11月': 'daily_working_hours_nov',
                '外12月': 'daily_working_hours_dec',
                '外1月': 'work_day_hours_jan',
                '外2月': 'work_day_hours_feb',
                '外3月': 'work_day_hours_mar',
                '外4月': 'work_day_hours_apr',
                '外5月': 'work_day_hours_may',
                '外6月': 'work_day_hours_jun',
                '外7月': 'work_day_hours_jul',
                '外8月': 'work_day_hours_aug',
                '外9月': 'work_day_hours_sep',
                '外10月': 'work_day_hours_oct',
                '外11月': 'work_day_hours_nov',
                '外12月': 'work_day_hours_dec',
                '外1月': 'holidays_hours_jan',
                '外2月': 'holidays_hours_feb',
                '外3月': 'holidays_hours_mar',
                '外4月': 'holidays_hours_apr',
                '外5月': 'holidays_hours_may',
                '外6月': 'holidays_hours_jun',
                '外7月': 'holidays_hours_jul',
                '外8月': 'holidays_hours_aug',
                '外9月': 'holidays_hours_sep',
                '外10月': 'holidays_hours_oct',
                '外11月': 'holidays_hours_nov',
                '外12月': 'holidays_hours_dec',
                '外1月': 'overtime_hours_jan',
                '外2月': 'overtime_hours_feb',
                '外3月': 'overtime_hours_mar',
                '外4月': 'overtime_hours_apr',
                '外5月': 'overtime_hours_may',
                '外6月': 'overtime_hours_jun',
                '外7月': 'overtime_hours_jul',
                '外8月': 'overtime_hours_aug',
                '外9月': 'overtime_hours_sep',
                '外10月': 'overtime_hours_oct',
                '外11月': 'overtime_hours_nov',
                '外12月': 'overtime_hours_dec',
                '外1月': 'leave_hours_hours_jan',
                '外2月': 'leave_hours_hours_feb',
                '外3月': 'leave_hours_hours_mar',
                '外4月': 'leave_hours_hours_apr',
                '外5月': 'leave_hours_hours_may',
                '外6月': 'leave_hours_hours_jun',
                '外7月': 'leave_hours_hours_jul',
                '外8月': 'leave_hours_hours_aug',
                '外9月': 'leave_hours_hours_sep',
                '外10月': 'leave_hours_hours_oct',
                '外11月': 'leave_hours_hours_nov',
                '外12月': 'leave_hours_hours_dec',
                '外1月': 'compensatory_leave_hours_hours_jan',
                '外2月': 'compensatory_leave_hours_hours_feb',
                '外3月': 'compensatory_leave_hours_hours_mar',
                '外4月': 'compensatory_leave_hours_hours_apr',
                '外5月': 'compensatory_leave_hours_hours_may',
                '外6月': 'compensatory_leave_hours_hours_jun',
                '外7月': 'compensatory_leave_hours_hours_jul',
                '外8月': 'compensatory_leave_hours_hours_aug',
                '外9月': 'compensatory_leave_hours_hours_sep',
                '外10月': 'compensatory_leave_hours_hours_oct',
                '外11月': 'compensatory_leave_hours_hours_nov',
                '外12月': 'compensatory_leave_hours_hours_dec',
            },
            'waste_water': {

            },
            'waste_sludge': {

            },
            'solvent_aerosol_emission_sources': {

            },
            'VOCs_one': {

            },
            'VOCs_two': {

            },
            'electricity': {

            },
            'upstream_transportation': {

            },
            'downstream_transportation': {

            },
            'employee_commute': {

            },
            'employee_business_trip': {

            },
            'waste': {

            },
            'pipe_wastewater': {

            },
            'purchase_material': {

            },
            'product_indirect_emissions': {

            },
        }

        def import_to_database(df):
            # 匯入資料庫
            df_records = df.to_dict(orient='records')
            # 將dataframe的NaN轉成None
            df_records = [{k: None if pd.isna(v) else v for k, v in convert.items()} for convert in df_records]

            model_instance = [model(**record) for record in df_records]
            model.objects.bulk_create(model_instance)

            # model_instances = [MyModel(
            #     field_1=record['field_1'],
            #     field_2=record['field_2'],
            # ) for record in df_records]

        @register_model_action('emergency_generators')
        def emergency_generator_dataframe(myfile, sheet_list):
            validation_results = {}

            def find_key_by_value(dictionary, value_to_find):
                for key, value in dictionary.items():
                    if value == value_to_find:
                        return key
                return value_to_find

            # validation
            def clean_device_id(row):
                device_id = row['device_id']
                if not re.match(r'^[a-zA-Z0-9_-]*$', str(device_id)) or pd.isna(device_id):
                    error_message = f"序號: {row.name + 1}，輸入值: {device_id}"
                    if "欄位: 緊急發電機設備編號 (規則: 只能輸入'英文'、'數字'、'-'、'_'、不可為空)" not in validation_results:
                        validation_results["欄位: 緊急發電機設備編號 (規則: 只能輸入'英文'、'數字'、'-'、'_'、不可為空)"] = []
                    validation_results["欄位: 緊急發電機設備編號 (規則: 只能輸入'英文'、'數字'、'-'、'_'、不可為空)"].append(error_message)
                    return None
                return device_id

            def clean_position(row):
                position = row['position']
                if pd.isna(position):
                    error_message = f"序號: {row.name + 1}，輸入值: {position}"
                    if "欄位: 設置地點 (規則: 不可為空)" not in validation_results:
                        validation_results["欄位: 設置地點 (規則: 不可為空)"] = []
                    validation_results["欄位: 設置地點 (規則: 不可為空)"].append(error_message)
                    return None
                return position

            def clean_capacity(row):
                if row['device_capacity'] > 0 and isinstance(row['device_capacity'], (int, float)):
                    # row['device_capacity'] = round(row['device_capacity'], 4)
                    return row['device_capacity']
                else:
                    error_message = f"序號: {row.name + 1}，輸入值: {row['device_capacity']}"
                    if '欄位: 緊急發電機容量 (規則: 輸入值須大於零、不可為空)' not in validation_results:
                        validation_results['欄位: 緊急發電機容量 (規則: 輸入值須大於零、不可為空)'] = []
                    validation_results['欄位: 緊急發電機容量 (規則: 輸入值須大於零、不可為空)'].append(error_message)
                    return None

            def clean_month(row):
                months = ['january', 'february', 'march', 'april', 'may', 'june',
                          'july', 'august', 'september', 'october', 'november', 'december']
                for month in months:
                    value = row[month]
                    if isinstance(value, (int, float)) and value >= 0:
                        row[month] = round(value, 4)
                    else:
                        conv_mont = find_key_by_value(rename[str(model_name)], month)
                        error_message = f"序號: {row.name + 1}，輸入值: {value}"
                        if f'欄位: {conv_mont} (規則: 輸入值須大於等於零、不可為空)' not in validation_results:
                            validation_results[f'欄位: {conv_mont} (規則: 輸入值須大於等於零、不可為空)'] = []
                        validation_results[f'欄位: {conv_mont} (規則: 輸入值須大於等於零、不可為空)'].append(error_message)
                        row[month] = None
                return row

            # dataframe = cut_vertical_df(myfile, sheet_list[0])
            data_processor = CutEmergencyGenerator(myfile, sheet_list[0])
            data_processor.process()
            df = data_processor.df
            df.rename(columns=rename[str(model_name)], inplace=True)
            display(df)

            # 如果excel為空，跳過驗證直接回傳
            if not df.empty:
                # 客製欄位補值
                df['estimate'] = False

                # 驗證
                df['device_id'] = df.apply(clean_device_id, axis=1)
                df['position'] = df.apply(clean_position, axis=1)
                df['device_capacity'] = df.apply(clean_capacity, axis=1)
                df = df.apply(clean_month, axis=1)

            else:
                validation_results = '匯入失敗，excel資料為空!'

            return df, validation_results

        @register_model_action('official_car')
        def official_car_dataframe(myfile, sheet_list):
            validation_results = {}

            def find_key_by_value(dictionary, value_to_find):
                for key, value in dictionary.items():
                    if value == value_to_find:
                        return key
                return value_to_find

            # validation
            def clean_device_id(row, fuel_name):
                device_id = row['device_id']
                index = row['序號']
                if not re.match(r'^[a-zA-Z0-9_-]*$', str(device_id)) or pd.isna(device_id):
                    error_message = f"序號: {index}，輸入值: {device_id}"
                    if f"'{fuel_name}分頁'欄位: 設備編號/車牌號碼 (規則: 只能輸入'英文'、'數字'、'-'、'_'、不可為空)" not in validation_results:
                        validation_results[f"'{fuel_name}分頁'欄位: 設備編號/車牌號碼 (規則: 只能輸入'英文'、'數字'、'-'、'_'、不可為空)"] = []
                    validation_results[f"'{fuel_name}分頁'欄位: 設備編號/車牌號碼 (規則: 只能輸入'英文'、'數字'、'-'、'_'、不可為空)"].append(error_message)
                    return None
                return device_id

            def clean_vehicle_type(row, fuel_name):
                vehicle_type = row['vehicle_type']
                index = row['序號']
                for VEHICLE_TYPE in VEHICLE_TYPE_CHOICES:
                    if vehicle_type == VEHICLE_TYPE[0]:
                        return vehicle_type
                error_message = f"序號: {index}，輸入值: {vehicle_type}"
                if f"'{fuel_name}分頁'欄位: 車輛類別 (規則: 請勿自行修改excel下拉選單、不可為空)" not in validation_results:
                    validation_results[f"'{fuel_name}分頁'欄位: 車輛類別 (規則: 請勿自行修改excel下拉選單、不可為空)"] = []
                validation_results[f"'{fuel_name}分頁'欄位: 車輛類別 (規則: 請勿自行修改excel下拉選單、不可為空)"].append(error_message)
                return None

            def clean_month(row, fuel_name):
                index = row['序號']
                months = ['january', 'february', 'march', 'april', 'may', 'june',
                          'july', 'august', 'september', 'october', 'november', 'december']
                for month in months:
                    value = row[month]
                    if isinstance(value, (int, float)) and value >= 0:
                        row[month] = round(value, 4)
                    else:
                        conv_mont = find_key_by_value(rename[str(model_name)], month)
                        error_message = f"序號: {index}，輸入值: {value}"
                        if f"'{fuel_name}分頁'欄位: {conv_mont} (規則: 輸入值須大於等於零、不可為空)" not in validation_results:
                            validation_results[f"'{fuel_name}分頁'欄位: {conv_mont} (規則: 輸入值須大於等於零、不可為空)"] = []
                        validation_results[f"'{fuel_name}分頁'欄位: {conv_mont} (規則: 輸入值須大於等於零、不可為空)"].append(error_message)
                        row[month] = None
                return row

            def clean_urea(row, fuel_name):
                urea_total = row['urea_total']
                index = row['序號']
                urea_content_median = row['urea_content_median']
                urea_water_median = row['urea_water_median']
                # 含量、水為空('是否添加尿素'欄位!='有')，但填了添加量
                if pd.isna(urea_content_median) and pd.isna(urea_water_median) and pd.notna(urea_total):
                    error_message = f"序號: {index}"
                    if f"'{fuel_name}分頁'欄位: 是否添加尿素 (規則: 只能輸入'有' / '無'，已填寫'尿素添加量'，請更正該欄位)" not in validation_results:
                        validation_results[f"'{fuel_name}分頁'欄位: 是否添加尿素 (規則: 只能輸入'有' / '無'，已填寫'尿素添加量'，請更正該欄位)"] = []
                    validation_results[f"'{fuel_name}分頁'欄位: 是否添加尿素 (規則: 只能輸入'有' / '無'，已填寫'尿素添加量'，請更正該欄位)"].append(error_message)

                # 三個其中一個有值
                if pd.notna(urea_content_median) or pd.notna(urea_water_median) or pd.notna(urea_total):
                    if pd.notna(urea_content_median):
                        if isinstance(urea_content_median, (int, float)) and urea_content_median > 0:
                            row['urea_content_median'] = round(urea_content_median, 4)
                        else:
                            error_message = f"輸入值: {urea_content_median}"
                            if f"'{fuel_name}分頁'欄位: 尿素含量中間值 (規則: 只能輸入'數字')" not in validation_results:
                                validation_results[f"'{fuel_name}分頁'欄位: 尿素含量中間值 (規則: 只能輸入'數字')"] = []
                            validation_results[f"'{fuel_name}分頁'欄位: 尿素含量中間值 (規則: 只能輸入'數字')"].append(error_message)
                    if pd.notna(urea_water_median):
                        if isinstance(urea_water_median, (int, float)) and urea_water_median > 0:
                            row['urea_water_median'] = round(urea_water_median, 4)
                        else:
                            error_message = f"輸入值: {urea_water_median}"
                            if f"'{fuel_name}分頁'欄位: 尿素水換算中間值 (規則: 只能輸入'數字')" not in validation_results:
                                validation_results[f"'{fuel_name}分頁'欄位: 尿素水換算中間值 (規則: 只能輸入'數字')"] = []
                            validation_results[f"'{fuel_name}分頁'欄位: 尿素水換算中間值 (規則: 只能輸入'數字')"].append(error_message)
                    if pd.notna(urea_total):
                        if isinstance(urea_total, (int, float)) and urea_total > 0:
                            row['urea_total'] = round(urea_total, 4)
                        else:
                            error_message = f"序號: {index}，輸入值: {urea_total}"
                            if "欄位: 添加量 (公升) (規則: 輸入值須大於零)" not in validation_results:
                                validation_results["欄位: 添加量 (公升) (規則: 規則: 輸入值須大於零)"] = []
                            validation_results["欄位: 添加量 (公升) (規則: 規則: 輸入值須大於零)"].append(error_message)
                return row

            # 燃料種類(汽油)
            fuel = '汽油'
            gas_processor = CutOfficialCar(myfile, sheet_list[0])
            gas_processor.gas_process()
            gas_dataframe = gas_processor.df
            gas = gas_dataframe.rename(columns=rename[str(model_name)], inplace=False)
            # display(gas)
            if not gas.empty:
                # # 驗證
                gas['device_id'] = gas.apply(clean_device_id, axis=1, args=(fuel,))
                gas['vehicle_type'] = gas.apply(clean_vehicle_type, axis=1, args=(fuel,))
                gas = gas.apply(clean_month, axis=1, args=(fuel,))
                gas['fuel_type'] = fuel

            # 燃料種類(柴油)
            fuel = '柴油'
            diesel_processor = CutOfficialCar(myfile, sheet_list[1])
            diesel_processor.diesel_process()
            diesel_dataframe = diesel_processor.df
            diesel = diesel_dataframe.rename(columns=rename[str(model_name)], inplace=False)
            display(diesel)
            if not diesel.empty:
                # # 驗證
                diesel['device_id'] = diesel.apply(clean_device_id, axis=1, args=(fuel,))
                diesel['vehicle_type'] = diesel.apply(clean_vehicle_type, axis=1, args=(fuel,))
                diesel = diesel.apply(clean_month, axis=1, args=(fuel,))
                diesel = diesel.apply(clean_urea, axis=1, args=(fuel,))
                diesel['fuel_type'] = fuel

            df = pd.concat([gas, diesel], ignore_index=True)
            display('after_concat>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n', df)

            if not df.empty:
                # 客製欄位補值

                # 刪除'序號'欄位
                df.drop(['序號'], axis=1, inplace=True)
                # 重製索引
                df.reset_index(drop=True, inplace=True)
            else:
                validation_results = '匯入失敗，excel資料為空!'

            display(df)
            return df, validation_results

        @register_model_action('process')
        def process_dataframe(myfile, sheet_list):
            validation_results = {}

            def find_key_by_value(dictionary, value_to_find):
                for key, value in dictionary.items():
                    if value == value_to_find:
                        return key
                return value_to_find

            # validation
            def clean_chemical_id(row):
                chemical_id = row['chemical_id']
                if not re.match(r'^[a-zA-Z0-9_-]*$', str(chemical_id)) or pd.isna(chemical_id):
                    error_message = f"序號: {row.name + 1}，輸入值: {chemical_id}"
                    if "欄位: 料號 (規則: 只能輸入'英文'、'數字'、'-'、'_'、不可為空)" not in validation_results:
                        validation_results["欄位: 料號 (規則: 只能輸入'英文'、'數字'、'-'、'_'、不可為空)"] = []
                    validation_results["欄位: 料號 (規則: 只能輸入'英文'、'數字'、'-'、'_'、不可為空)"].append(error_message)
                    return None
                return chemical_id

            def clean_burn(row):
                burn = row['burn']
                if pd.notna(burn) and isinstance(burn, bool):
                    return burn
                else:
                    error_message = f"序號: {row.name + 1}，輸入值: {burn}"
                    if "欄位: 是否燃燒 (規則: 只能輸入'是' / '否'、不可為空)" not in validation_results:
                        validation_results["欄位: 是否燃燒 (規則: 只能輸入'是' / '否'、不可為空)"] = []
                    validation_results["欄位: 是否燃燒 (規則: 只能輸入'是' / '否'、不可為空)"].append(error_message)
                    return None

            def clean_process_add_name(row):
                process_add_name = row['process_add_name']
                if pd.isna(process_add_name):
                    error_message = f"序號: {row.name + 1}，輸入值: {process_add_name}"
                    if "欄位: 製程添加物名稱(學名) (規則: 不可為空)" not in validation_results:
                        validation_results["欄位: 製程添加物名稱(學名) (規則: 不可為空)"] = []
                    validation_results["欄位: 製程添加物名稱(學名) (規則: 不可為空)"].append(error_message)
                    return None
                return process_add_name

            def clean_chemical_formula(row):
                chemical_formula = row['chemical_formula']
                if pd.isna(chemical_formula):
                    error_message = f"序號: {row.name + 1}，輸入值: {chemical_formula}"
                    if "欄位: 化學式 (規則: 不可為空)" not in validation_results:
                        validation_results["欄位: 化學式 (規則: 不可為空)"] = []
                    validation_results["欄位: 化學式 (規則: 不可為空)"].append(error_message)
                    return None
                return chemical_formula

            def clean_cas_no(row):
                cas_no = row['CAS_NO']
                if pd.isna(cas_no):
                    error_message = f"序號: {row.name + 1}，輸入值: {cas_no}"
                    if "欄位: CAS 編號 (規則: 不可為空)" not in validation_results:
                        validation_results["欄位: CAS 編號 (規則: 不可為空)"] = []
                    validation_results["欄位: CAS 編號 (規則: 不可為空)"].append(error_message)
                    return None
                return cas_no

            def clean_month(row):
                months = ['january', 'february', 'march', 'april', 'may', 'june',
                          'july', 'august', 'september', 'october', 'november', 'december']
                for month in months:
                    value = row[month]
                    if isinstance(value, (int, float)) and value >= 0:
                        row[month] = round(value, 4)
                    else:
                        conv_mont = find_key_by_value(rename[str(model_name)], month)
                        error_message = f"序號: {row.name + 1}，輸入值: {value}"
                        if f'欄位: {conv_mont} (規則: 輸入值須大於等於零、不可為空)' not in validation_results:
                            validation_results[f'欄位: {conv_mont} (規則: 輸入值須大於等於零、不可為空)'] = []
                        validation_results[f'欄位: {conv_mont} (規則: 輸入值須大於等於零、不可為空)'].append(error_message)
                        row[month] = None
                return row

            process_processor = CutProcess(myfile, sheet_list[0])
            process_processor.process()
            df = process_processor.df
            df.rename(columns=rename[str(model_name)], inplace=True)
            display(df)

            # 如果excel為空，跳過驗證直接回傳
            if not df.empty:
                # 客製欄位補值
                # df['burn'] = False
                df['unit'] = '公斤'
                df['chemical_coefficient'] = 123

                # 驗證
                df['device_id'] = df.apply(clean_chemical_id, axis=1)
                df['clean_burn'] = df.apply(clean_burn, axis=1)
                df['clean_process_add_name'] = df.apply(clean_process_add_name, axis=1)
                df['clean_chemical_formula'] = df.apply(clean_chemical_formula, axis=1)
                df['clean_cas_no'] = df.apply(clean_cas_no, axis=1)
                df = df.apply(clean_month, axis=1)

            else:
                validation_results = '匯入失敗，excel資料為空!'

            return df, validation_results

        @register_model_action('personnel_inventory')
        def personnel_inventory_dataframe(myfile, sheet_list):
            validation_results = {}

            def find_key_by_value(dictionary, value_to_find):
                for key, value in dictionary.items():
                    if value == value_to_find:
                        return key
                return value_to_find

            # validation
            def clean_device_id(row, fuel_name):
                device_id = row['device_id']
                index = row['序號']
                if not re.match(r'^[a-zA-Z0-9_-]*$', str(device_id)) or pd.isna(device_id):
                    error_message = f"序號: {index}，輸入值: {device_id}"
                    if f"'{fuel_name}分頁'欄位: 設備編號/車牌號碼 (規則: 只能輸入'英文'、'數字'、'-'、'_'、不可為空)" not in validation_results:
                        validation_results[f"'{fuel_name}分頁'欄位: 設備編號/車牌號碼 (規則: 只能輸入'英文'、'數字'、'-'、'_'、不可為空)"] = []
                    validation_results[f"'{fuel_name}分頁'欄位: 設備編號/車牌號碼 (規則: 只能輸入'英文'、'數字'、'-'、'_'、不可為空)"].append(error_message)
                    return None
                return device_id

            def clean_vehicle_type(row, fuel_name):
                vehicle_type = row['vehicle_type']
                index = row['序號']
                for VEHICLE_TYPE in VEHICLE_TYPE_CHOICES:
                    if vehicle_type == VEHICLE_TYPE[0]:
                        return vehicle_type
                error_message = f"序號: {index}，輸入值: {vehicle_type}"
                if f"'{fuel_name}分頁'欄位: 車輛類別 (規則: 請勿自行修改excel下拉選單、不可為空)" not in validation_results:
                    validation_results[f"'{fuel_name}分頁'欄位: 車輛類別 (規則: 請勿自行修改excel下拉選單、不可為空)"] = []
                validation_results[f"'{fuel_name}分頁'欄位: 車輛類別 (規則: 請勿自行修改excel下拉選單、不可為空)"].append(error_message)
                return None

            def clean_month(row, fuel_name):
                index = row['序號']
                months = ['january', 'february', 'march', 'april', 'may', 'june',
                          'july', 'august', 'september', 'october', 'november', 'december']
                for month in months:
                    value = row[month]
                    if isinstance(value, (int, float)) and value >= 0:
                        row[month] = round(value, 4)
                    else:
                        conv_mont = find_key_by_value(rename[str(model_name)], month)
                        error_message = f"序號: {index}，輸入值: {value}"
                        if f"'{fuel_name}分頁'欄位: {conv_mont} (規則: 輸入值須大於等於零、不可為空)" not in validation_results:
                            validation_results[f"'{fuel_name}分頁'欄位: {conv_mont} (規則: 輸入值須大於等於零、不可為空)"] = []
                        validation_results[f"'{fuel_name}分頁'欄位: {conv_mont} (規則: 輸入值須大於等於零、不可為空)"].append(error_message)
                        row[month] = None
                return row

            def clean_urea(row, fuel_name):
                urea_total = row['urea_total']
                index = row['序號']
                urea_content_median = row['urea_content_median']
                urea_water_median = row['urea_water_median']
                # 含量、水為空('是否添加尿素'欄位!='有')，但填了添加量
                if pd.isna(urea_content_median) and pd.isna(urea_water_median) and pd.notna(urea_total):
                    error_message = f"序號: {index}"
                    if f"'{fuel_name}分頁'欄位: 是否添加尿素 (規則: 只能輸入'有' / '無'，已填寫'尿素添加量'，請更正該欄位)" not in validation_results:
                        validation_results[f"'{fuel_name}分頁'欄位: 是否添加尿素 (規則: 只能輸入'有' / '無'，已填寫'尿素添加量'，請更正該欄位)"] = []
                    validation_results[f"'{fuel_name}分頁'欄位: 是否添加尿素 (規則: 只能輸入'有' / '無'，已填寫'尿素添加量'，請更正該欄位)"].append(error_message)

                # 三個其中一個有值
                if pd.notna(urea_content_median) or pd.notna(urea_water_median) or pd.notna(urea_total):
                    if pd.notna(urea_content_median):
                        if isinstance(urea_content_median, (int, float)) and urea_content_median > 0:
                            row['urea_content_median'] = round(urea_content_median, 4)
                        else:
                            error_message = f"輸入值: {urea_content_median}"
                            if f"'{fuel_name}分頁'欄位: 尿素含量中間值 (規則: 只能輸入'數字')" not in validation_results:
                                validation_results[f"'{fuel_name}分頁'欄位: 尿素含量中間值 (規則: 只能輸入'數字')"] = []
                            validation_results[f"'{fuel_name}分頁'欄位: 尿素含量中間值 (規則: 只能輸入'數字')"].append(error_message)
                    if pd.notna(urea_water_median):
                        if isinstance(urea_water_median, (int, float)) and urea_water_median > 0:
                            row['urea_water_median'] = round(urea_water_median, 4)
                        else:
                            error_message = f"輸入值: {urea_water_median}"
                            if f"'{fuel_name}分頁'欄位: 尿素水換算中間值 (規則: 只能輸入'數字')" not in validation_results:
                                validation_results[f"'{fuel_name}分頁'欄位: 尿素水換算中間值 (規則: 只能輸入'數字')"] = []
                            validation_results[f"'{fuel_name}分頁'欄位: 尿素水換算中間值 (規則: 只能輸入'數字')"].append(error_message)
                    if pd.notna(urea_total):
                        if isinstance(urea_total, (int, float)) and urea_total > 0:
                            row['urea_total'] = round(urea_total, 4)
                        else:
                            error_message = f"序號: {index}，輸入值: {urea_total}"
                            if "欄位: 添加量 (公升) (規則: 輸入值須大於零)" not in validation_results:
                                validation_results["欄位: 添加量 (公升) (規則: 規則: 輸入值須大於零)"] = []
                            validation_results["欄位: 添加量 (公升) (規則: 規則: 輸入值須大於零)"].append(error_message)
                return row

            # 類型(內部)
            classification = '內部人員清冊'
            inside_processor = CutPersonInventory(myfile, sheet_list[0])
            inside_processor.process()
            inside_dataframe = inside_processor.df
            display(inside_dataframe)
            inside = inside_dataframe.rename(columns=rename[str(model_name)], inplace=False)
            # display('inside\n', inside)
            # display(inside)
            # if not inside.empty:
            #     # # 驗證
            #     inside['device_id'] = inside.apply(clean_device_id, axis=1, args=(classification,))
            #     inside['vehicle_type'] = inside.apply(clean_vehicle_type, axis=1, args=(classification,))
            #     inside = inside.apply(clean_month, axis=1, args=(classification,))
            # display(inside)
            # display(gas_dataframe)

            # 類型(外部)
            classification = '外部人員清冊'
            outside_processor = CutPersonInventory(myfile, sheet_list[1])
            outside_processor.process()
            outside_dataframe = outside_processor.df
            display(outside_dataframe)
            outside = outside_dataframe.rename(columns=rename[str(model_name)], inplace=False)
            # display(outside)
            # if not outside.empty:
            #     # # 驗證
            #     outside['device_id'] = outside.apply(clean_device_id, axis=1, args=(classification,))
            #     outside['vehicle_type'] = outside.apply(clean_vehicle_type, axis=1, args=(classification,))
            #     outside = outside.apply(clean_month, axis=1, args=(classification,))
            #     outside = outside.apply(clean_urea, axis=1, args=(classification,))
            # display(outside)

            # 類型(宿舍)
            classification = '宿舍清冊'
            dormitory_processor = CutPersonInventory(myfile, sheet_list[2])
            dormitory_processor.process()
            dormitory_dataframe = dormitory_processor.df
            display(dormitory_dataframe)
            dormitory = dormitory_dataframe.rename(columns=rename[str(model_name)], inplace=False)
            # display(dormitory)
            # if not dormitory.empty:
            #     # # 驗證
            #     dormitory['device_id'] = dormitory.apply(clean_device_id, axis=1, args=(classification,))
            #     dormitory['vehicle_type'] = dormitory.apply(clean_vehicle_type, axis=1, args=(classification,))
            #     dormitory = dormitory.apply(clean_month, axis=1, args=(classification,))
            #     dormitory = dormitory.apply(clean_urea, axis=1, args=(classification,))
            # # display(dormitory)

            df = pd.concat([gas, diesel], ignore_index=True)
            if not df.empty:
                # 客製欄位補值

                # 刪除'序號'欄位
                df.drop(['序號'], axis=1, inplace=True)
                # 重製索引
                df.reset_index(drop=True, inplace=True)
            else:
                validation_results = '匯入失敗，excel資料為空!'

            display(df)
            return df, validation_results

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>start<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        sheet_list = pd.ExcelFile(myfile).sheet_names
        # print('sheet_list', sheet_list, type(sheet_list))

        # 利用model_name選擇要呼叫的function
        if model_name in model_actions:
            df, final_result = model_actions[model_name](myfile, sheet_list)

            if final_result:
                if isinstance(final_result, str):
                    print('final_result>>>', final_result)
                else:
                    print('final_result>>>\n')
                    for i in final_result:
                        print(i)
                        for j in final_result[i]:
                            print(j)
            # 如果沒有dataframe錯誤訊息，存入資料庫
            else:
                # add common necessary column to dataframe.
                df['did'] = section_two.objects.get(did=did)
                df['company_id'] = factory_id
                df['years'] = years

                # 匯入資料庫
                import_to_database(df)
                final_result = '匯入成功!'

            message = {'import_excel': final_result}
        return message

# 66666666666666666666666666666666666666666666666666666666666666666666666666666666666666666
# def import_excel(request, myfile):
#     if request.method == 'POST':
#         message = {}
#         factory_id = request.session.get('factory_id')
#         did = request.session.get('dropdown_three')
#         model_name = section_two.objects.get(did=did).t_name
#         model = apps.get_model('home', model_name)
#         years = timezone.now().year
#
#         df = cut_vertical_df(myfile)
#
#         rename = {
#             'emergency_generators': {
#                 '緊急發電機編號': 'device_id',
#                 '緊急發電機容量\n(千瓦)': 'device_capacity',
#                 '所屬單位': 'department',
#                 '設置地點': 'position',
#                 '1月': 'january',
#                 '2月': 'february',
#                 '3月': 'march',
#                 '4月': 'april',
#                 '5月': 'may',
#                 '6月': 'june',
#                 '7月': 'july',
#                 '8月': 'august',
#                 '9月': 'september',
#                 '10月': 'october',
#                 '11月': 'november',
#                 '12月': 'december',
#             },
#             'combustion_equipment': {
#
#             },
#             'official_car': {
#
#             },
#             'material': {
#
#             },
#             'process': {
#
#             },
#             'refrigerator': {
#
#             },
#             'airconditioner': {
#
#             },
#             'vehicle': {
#
#             },
#             'water_dispenser': {
#
#             },
#             'ice_water_dispenser': {
#
#             },
#             'ice_maker': {
#
#             },
#             'other_device': {
#
#             },
#             'extinguisher': {
#
#             },
#             'personnel_inventory': {
#
#             },
#             'waste_water': {
#
#             },
#             'waste_sludge': {
#
#             },
#             'solvent_aerosol_emission_sources': {
#
#             },
#             'VOCs_one': {
#
#             },
#             'VOCs_two': {
#
#             },
#             'electricity': {
#
#             },
#             'upstream_transportation': {
#
#             },
#             'downstream_transportation': {
#
#             },
#             'employee_commute': {
#
#             },
#             'employee_business_trip': {
#
#             },
#             'waste': {
#
#             },
#             'pipe_wastewater': {
#
#             },
#             'purchase_material': {
#
#             },
#             'product_indirect_emissions': {
#
#             },
#         }
#
#         # rename dataframe.
#         df.rename(columns=rename[str(model_name)], inplace=True)
#
#         # display(df)
#
#         def find_key_by_value(dictionary, value_to_find):
#             for key, value in dictionary.items():
#                 if value == value_to_find:
#                     return key
#             return value_to_find
#
#         # validation
#         def clean_device_id(row):
#             device_id = row['device_id']
#             if not re.match(r'^[a-zA-Z0-9_-]*$', str(device_id)) or pd.isna(device_id):
#                 error_message = f"序號: {row.name + 1}，輸入值: {device_id}"
#                 if "欄位: 緊急發電機設備編號 (規則: 只能輸入'英文'、'數字'、'-'、'_'、不可為空)" not in validation_results:
#                     validation_results["欄位: 緊急發電機設備編號 (規則: 只能輸入'英文'、'數字'、'-'、'_'、不可為空)"] = []
#                 validation_results["欄位: 緊急發電機設備編號 (規則: 只能輸入'英文'、'數字'、'-'、'_'、不可為空)"].append(error_message)
#                 return None
#             return device_id
#
#         def clean_position(row):
#             position = row['position']
#             if pd.isna(position):
#                 error_message = f"序號: {row.name + 1}，輸入值: {position}"
#                 if "欄位: 設置地點 (規則: 不可為空)" not in validation_results:
#                     validation_results["欄位: 設置地點 (規則: 不可為空)"] = []
#                 validation_results["欄位: 設置地點 (規則: 不可為空)"].append(error_message)
#                 return None
#             return position
#
#         def clean_capacity(row):
#             if row['device_capacity'] > 0 and isinstance(row['device_capacity'], (int, float)):
#                 # row['device_capacity'] = round(row['device_capacity'], 4)
#                 return row['device_capacity']
#             else:
#                 error_message = f"序號: {row.name + 1}，輸入值: {row['device_capacity']}"
#                 if '欄位: 緊急發電機容量 (規則: 輸入值須大於零、不可為空)' not in validation_results:
#                     validation_results['欄位: 緊急發電機容量 (規則: 輸入值須大於零、不可為空)'] = []
#                 validation_results['欄位: 緊急發電機容量 (規則: 輸入值須大於零、不可為空)'].append(error_message)
#                 return None
#
#         def clean_month(row):
#             months = ['january', 'february', 'march', 'april', 'may', 'june',
#                       'july', 'august', 'september', 'october', 'november', 'december']
#             for month in months:
#                 value = row[month]
#                 if isinstance(value, (int, float)) and value >= 0:
#                     row[month] = round(value, 4)
#                 else:
#                     conv_mont = find_key_by_value(rename[str(model_name)], month)
#                     error_message = f"序號: {row.name + 1}，輸入值: {value}"
#                     if f'欄位: {conv_mont} (規則: 輸入值須大於等於零、不可為空)' not in validation_results:
#                         validation_results[f'欄位: {conv_mont} (規則: 輸入值須大於等於零、不可為空)'] = []
#                     validation_results[f'欄位: {conv_mont} (規則: 輸入值須大於等於零、不可為空)'].append(error_message)
#                     row[month] = None
#             return row
#
#         # 驗證
#         validation_results = {}
#         df['device_id'] = df.apply(clean_device_id, axis=1)
#         df['position'] = df.apply(clean_position, axis=1)
#         df['device_capacity'] = df.apply(clean_capacity, axis=1)
#         df = df.apply(clean_month, axis=1)
#
#         if validation_results:
#             for i in validation_results:
#                 print(i)
#                 for j in validation_results[i]:
#                     print(j)
#             message['import_excel'] = validation_results
#         else:
#
#             # add necessary column to dataframe.
#             df['did'] = section_two.objects.get(did=did)
#             df['company_id'] = factory_id
#             df['years'] = years
#             df['estimate'] = False
#
#             # 大家都一樣
#             df_records = df.to_dict(orient='records')
#             model_instance = [model(**record) for record in df_records]
#             emergency_generators.objects.bulk_create(model_instance)
#             message = {'import_excel': '匯入成功!'}
#
#         return message
# 6666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666
#
#         df.rename(columns=dict(zip(column_names, columns)), inplace=True)
#
#                         # 將df轉換成dict
#                         data_dict = df.to_dict('records')
#
#                         # 將公司編號加入dict中
#                         for data in data_dict:
#                             data['company_id'] = factory_id
#
#                             for key, value in data.items():
#                                 # 判斷值是否為'是'或'否'
#                                 if value == '是':
#                                     data[key] = True
#                                 elif value == '否':
#                                     data[key] = False
#                                 elif pd.isna(value) or value == '':  # 檢查是否為 NaN 或空白儲存格
#                                     data[key] = None  # 將值設為 None，而不是儲存空白值
#
#                         # 將資料存入資料庫
#                         model_list = [globals()[table_name](**data) for data in data_dict]
#                         globals()[table_name].objects.bulk_create(model_list)
#
#         #
#         message = {'import_excel': '匯入成功!'}
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////
# factory_id = request.session.get('factory_id')
# generators = EmergencyGeneratorsResource(factory_id=factory_id)
#
# dataset = Dataset().load(df)
#
# # result = generators.import_data(dataset, dry_run=True, raise_errors=True, collect_failed_rows=False)
# # if not result.has_errors():
# #     result = generators.import_data(dataset, dry_run=False)
# #     # result = generators.import_data(df_to_csv, dry_run=False)
# #     message = {'import_excel': '匯入成功!'}
# # else:
# #     print('error\n', result.errors)
# try:
#     result = generators.import_data(dataset, dry_run=True, raise_errors=True, collect_failed_rows=False)
#     if not result.has_errors():
#         generators.import_data(dataset, dry_run=False)
#         # result = generators.import_data(df_to_csv, dry_run=False)
#         message = {'import_excel': '匯入成功!'}
#     else:
#         print('error\n', result.errors)
# except ValueError as e:
#     # print('e', type(e))
#     # print(str(e))
#     message = {'import_excel': str(e)}


# @csrf_exempt
# @require_http_methods(["POST"])
# def import_excel(request):
#     if request.method == 'POST':
#         # 取得設備編號、公司編號、檔案
#         did = request.session.get('dropdown_three')
#         factory_id = request.session.get('factory_id')
#         file = request.FILES.get('excel_file')
#
#         # 檢查檔案副檔名是否為Excel或CSV
#         file_type = os.path.splitext(file.name)[1]
#         if file_type in ['.xlsx', '.xls', '.csv']:
#             if file_type == '.csv':
#                 # 讀取Excel檔案
#                 df = pd.read_csv(file)
#                 # 將NaN值替換為空值
#                 df.fillna(value='', inplace=True)
#             else:
#                 # 讀取Excel檔案
#                 df = pd.read_excel(file)
#                 # 將NaN值替換為空值
#                 df.fillna(value='', inplace=True)
#         else:
#             response_data = {
#                 'success': False,
#                 'message': '檔案格式不正確，請選擇Excel或CSV檔案'
#             }
#             return JsonResponse(response_data)
#
#         # 取得目標資料表名稱
#         section = section_two.objects.get(did=did)
#         table_name = section.t_name
#         device_name = section.d_name
#
#         column_mapping = COLUMN_MAPPING[table_name]
#         column_names = column_mapping['column_names']
#         columns = column_mapping['columns']
#
#         # 檢查今年度是否已存在資料
#         this_year = datetime.now().year
#         if globals()[table_name].objects.filter(company_id=factory_id, years=this_year).exists():
#             response_data = {
#                 'success': False,
#                 'message': f'今年度已存在 {device_name} 的資料'
#             }
#             return JsonResponse(response_data)
#
#         # 寫入資料庫
#         try:
#             if table_name == 'employee_business_trip':
#                 # 轉換欄位名稱
#                 df.rename(columns={'年度': 'years', '出差單號': 'business_trip_number', '員工編號': 'employee_id', '部門': 'department', '姓名': 'employee_name', '出差地點': 'business_trip_location', '啟程日期': 'business_trip_date',
#                                    '出發地': 'departure', '交通工具': 'transportation', '距離': 'distance', '出差行程編號': 'trip_id', '備註欄': 'message_board'}, inplace=True)
#                 # 分離母子表資料
#                 mother_df = df.loc[:, ['years', 'business_trip_number', 'employee_id', 'department', 'employee_name', 'business_trip_location', 'business_trip_date', 'trip_id', 'message_board']]
#                 child_df = df.loc[:, ['trip_id', 'departure', 'transportation', 'distance']]
#
#                 # 將df轉換成dict
#                 mother_data_dict = mother_df.to_dict('records')
#                 child_data_dict = child_df.to_dict('records')
#
#                 trip_id_dict = {}
#                 new_business_trip_data = []
#                 new_trip_section_data = []
#
#                 # 將公司編號加入dict中
#                 for data in mother_data_dict:
#                     old_trip_id = data['trip_id']
#                     if old_trip_id not in trip_id_dict:
#                         data.pop('trip_id')
#                         data['company_id'] = factory_id
#                         new_mother_data = employee_business_trip.objects.create(**data)
#                         new_business_trip_data.append(new_mother_data)
#                         trip_id_dict[old_trip_id] = new_mother_data.id
#                     else:
#                         trip_id_dict[old_trip_id] = trip_id_dict[old_trip_id]
#
#                 for data in child_data_dict:
#                     old_trip_id = data['trip_id']
#                     new_trip_id = trip_id_dict[old_trip_id]
#                     data['trip_id'] = employee_business_trip.objects.get(id=new_trip_id)
#                     new_trip = trip_section(**data)
#                     new_trip_section_data.append(new_trip)
#
#                 # 儲存新的資料到資料庫中
#                 trip_section.objects.bulk_create(new_trip_section_data)
#
#                 response_data = {
#                     'success': True,
#                     'message': '匯入Excel成功'
#                 }
#                 return JsonResponse(response_data)
#
#             elif table_name == 'employee_commute':
#                 # 轉換欄位名稱
#                 df.rename(columns={'年度': 'years', '員工編號': 'employee_id', '部門': 'department', '姓名': 'employee_name', '居住城市': 'city', '鄉鎮市區': 'township', '行政區公家機關地址': 'address',
#                                    '至公司距離(km)': 'commute_distance', '年工作天數': 'work_days', '交通工具': 'transportation', '員工通勤編號': 'commute_id', '備註欄': 'message_board'}, inplace=True)
#
#                 # 分離母子表資料
#
#                 mother_df = df.loc[:, ['years', 'employee_id', 'department', 'employee_name', 'city', 'township', 'address', 'commute_distance', 'work_days', 'commute_id', 'message_board']]
#                 child_df = df.loc[:, ['commute_id', 'transportation']]
#
#                 # 將df轉換成dict
#                 mother_data_dict = mother_df.to_dict('records')
#                 child_data_dict = child_df.to_dict('records')
#
#                 commute_id_dict = {}
#                 new_commute_data = []
#                 new_transportation_data = []
#
#                 # 將公司編號加入dict中
#                 for data in mother_data_dict:
#                     old_commute_id = data['commute_id']
#                     if old_commute_id not in commute_id_dict:
#                         data.pop('commute_id')
#                         data['company_id'] = factory_id
#                         new_mother_data = employee_commute.objects.create(**data)
#                         new_commute_data.append(new_mother_data)
#                         commute_id_dict[old_commute_id] = new_mother_data.id
#                     else:
#                         commute_id_dict[old_commute_id] = commute_id_dict[old_commute_id]
#
#                 for data in child_data_dict:
#                     old_commute_id = data['commute_id']
#                     new_commute_id = commute_id_dict[old_commute_id]
#                     data['commute_id'] = new_commute_id
#                     new_transportation = transportation_way(**data)
#                     new_transportation_data.append(new_transportation)
#
#                 # 儲存新的資料到資料庫中
#                 transportation_way.objects.bulk_create(new_transportation_data)
#
#                 response_data = {
#                     'success': True,
#                     'message': '匯入Excel成功'
#                 }
#                 return JsonResponse(response_data)
#
#             else:
#                 # 將中文列名轉換為英文列名
#                 df.rename(columns=dict(zip(column_names, columns)), inplace=True)
#
#                 # 將df轉換成dict
#                 data_dict = df.to_dict('records')
#
#                 # 將公司編號加入dict中
#                 for data in data_dict:
#                     data['company_id'] = factory_id
#
#                     for key, value in data.items():
#                         # 判斷值是否為'是'或'否'
#                         if value == '是':
#                             data[key] = True
#                         elif value == '否':
#                             data[key] = False
#                         elif pd.isna(value) or value == '':  # 檢查是否為 NaN 或空白儲存格
#                             data[key] = None  # 將值設為 None，而不是儲存空白值
#
#                 # 將資料存入資料庫
#                 model_list = [globals()[table_name](**data) for data in data_dict]
#                 globals()[table_name].objects.bulk_create(model_list)
#
#                 response_data = {
#                     'success': True,
#                     'message': '匯入Excel成功'
#                 }
#                 return JsonResponse(response_data)
#
#         # 表示檔案格式不正確
#         except pd.errors.ParserError:
#             response_data = {
#                 'success': False,
#                 'message': '匯入Excel失敗，請檢查欄位格式是否正確。'
#             }
#             return JsonResponse(response_data)
#
#         except ValueError as error:
#             print('匯入Excel失敗，錯誤原因：', error)
#             response_data = {
#                 'success': False,
#                 'message': '匯入Excel失敗，請檢是否有選取設備。'
#             }
#             return JsonResponse(response_data, status=400)
#
#         except TypeError as error:
#             print('匯入Excel失敗，錯誤原因：', error)
#             response_data = {
#                 'success': False,
#                 'message': '匯入Excel失敗，請檢查選擇的檔案是否正確。'
#             }
#             return JsonResponse(response_data)
#
#         except KeyError as error:
#             print('匯入Excel失敗，錯誤原因：', error)
#             response_data = {
#                 'success': False,
#                 'message': f'匯入Excel失敗，請檢查欄位名稱是否正確。'
#             }
#             return JsonResponse(response_data)
#
#         # 其他可能性錯誤
#         except Exception as error:
#             print('匯入Excel失敗，錯誤原因：', error)
#             response_data = {
#                 'success': False,
#                 'message': '匯入Excel失敗，錯誤原因：' + str(error)
#             }
#             return JsonResponse(response_data)
