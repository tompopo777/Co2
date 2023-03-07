import io
import pandas as pd
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from urllib import parse
from django.contrib import messages
from openpyxl import load_workbook

from .models import *


COLUMN_MAPPING = {
    'emergency_generators': {
        'columns': ['years', 'device_id', 'device_capacity', 'position', 'department',
                    'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
                    'september', 'october', 'november', 'december', 'message_board'],  # 欄位清單1
        'column_names': ['ID', '年度', '設備編號', '容量(𝓁)', '地點', '部門', '一月', '二月', '三月', 
                         '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月', '備註欄'],  # 欄位中文名稱1
        'prefix': '類別一_'
    },
    'combustion_equipment': {
        'columns': ["years", "device_name", "device_id", "fuel_type", "fuel_january", "fuel_february", "fuel_march",
                    "fuel_april", "fuel_may", "fuel_june",  "fuel_july", "fuel_august", "fuel_september", "fuel_october",
                    "fuel_november", "fuel_december", "heat_january", "heat_february", "heat_march", "heat_april", "heat_may",
                    "heat_june", "heat_july", "heat_august", "heat_september", "heat_october", "heat_november", "heat_december"],
        'column_names': ['中文名稱4', '中文名稱5', '中文名稱6'],
        'prefix': '類別一_'
    },
    'official_car': {
        'columns': ['col4', 'col5', 'col6'],
        'column_names': ['中文名稱4', '中文名稱5', '中文名稱6'],
        'prefix': '類別一_'
    },
    'material': {
        'columns': ["id", "years", "material_id", "material_type", "material_name", "process_add_name", "chemical_name",
                    "chemical_formula", "january", "february", "march", "april", "may", "june", "july", "august",
                    "september", "october", "november", "december"],
        'column_names': ['中文名稱4', '中文名稱5', '中文名稱6'],
        'prefix': '類別一_'
    },
    'process': {
        'columns': ["id", "years", "process_stage", "material_id", "process_add_name", "chemical_name", "chemical_formula",
                    "CAS_NO", "burn", "VOCs", "january", "february", "march", "april", "may", "june", "july", "august",
                    "september", "october", "november", "december"],
        'column_names': ['中文名稱4', '中文名稱5', '中文名稱6'],
        'prefix': '類別一__'
    },
    'refrigerator': {
        'columns': ["years", "device_id", "device_name", "brand_name", "model_type", "position", "filling_volume",
                    "refrigerant_type", "filling_fix_volume", "effusion_rate"],
        'column_names': ['年度', '編號', '名稱', '品牌', '型號', '位置', '規格填充量', '冷媒類型', '維修填充量(kg)', '逸散率(%)'],
        'prefix': '類別一__'
    },
    'airconditioner': {
        'columns': ['years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'filling_volume',
                    'refrigerant_type', 'filling_fix_volume', 'effusion_rate'],
        'column_names': ['年度', '編號', '名稱', '品牌', '型號', '位置', '規格填充量', '冷媒類型', '維修填充量(kg)', '逸散率(%)'],
        'prefix': '類別一__'
    },
    'vehicle': {
        'columns': ['years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'filling_volume',
                    'refrigerant_type', 'filling_fix_volume', 'effusion_rate'],
        'column_names': ['年度', '編號', '名稱', '品牌', '型號', '位置', '規格填充量', '冷媒類型', '維修填充量(kg)', '逸散率(%)'],
        'prefix': '類別一_'
    },
    'water_dispenser': {
        'columns': ['years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'filling_volume',
                    'refrigerant_type', 'filling_fix_volume', 'effusion_rate'],
        'column_names': ['年度', '編號', '名稱', '品牌', '型號', '位置', '規格填充量', '冷媒類型', '維修填充量(kg)', '逸散率(%)'],
        'prefix': '類別一_'
    },
    'ice_water_dispenser': {
        'columns': ['years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'filling_volume',
                    'refrigerant_type', 'filling_fix_volume', 'effusion_rate'],
        'column_names': ['年度', '編號', '名稱', '品牌', '型號', '位置', '規格填充量', '冷媒類型', '維修填充量(kg)', '逸散率(%)'],
        'prefix': '類別一_'
    },
    'ice_maker': {
        'columns': ['years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'filling_volume',
                    'refrigerant_type', 'filling_fix_volume', 'effusion_rate'],
        'column_names': ['年度', '編號', '名稱', '品牌', '型號', '位置', '規格填充量', '冷媒類型', '維修填充量(kg)', '逸散率(%)'],
        'prefix': '類別一_'
    },
    'other_device': {
        'columns': ['years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'filling_volume',
                    'refrigerant_type', 'filling_fix_volume', 'effusion_rate'],
        'column_names': ['年度', '編號', '名稱', '品牌', '型號', '位置', '規格填充量', '冷媒類型', '維修填充量(kg)', '逸散率(%)'],
        'prefix': '類別一_'
    },
    'extinguisher': {
        'columns': ["business_trip_number", "employee_id", "department", "employee_name", "business_trip_location",
                    "business_trip_date"],
        'column_names': ['出差單號', '員工編號', '部門', '姓名', '出差地點', '啟程日期'],
        'prefix': '類別一_'
    },
    'personnel_inventory': {
        'columns': ["business_trip_number", "employee_id", "department", "employee_name", "business_trip_location",
                    "business_trip_date"],
        'column_names': ['出差單號', '員工編號', '部門', '姓名', '出差地點', '啟程日期'],
        'prefix': '類別一_'
    },
    'employee': {
        'columns': ["business_trip_number", "employee_id", "department", "employee_name", "business_trip_location",
                    "business_trip_date"],
        'column_names': ['出差單號', '員工編號', '部門', '姓名', '出差地點', '啟程日期'],
        'prefix': '類別一_'
    },
    'waste_water': {
        'columns': ["business_trip_number", "employee_id", "department", "employee_name", "business_trip_location",
                    "business_trip_date"],
        'column_names': ['出差單號', '員工編號', '部門', '姓名', '出差地點', '啟程日期'],
        'prefix': '類別一_'
    },
    'waste_sludge': {
        'columns': ["business_trip_number", "employee_id", "department", "employee_name", "business_trip_location",
                    "business_trip_date"],
        'column_names': ['出差單號', '員工編號', '部門', '姓名', '出差地點', '啟程日期'],
        'prefix': '類別一_'
    },
    'solvent_aerosol_emission_sources': {
        'columns': ["business_trip_number", "employee_id", "department", "employee_name", "business_trip_location",
                    "business_trip_date"],
        'column_names': ['出差單號', '員工編號', '部門', '姓名', '出差地點', '啟程日期'],
        'prefix': '類別一_'
    },
    'VOCs_one': {
        'columns': ["business_trip_number", "employee_id", "department", "employee_name", "business_trip_location",
                    "business_trip_date"],
        'column_names': ['出差單號', '員工編號', '部門', '姓名', '出差地點', '啟程日期'],
        'prefix': '類別一_'
    },
    'VOCs_two': {
        'columns': ["business_trip_number", "employee_id", "department", "employee_name", "business_trip_location",
                    "business_trip_date"],
        'column_names': ['出差單號', '員工編號', '部門', '姓名', '出差地點', '啟程日期'],
        'prefix': '類別一_'
    },
    'electricity': {
        'columns': ["business_trip_number", "employee_id", "department", "employee_name", "business_trip_location",
                    "business_trip_date"],
        'column_names': ['出差單號', '員工編號', '部門', '姓名', '出差地點', '啟程日期'],
        'prefix': '類別二_'
    },
    'upstream_transportation': {
        'columns': ["business_trip_number", "employee_id", "department", "employee_name", "business_trip_location",
                    "business_trip_date"],
        'column_names': ['出差單號', '員工編號', '部門', '姓名', '出差地點', '啟程日期'],
        'prefix': '類別三_'
    },
    'downstream_transportation': {
        'columns': ["business_trip_number", "employee_id", "department", "employee_name", "business_trip_location",
                    "business_trip_date"],
        'column_names': ['出差單號', '員工編號', '部門', '姓名', '出差地點', '啟程日期'],
        'prefix': '類別三_'
    },
    'waste': {
        'columns': ["business_trip_number", "employee_id", "department", "employee_name", "business_trip_location",
                    "business_trip_date"],
        'column_names': ['出差單號', '員工編號', '部門', '姓名', '出差地點', '啟程日期'],
        'prefix': '類別四_'
    },
    'pipe_wastewater': {
        'columns': ["business_trip_number", "employee_id", "department", "employee_name", "business_trip_location",
                    "business_trip_date"],
        'column_names': ['出差單號', '員工編號', '部門', '姓名', '出差地點', '啟程日期'],
        'prefix': '類別四_'
    },
    'purchase_material': {
        'columns': ["business_trip_number", "employee_id", "department", "employee_name", "business_trip_location",
                    "business_trip_date"],
        'column_names': ['出差單號', '員工編號', '部門', '姓名', '出差地點', '啟程日期'],
        'prefix': '類別四_'
    },
    'product_indirect_emissions': {
        'columns': ["business_trip_number", "employee_id", "department", "employee_name", "business_trip_location",
                    "business_trip_date"],
        'column_names': ['出差單號', '員工編號', '部門', '姓名', '出差地點', '啟程日期'],
        'prefix': '類別五_'
    },
    'employee_business_trip': {
        'columns': ["id", "business_trip_number", "employee_id", "department", "employee_name", "business_trip_location", "business_trip_date"],
        'column_names': ['出差行程編號', '出差單號', '員工編號', '部門', '姓名', '出差地點', '啟程日期'],
        'prefix': '類別三_'
    },
    'trip_section': {
        'columns': ["departure", "transportation", "distance", "trip_id"],
        'column_names': ['出發地', '交通工具', '距離', '出差行程編號'],
    },
    'employee_commute': {
        'columns': ["id", "years", "employee_id", "department", "employee_name", "city", "township", "address", "commute_distance", "work_days"],
        'column_names': ['員工通勤編號', '年度', '員工編號', '部門', '姓名', '居住城市', '鄉鎮市區', '行政區公家機關地址', '至公司距離(km)', '年工作天數'],
        'prefix': '類別三_'
    },
    'transportation_way': {
        'columns': ["transportation", "commute"],
        'column_names': ['交通工具', '員工通勤編號'],
    },


    # ... 其他資料庫表格和欄位清單映射
}


