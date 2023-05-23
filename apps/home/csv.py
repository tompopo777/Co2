import io
import os
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from urllib import parse
from django.contrib import messages
from openpyxl import load_workbook
from .views import current_user_group_id

from .models import *

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
        'columns': ['years', 'device_name', 'device_id', 'fuel_type', 'fuel_january', 'fuel_february', 'fuel_march',
                    'fuel_april', 'fuel_may', 'fuel_june', 'fuel_july', 'fuel_august', 'fuel_september', 'fuel_october',
                    'fuel_november', 'fuel_december', 'heat_january', 'heat_february', 'heat_march', 'heat_april', 'heat_may',
                    'heat_june', 'heat_july', 'heat_august', 'heat_september', 'heat_october', 'heat_november', 'heat_december', 'message_board'],
        'column_names': ['年度', '名稱', '編號', '燃料種類', '一月 使用量', '二月 使用量', '三月 使用量', '四月 使用量', '五月 使用量', '六月 使用量',
                         '七月 使用量', '八月 使用量', '九月 使用量', '十月 使用量', '十一月 使用量', '十二月 使用量',
                         '一月 熱值(Kcal/kg)', '二月 熱值(Kcal/kg)', '三月 熱值(Kcal/kg)', '四月 熱值(Kcal/kg)', '五月 熱值(Kcal/kg)', '六月 熱值(Kcal/kg)',
                         '七月 熱值(Kcal/kg)', '八月 熱值(Kcal/kg)', '九月 熱值(Kcal/kg)', '十月 熱值(Kcal/kg)', '十一月 熱值(Kcal/kg)', '十二月 熱值(Kcal/kg)', '備註欄'],
        'prefix': '類別一_'
    },
    'official_car': {
        'columns': ['years', 'vehicle_type', 'device_id', 'fuel_type', 'department', 'metering_method',
                    'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
                    'september', 'october', 'november', 'december',
                    'urea_january', 'urea_february', 'urea_march', 'urea_april', 'urea_may', 'urea_june', 'urea_july',
                    'urea_august', 'urea_september', 'urea_october', 'urea_november', 'urea_december'],
        'column_names': ['年度', '類別', '編號', '燃料種類', '所屬單位', '計程方式',
                         '耗用量 一月', '耗用量 二月', '耗用量 三月', '耗用量 四月', '耗用量 五月', '耗用量 六月',
                         '耗用量 七月', '耗用量 八月', '耗用量 九月', '耗用量 十月', '耗用量 十一月', '耗用量 十二月',
                         '尿素 一月', '尿素 二月', '尿素 三月', '尿素 四月', '尿素 五月', '尿素 六月',
                         '尿素 七月', '尿素 八月', '尿素 九月', '尿素 十月', '尿素 十一月', '尿素 十二月'],
        'prefix': '類別一_'
    },
    'material': {
        'columns': ['years', 'material_id', 'material_type', 'material_name', 'chemical', 'process_add_name', 'chemical_name', 'chemical_formula',
                    'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'message_board'],
        'column_names': ['年度', '原物料號', '原/物料', '名稱', '是否為化學品', '化學品名稱', '化學品名', '化學式', '一月', '二月', '三月', '四月', '五月',
                         '六月', '七月', '八月', '九月', '十月', '十一月', '十二月', '備註欄'],
        'prefix': '類別一_'
    },
    'process': {
        'columns': ['years', 'process_stage', 'material_id', 'process_add_name', 'carbon_content', 'burn', 'VOCs',
                    'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'message_board', 'unit'],
        'column_names': ['年度', '製程階段', '料號', '製程添加名稱', '含碳量(%)', '是否燃燒', 'VOCs',
                         '一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月', '備註欄', '使用量單位'],
        'prefix': '類別一__'
    },
    'refrigerator': {
        'columns': ['years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                    'filling_volume', 'refrigerant_type', 'filling_fix_volume', 'effusion_rate', 'message_board'],
        'column_names': ['年度', '編號', '名稱', '品牌', '型號', '位置', '購買年份', '規格填充量', '冷媒類型', '維修填充量(kg)', '逸散率(%)', '備註欄'],
        'prefix': '類別一__'
    },
    'airconditioner': {
        'columns': ['years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                    'filling_volume', 'refrigerant_type', 'filling_fix_volume', 'effusion_rate', 'message_board'],
        'column_names': ['年度', '編號', '名稱', '品牌', '型號', '位置', '購買年份', '規格填充量', '冷媒類型', '維修填充量(kg)', '逸散率(%)', '備註欄'],
        'prefix': '類別一__'
    },
    'vehicle': {
        'columns': ['years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                    'filling_volume', 'refrigerant_type', 'filling_fix_volume', 'effusion_rate', 'message_board'],
        'column_names': ['年度', '編號', '名稱', '品牌', '型號', '位置', '購買年份', '規格填充量', '冷媒類型', '維修填充量(kg)', '逸散率(%)', '備註欄'],
        'prefix': '類別一__'
    },
    'water_dispenser': {
        'columns': ['years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                    'filling_volume', 'refrigerant_type', 'filling_fix_volume', 'effusion_rate', 'message_board'],
        'column_names': ['年度', '編號', '名稱', '品牌', '型號', '位置', '購買年份', '規格填充量', '冷媒類型', '維修填充量(kg)', '逸散率(%)', '備註欄'],
        'prefix': '類別一__'
    },
    'ice_water_dispenser': {
        'columns': ['years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                    'filling_volume', 'refrigerant_type', 'filling_fix_volume', 'effusion_rate', 'message_board'],
        'column_names': ['年度', '編號', '名稱', '品牌', '型號', '位置', '購買年份', '規格填充量', '冷媒類型', '維修填充量(kg)', '逸散率(%)', '備註欄'],
        'prefix': '類別一__'
    },
    'ice_maker': {
        'columns': ['years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                    'filling_volume', 'refrigerant_type', 'filling_fix_volume', 'effusion_rate', 'message_board'],
        'column_names': ['年度', '編號', '名稱', '品牌', '型號', '位置', '購買年份', '規格填充量', '冷媒類型', '維修填充量(kg)', '逸散率(%)', '備註欄'],
        'prefix': '類別一__'
    },
    'other_device': {
        'columns': ['years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                    'filling_volume', 'refrigerant_type', 'filling_fix_volume', 'effusion_rate', 'message_board'],
        'column_names': ['年度', '編號', '名稱', '品牌', '型號', '位置', '購買年份', '規格填充量', '冷媒類型', '維修填充量(kg)', '逸散率(%)', '備註欄'],
        'prefix': '類別一__'
    },
    'extinguisher': {
        'columns': ['years', 'device_id', 'extinguisher_vendor', 'extinguisher_type', 'position', 'inventory',
                    'chemical_weight', 'using_amount', 'monthly', 'replace_filling_amount', 'replace_filling_date', 'message_board'],
        'column_names': ['年度', '設備編號', '廠商', '類型', '擺放位置(廠別)', '庫存量', '藥劑重量(單位:kg)', '使用量數量', '使用月份', '更換/填充量', '更換/填充日期', '備註欄'],
        'prefix': '類別一_'
    },
    'personnel_inventory': {
        'columns': ['years', 'classification', 'WKhours_january', 'WKhours_february', 'WKhours_march', 'WKhours_april', 'WKhours_may', 'WKhours_june',
                    'WKhours_july', 'WKhours_august', 'WKhours_september', 'WKhours_october', 'WKhours_november', 'WKhours_december',
                    'WKnum_january', 'WKnum_february', 'WKnum_march', 'WKnum_april', 'WKnum_may', 'WKnum_june', 'WKnum_july',
                    'WKnum_august', 'WKnum_september', 'WKnum_october', 'WKnum_november', 'WKnum_december', 'message_board'],
        'column_names': ['年度', '類型', '時數 一月', '時數 二月', '時數 三月', '時數 四月', '時數 五月', '時數 六月',
                         '時數 七月', '時數 八月', '時數 九月', '時數 十月', '時數 十一月', '時數 十二月',
                         '人數 一月', '人數 二月', '人數 三月', '人數 四月', '人數 五月', '人數 六月',
                         '人數 七月', '人數 八月', '人數 九月', '人數 十月', '人數 十一月', '人數 十二月', '備註欄'],
        'prefix': '類別一_'
    },
    'employee': {
        'columns': ['years', 'career', 'employeeNum_january', 'employeeNum_february', 'employeeNum_march', 'employeeNum_april', 'employeeNum_may',
                    'employeeNum_june', 'employeeNum_july', 'employeeNum_august', 'employeeNum_september', 'employeeNum_october', 'employeeNum_november',
                    'employeeNum_december', 'WKdays_january', 'WKdays_february', 'WKdays_march', 'WKdays_april', 'WKdays_may', 'WKdays_june',
                    'WKdays_july', 'WKdays_august', 'WKdays_september', 'WKdays_october', 'WKdays_november', 'WKdays_december',
                    'WKhours_january', 'WKhours_february', 'WKhours_march', 'WKhours_april', 'WKhours_may', 'WKhours_june', 'WKhours_july',
                    'WKhours_august', 'WKhours_september', 'WKhours_october', 'WKhours_november', 'WKhours_december', 'message_board'],
        'column_names': ['年度', '人員類別',
                         '人數 一月', '人數 二月', '人數 三月', '人數 四月', '人數 五月', '人數 六月',
                         '人數 七月', '人數 八月', '人數 九月', '人數 十月', '人數 十一月', '人數 十二月',
                         '工作天數 一月', '工作天數 二月', '工作天數 三月', '工作天數 四月', '工作天數 五月', '工作天數 六月',
                         '工作天數 七月', '工作天數 八月', '工作天數 九月', '工作天數 十月', '工作天數 十一月', '工作天數 十二月',
                         '時數 一月', '時數 二月', '時數 三月', '時數 四月', '時數 五月', '時數 六月',
                         '時數 七月', '時數 八月', '時數 九月', '時數 十月', '時數 十一月', '時數 十二月', '備註欄'],
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
    'waste': {
        'columns': ['years', 'waste_name', 'waste_weigh', 'waste_date', 'waste_location', 'waste_disposal', 'waste_disposal_vendor',
                    'transport_type', 'transport_fuel', 'transport_distance', 'message_board'],
        'column_names': ['年度', '名稱', '重量(噸)', '運送時間', '處置地點', '處理方式', '處理廠商名稱', '運輸方式', '運輸燃料', '運輸距離(km)', '備註欄'],
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
@require_http_methods(["POST"])
def export_excel(request):
    if request.method == "POST":
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

        # 根據所需欄位清單查詢資料
        data = globals()[table_name].objects.all().filter(company_id=factory_id, years=year).values(*columns)

        # 將查詢結果轉換為DataFrame
        df = pd.DataFrame(list(data))

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


# 下載公版
@csrf_exempt
@require_http_methods(["POST"])
def public_version(request):
    if request.method == 'POST':
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



@csrf_exempt
@require_http_methods(["POST"])
def import_excel(request):
    if request.method == 'POST':
        # 取得設備編號、公司編號、檔案
        did = request.session.get('dropdown_three')
        factory_id = request.session.get('factory_id')
        file = request.FILES.get('excel_file')

        # 檢查檔案副檔名是否為Excel或CSV
        file_type = os.path.splitext(file.name)[1]
        if file_type in ['.xlsx', '.xls', '.csv']:
            if file_type == '.csv':
                # 讀取Excel檔案
                df = pd.read_csv(file)
                # 將NaN值替換為空值
                df.fillna(value='', inplace=True)
            else:
                # 讀取Excel檔案
                df = pd.read_excel(file)
                # 將NaN值替換為空值
                df.fillna(value='', inplace=True)
        else:
            response_data = {
                'success': False,
                'message': '檔案格式不正確，請選擇Excel或CSV檔案'
            }
            return JsonResponse(response_data)

        # 取得目標資料表名稱
        section = section_two.objects.get(did=did)
        table_name = section.t_name

        column_mapping = COLUMN_MAPPING[table_name]
        column_names = column_mapping['column_names']
        columns = column_mapping['columns']

        # 寫入資料庫
        try:
            if table_name == 'employee_business_trip':
                # 轉換欄位名稱
                df.rename(columns={'年度': 'years', '出差單號': 'business_trip_number', '員工編號': 'employee_id', '部門': 'department', '姓名': 'employee_name', '出差地點': 'business_trip_location', '啟程日期': 'business_trip_date',
                                   '出發地': 'departure', '交通工具': 'transportation', '距離': 'distance', '出差行程編號': 'trip_id', '備註欄': 'message_board'}, inplace=True)
                # 分離母子表資料
                mother_df = df.loc[:, ['years', 'business_trip_number', 'employee_id', 'department', 'employee_name', 'business_trip_location', 'business_trip_date', 'trip_id', 'message_board']]
                child_df = df.loc[:, ['trip_id', 'departure', 'transportation', 'distance']]

                # 將df轉換成dict
                mother_data_dict = mother_df.to_dict('records')
                child_data_dict = child_df.to_dict('records')

                trip_id_dict = {}
                new_business_trip_data = []
                new_trip_section_data = []

                # 將公司編號加入dict中
                for data in mother_data_dict:
                    old_trip_id = data['trip_id']
                    if old_trip_id not in trip_id_dict:
                        data.pop('trip_id')
                        data['company_id'] = factory_id
                        new_mother_data = employee_business_trip.objects.create(**data)
                        new_business_trip_data.append(new_mother_data)
                        trip_id_dict[old_trip_id] = new_mother_data.id
                    else:
                        trip_id_dict[old_trip_id] = trip_id_dict[old_trip_id]

                for data in child_data_dict:
                    old_trip_id = data['trip_id']
                    new_trip_id = trip_id_dict[old_trip_id]
                    data['trip_id'] = employee_business_trip.objects.get(id=new_trip_id)
                    new_trip = trip_section(**data)
                    new_trip_section_data.append(new_trip)

                # 儲存新的資料到資料庫中
                trip_section.objects.bulk_create(new_trip_section_data)

                response_data = {
                    'success': True,
                    'message': '匯入Excel成功'
                }
                return JsonResponse(response_data)

            elif table_name == 'employee_commute':
                # 轉換欄位名稱
                df.rename(columns={'年度': 'years', '員工編號': 'employee_id', '部門': 'department', '姓名': 'employee_name', '居住城市': 'city', '鄉鎮市區': 'township', '行政區公家機關地址': 'address',
                                   '至公司距離(km)': 'commute_distance', '年工作天數': 'work_days', '交通工具': 'transportation', '員工通勤編號': 'commute_id', '備註欄': 'message_board'}, inplace=True)

                # 分離母子表資料

                mother_df = df.loc[:, ['years', 'employee_id', 'department', 'employee_name', 'city', 'township', 'address', 'commute_distance', 'work_days', 'commute_id', 'message_board']]
                child_df = df.loc[:, ['commute_id', 'transportation']]

                # 將df轉換成dict
                mother_data_dict = mother_df.to_dict('records')
                child_data_dict = child_df.to_dict('records')

                commute_id_dict = {}
                new_commute_data = []
                new_transportation_data = []

                # 將公司編號加入dict中
                for data in mother_data_dict:
                    old_commute_id = data['commute_id']
                    if old_commute_id not in commute_id_dict:
                        data.pop('commute_id')
                        data['company_id'] = factory_id
                        new_mother_data = employee_commute.objects.create(**data)
                        new_commute_data.append(new_mother_data)
                        commute_id_dict[old_commute_id] = new_mother_data.id
                    else:
                        commute_id_dict[old_commute_id] = commute_id_dict[old_commute_id]

                for data in child_data_dict:
                    old_commute_id = data['commute_id']
                    new_commute_id = commute_id_dict[old_commute_id]
                    data['commute_id'] = new_commute_id
                    new_transportation = transportation_way(**data)
                    new_transportation_data.append(new_transportation)

                # 儲存新的資料到資料庫中
                transportation_way.objects.bulk_create(new_transportation_data)

                response_data = {
                    'success': True,
                    'message': '匯入Excel成功'
                }
                return JsonResponse(response_data)

            else:
                # 將中文列名轉換為英文列名
                df.rename(columns=dict(zip(column_names, columns)), inplace=True)

                # 將df轉換成dict
                data_dict = df.to_dict('records')

                # 將公司編號加入dict中
                for data in data_dict:
                    data['company_id'] = factory_id

                    # # 判斷 estimate 欄位的值並轉換為布尔值
                    # if data['estimate'] == '是':
                    #     data['estimate'] = True
                    # else:
                    #     data['estimate'] = False
                    for key, value in data.items():
                        # 判斷值是否為'是'或'否'
                        if value == '是':
                            data[key] = True
                        elif value == '否':
                            data[key] = False

                # 將資料存入資料庫
                model_list = [globals()[table_name](**data) for data in data_dict]
                globals()[table_name].objects.bulk_create(model_list)

                response_data = {
                    'success': True,
                    'message': '匯入Excel成功'
                }
                return JsonResponse(response_data)

        # 表示檔案格式不正確
        except pd.errors.ParserError:
            response_data = {
                'success': False,
                'message': '匯入Excel失敗，請檢查欄位格式是否正確。'
            }
            return JsonResponse(response_data)

        except ValueError as error:
            print('匯入Excel失敗，錯誤原因：', error)
            response_data = {
                'success': False,
                'message': '匯入Excel失敗，請檢是否有選取設備。'
            }
            return JsonResponse(response_data, status=400)

        except TypeError as error:
            print('匯入Excel失敗，錯誤原因：', error)
            response_data = {
                'success': False,
                'message': '匯入Excel失敗，請檢查選擇的檔案是否正確。'
            }
            return JsonResponse(response_data)

        except KeyError as error:
            print('匯入Excel失敗，錯誤原因：', error)
            response_data = {
                'success': False,
                'message': f'匯入Excel失敗，請檢查欄位名稱是否正確。'
            }
            return JsonResponse(response_data)

        # 其他可能性錯誤
        except Exception as error:
            print('匯入Excel失敗，錯誤原因：', error)
            response_data = {
                'success': False,
                'message': '匯入Excel失敗，錯誤原因：' + str(error)
            }
            return JsonResponse(response_data)