# 匯出功能
@csrf_exempt
@require_http_methods(["POST"])
def export_excel(request):
    if request.method == "POST":
        did = request.POST.get('did')
        print(did)
        excel_did = section_two.objects.filter(did__exact=int(did))

        # 取得欄位清單和欄位中文名稱
        table_name = excel_did[0].t_name
        column_mapping = COLUMN_MAPPING[table_name]
        prefix = column_mapping.get('prefix', '')
        columns = column_mapping['columns']
        column_names = column_mapping['column_names']

        # 根據所需欄位清單查詢資料
        data = globals()[table_name].objects.all().values(*columns)

        # 將查詢結果轉換為DataFrame
        df = pd.DataFrame(list(data))

        # 將欄位名稱改成中文
        df.columns = column_names

        if table_name == 'employee_business_trip':
            # 取得母表和子表的欄位資訊
            mother_columns = COLUMN_MAPPING['employee_business_trip']['columns']
            mother_column_names = COLUMN_MAPPING['employee_business_trip']['column_names']
            child_columns = COLUMN_MAPPING['trip_section']['columns']
            child_column_names = COLUMN_MAPPING['trip_section']['column_names']

            # 取得母表和子表的資料
            mother_data = employee_business_trip.objects.all().values(*mother_columns)
            child_data = trip_section.objects.all().values(*child_columns)

            # 將母表和子表的資料轉換為 DataFrame
            mother_df = pd.DataFrame(list(mother_data))
            child_df = pd.DataFrame(list(child_data))

            # 將欄位名稱改成中文
            mother_df.columns = mother_column_names
            child_df.columns = child_column_names

            # 將子表的資料加入到母表的資料中
            df = pd.merge(mother_df, child_df[['出發地', '交通工具', '距離', '出差行程編號']], on='出差行程編號', how='left')

            # 將子表的欄位名稱加入到匯出的資料中
            column_names = ['出差行程編號', '出差單號', '員工編號', '部門', '姓名', '出差地點', '啟程日期']
            column_names.extend(['出發地', '交通工具', '距離'])

        elif table_name == 'employee_commute':
            # 取得母表和子表的欄位資訊
            mother_columns = COLUMN_MAPPING['employee_commute']['columns']
            mother_column_names = COLUMN_MAPPING['employee_commute']['column_names']
            child_columns = COLUMN_MAPPING['transportation_way']['columns']
            child_column_names = COLUMN_MAPPING['transportation_way']['column_names']

            # 取得母表和子表的資料
            mother_data = employee_commute.objects.all().values(*mother_columns)
            child_data = transportation_way.objects.all().values(*child_columns)

            # 將母表和子表的資料轉換為 DataFrame
            mother_df = pd.DataFrame(list(mother_data))
            child_df = pd.DataFrame(list(child_data))

            # 將欄位名稱改成中文
            mother_df.columns = mother_column_names
            child_df.columns = child_column_names

            # 將子表的資料加入到母表的資料中
            df = pd.merge(mother_df, child_df[['交通工具', '員工通勤編號']], on='員工通勤編號', how='left')

            # 將子表的欄位名稱加入到匯出的資料中
            column_names = ['員工通勤編號', '年度', '員工編號', '部門', '姓名', '居住城市', '鄉鎮市區', '行政區公家機關地址', '至公司距離(km)', '年工作天數']
            column_names.extend(['交通工具'])

        # 將欄位名稱改成中文
        df.columns = column_names

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


# 匯入功能
@csrf_exempt
@require_http_methods(["POST"])
def import_excel(request):
    if request.method == 'POST':
        try:
            did = request.POST.get('did')
            file = request.FILES['excel_file']

            # 解析Excel檔案
            wb = load_workbook(file, data_only=True)
            sheet = wb.active

            # 取得目標資料表名稱
            section = section_two.objects.get(did=did)
            table_name = section.t_name

            # 取得目標資料表的中英文欄位名稱對應
            column_mapping = COLUMN_MAPPING[table_name]
            column_names = column_mapping['column_names']
            columns = column_mapping['columns']

            # 讀取Excel中的資料，並存入資料庫中
            for row in sheet.iter_rows(min_row=2):
                data = {}
                for i, cell in enumerate(row):
                    # 將中文欄位名稱轉換為英文欄位名稱
                    column_name = column_names[i]
                    column = columns[i]
                    if column == "id":
                        continue  # 如果欄位是id，則略過不處理
                    data[column] = cell.value

                # 將資料存入資料庫
                your_model_instance = globals()[table_name](**data)
                your_model_instance.save()

            messages.success(request, '匯入Excel成功')
            return HttpResponse('OK')
        except Exception as e:
            messages.error(request, '匯入Excel失敗')
            return HttpResponse(str(e), status=400)
