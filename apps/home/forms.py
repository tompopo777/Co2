import decimal
import re

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *
from decimal import *
from django.forms import inlineformset_factory

# 前面: 存DB，後面: 顯示
MONTH_CHOICES = [
    ('1', '一月'),
    ('2', '二月'),
    ('3', '三月'),
    ('4', '四月'),
    ('5', '五月'),
    ('6', '六月'),
    ('7', '七月'),
    ('8', '八月'),
    ('9', '九月'),
    ('10', '十月'),
    ('11', '十一月'),
    ('12', '十二月'),
]
TRANSPORTATION_CHOICES = [
    ('', '------'),
    ('走路', '走路'),
    ('自行車', '自行車'),
    ('機車', '機車'),
    ('電動機車', '電動機車'),
    ('汽車(汽油)', '汽車(汽油)'),
    ('汽車(柴油)', '汽車(柴油)'),
    ('汽車(油電)', '汽車(油電)'),
    ('公車', '公車'),
    ('捷運', '捷運'),
    ('高鐵', '高鐵'),
]
EBT_TRANSPORTATION_CHOICES = [
    ('自駕汽車', '自駕汽車'),
    ('計程車', '計程車'),
    ('火車', '火車'),
    ('高鐵', '高鐵'),
    ('捷運', '捷運'),
    ('船舶', '船舶'),
    ('飛機', '飛機'),
]
FUEL_TYPE_CHOICES = [
    ('', '------'),
    ('汽油', '汽油'),
    ('柴油', '柴油'),
    ('電力', '電力(不列入計算)'),
]
WASTE_DISPOSAL_CHOICES = [
    ('焚化', '焚化'),
    ('洗淨', '洗淨'),
    ('熱處理', '熱處理'),
    ('再利用', '再利用')
]
CE_FUEL_TYPE_CHOICES = [
    ('天然氣', '天然氣'),
    ('液化石油氣', '液化石油氣'),
    ('燃煤', '燃煤'),
    ('蒸餘油(燃料油)', '蒸餘油(燃料油)')
]
VEHICLE_TYPE_CHOICES = [
    ('汽車', '汽車'),
    ('貨車', '貨車'),
    ('堆高機', '堆高機'),
    ('電動車', '電動車'),
    ('油電車', '油電車'),
    ('機車', '機車')
]
PROCESS_UNIT_CHOICES = [
    ('公噸', '公噸'),
    ('公斤', '公斤'),
    ('公升', '公升'),
    ('立方公尺', '立方公尺')
]
PROCESS_GAS_UNIT_CHOICES = [
    ('公斤', '公斤'),
    ('立方公尺', '立方公尺')
]
VOC1_UNIT_CHOICES = [
    ('公斤', '公斤'),
    ('公升', '公升')
]
DEVICE_TYPE_CHOICES = [
    ('', '----------------'),
    ('車輛、家用除濕機', '車輛、家用除濕機'),
    ('冷氣', '冷氣'),
    ('冰箱、飲水機', '冰箱、飲水機'),
    ('落地形大型冷氣機', '落地形大型冷氣機'),
    ('大型冷凍櫃', '大型冷凍櫃'),
    ('交通用冷凍、冷藏裝備', '交通用冷凍、冷藏裝備'),
    ('冷凍物流車', '冷凍物流車'),
    ('冰水機', '冰水機'),
    ('其他', '其他')
]
REFRIGERANT_TYPE_CHOICES = [
    ('R-11', 'R-11'),
    ('R-115', 'R-115'),
    ('R-12', 'R-12'),
    ('R-123', 'R-123'),
    ('R-124', 'R-124'),
    ('R-22', 'R-22'),
    ('R-23', 'R-23'),
    ('R-32', 'R-32'),
    ('R-125', 'R-125'),
    ('R-134a', 'R-134a'),
    ('R-143a', 'R-143a'),
    ('R-152a', 'R-152a'),
    ('R-401A', 'R-401A'),
    ('R-401B', 'R-401B'),
    ('R-401C', 'R-401C'),
    ('R-402A', 'R-402A'),
    ('R-402B', 'R-402B'),
    ('R-403A', 'R-403A'),
    ('R-403B', 'R-403B'),
    ('R-404A', 'R-404A'),
    ('R-405A', 'R-405A'),
    ('R-406A', 'R-406A'),
    ('R-407A', 'R-407A'),
    ('R-407B', 'R-407B'),
    ('R-407C', 'R-407C'),
    ('R-407D', 'R-407D'),
    ('R-407E', 'R-407E'),
    ('R-408A', 'R-408A'),
    ('R-409A', 'R-409A'),
    ('R-409B', 'R-409B'),
    ('R-410A', 'R-410A'),
    ('R-410B', 'R-410B'),
    ('R-411A', 'R-411A'),
    ('R-411B', 'R-411B'),
    ('R-411C', 'R-411C'),
    ('R-412A', 'R-412A'),
    ('R-413A', 'R-413A'),
    ('R-414A', 'R-414A'),
    ('R-414B', 'R-414B'),
    ('R-415A', 'R-415A'),
    ('R-415B', 'R-415B'),
    ('R-416A', 'R-416A'),
    ('R-417A', 'R-417A'),
    ('R-418A', 'R-418A'),
    ('R-419A', 'R-419A'),
    ('R-420A', 'R-420A'),
    ('R-421A', 'R-421A'),
    ('R-421B', 'R-421B'),
    ('R-422A', 'R-422A'),
    ('R-422B', 'R-422B'),
    ('R-422C', 'R-422C'),
    ('R-442A', 'R-442A'),
    ('R-500', 'R-500'),
    ('R-501', 'R-501'),
    ('R-502', 'R-502'),
    ('R-503', 'R-503'),
    ('R-504', 'R-504'),
    ('R-505', 'R-505'),
    ('R-506', 'R-506'),
    ('R-507A', 'R-507A'),
    ('R-508A', 'R-508A'),
    ('R-508B', 'R-508B'),
    ('R-509A', 'R-509A'),
    ('R-600A', 'R-600A'),
    ('R-1270', 'R-1270'),
    ('R-1234yf', 'R-1234yf'),
]
EXTINGUISHER_TYPE_CHOICES = [
    ('ABC型乾粉滅火器', 'ABC型乾粉滅火器'),
    ('BC型乾粉滅火器', 'BC型乾粉滅火器'),
    ('CO2滅火器', 'CO2滅火器'),
    ('FM200滅火器', 'FM200滅火器'),
    ('HFC滅火器', 'HFC滅火器'),
    ('強化液滅火器', '強化液滅火器'),
    ('泡沫滅火器', '泡沫滅火器'),
    ('海龍滅火器', '海龍滅火器'),
]
TRANSPORT_TYPE_CHOICES = [
    ('', '---------------------'),
    ('營業大貨車', '營業大貨車'),
    ('營業小貨車', '營業小貨車'),
    ('自用大貨車', '自用大貨車'),
    ('自用小貨車', '自用小貨車'),
    ('3.49噸常溫貨車服務(裝載率31%，包含營業據點排放)', '3.49噸常溫貨車服務(裝載率31%，包含營業據點排放)'),
    ('3.49噸常溫貨車服務(裝載率84%，包含營業據點排放)', '3.49噸常溫貨車服務(裝載率84%，包含營業據點排放)'),
    ('3.5~7.4噸常溫貨車服務(裝載率82%，包含營業據點排放)', '3.5~7.4噸常溫貨車服務(裝載率82%，包含營業據點排放)'),
    ('7.5~16噸常溫貨車服務(裝載率80%，包含營業據點排放)', '7.5~16噸常溫貨車服務(裝載率80%，包含營業據點排放)'),
    ('3.49噸低溫貨車服務(裝載率32%，包含營業據點排放)', '3.49噸低溫貨車服務(裝載率32%，包含營業據點排放)'),
    ('3.49噸低溫貨車服務(裝載率77%，包含營業據點排放)', '3.49噸低溫貨車服務(裝載率77%，包含營業據點排放)'),
    ('3.5~7.4噸低溫貨車服務(裝載率41%，包含營業據點排放)', '3.5~7.4噸低溫貨車服務(裝載率41%，包含營業據點排放)'),
    ('3.5~7.4噸低溫貨車服務(裝載率69%，包含營業據點排放)', '3.5~7.4噸低溫貨車服務(裝載率69%，包含營業據點排放)'),
    ('7.5~16噸常溫貨車服務(裝載率65%，包含營業據點排放)', '7.5~16噸常溫貨車服務(裝載率65%，包含營業據點排放)'),
    ('3.49噸多溫貨車服務(包含營業據點排放)', '3.49噸多溫貨車服務(包含營業據點排放)'),
    ('以柴油動力垃圾車清除運輸一般廢棄物', '以柴油動力垃圾車清除運輸一般廢棄物')
]
TRANSPORT_FUEL_CHOICES = [
    ('', '無'),
    ('柴油', '柴油'),
    ('汽油', '汽油'),
]
CAREER_CHOICES = [
    ('保全', '保全'),
    ('清潔工', '清潔工'),
    ('其他', '其他')
]
WEIGHT_CHOICES = [
    ('淨重', '淨重'),
    ('毛重', '毛重'),
]
CUSTOMER_CHOICES = [
    ('國內', '國內'),
    ('國外', '國外')
]
TRADE_TERM_CHOICES = [
    ('國內', '國內'),
    ('EXW', 'EXW 工廠交貨'),
    ('FCA', 'FCA 貨交承運人'),
    ('FAS', 'FAS 裝運港船邊交貨'),
    ('FOB', 'FOB 裝運港船上交貨'),
    ('CFR', 'CFR 成本+運費'),
    ('CIF', 'CIF 成本保險費+運費'),
    ('CPT', 'CPT 運費付至'),
    ('CIP', 'CIP 運費保險費付至'),
    ('DPU', 'DPU 卸貨地交貨'),
    ('DAP', 'DAP 目的地交貨'),
    ('DDP', 'DDP 完稅後交貨')
]
DOWN_PAID_CHOICES = [
    ('我方支付', '我方支付'),
    ('客戶支付(上游計算)', '客戶支付(上游計算)'),
]
COMMUTE_TRANSPORTATION_CHOICES = [
    ('', '------'),
    ('機車', '機車'),
    ('電動機車', '電動機車'),
    ('汽車(汽油)', '汽車(汽油)'),
    ('汽車(柴油)', '汽車(柴油)'),
    ('汽車(油電)', '汽車(油電)'),
    ('公車', '公車'),
    ('火車', '火車'),
    ('捷運', '捷運'),
    ('高鐵', '高鐵'),
]
BUSINESS_TRANSPORTATION_CHOICES = [
    ('', '------'),
    ('汽車', '汽車'),
    ('火車', '火車'),
    ('高鐵', '高鐵'),
    ('捷運', '捷運'),
    ('船舶', '船舶'),
    ('飛機', '飛機'),
]
SOLVENT_GAS_CHOICES = [
    ('', '-------'),
    ('CO2', 'R744，二氧化碳，CO2'),
    ('CH4', 'R50，甲烷，CH4'),
    ('HFCs', 'HFC-23/R-23，三氟甲烷，CHF3'),
    ('HFCs', 'HFC-32/R-32，二氟甲烷，CH2F2'),
    ('HFCs', 'HFC-125/R-125，1,1,1,2,2-五氟乙烷，C2HF5'),
    ('HFCs', 'HFC-134a/R-134a，1,1,1,2-四氟乙烷，C2H2F4'),
    ('HFCs', 'HFC-143a/R-143a，1,1,1-三氟乙烷，C2H3F3'),
    ('HFCs', 'HFC-152a/R-152a，1,1-二氟乙烷，C2H4F2'),
    ('HFCs', 'HFC-227ea，1,1,1,2,3,3,3-七氟丙烷，CF3CHFCF3'),
    ('HFCs', 'HFC-236fa，1,1,1,3,3,3-六氟丙烷，C3H2F6'),
    ('HFCs', 'HFC-245fa，1,1,1,3,3-五氟丙烷，CHF2CH2CF3'),
    ('HFCs', 'R401a，R22/152a/124（53/13/34）'),
    ('HFCs', 'R401b，R22/152a/124（61/11/28）'),
    ('HFCs', 'R404a，R125/143a/134a（44/52/4）'),
    ('HFCs', 'R407a，R32/125/134a（20/40/40）'),
    ('HFCs', 'R407b，R32/125/134a（10/70/20）'),
    ('HFCs', 'R407c，R32/125/134a（23/25/52）'),
    ('HFCs', 'R408a，R125/R143a/22（7/46/47）'),
    ('HFCs', 'R410a，R32/125（50/50）'),
    ('HFCs', 'R413a，R134a/218/600a'),
    ('HFCs', 'R417a，R125/134a/600a'),
    ('HFCs', 'R507，R125/143a（50.0/50.0）'),
    ('HFCs', 'FX80，R32/125'),
    ('PFCs', 'C4F10，全氟丁烷'),
    ('SF6', 'SF6，六氟化硫')
]
# 原物料種類
MATERIAL_TYPE_CHOICE = [
    ('原料', '原料'),
    ('物料', '物料')
]

# 人添清冊
CLASSIFICATION_CHOICES = [
    ('內部人員', '內部人員'),
    ('外部人員', '外部人員'),
    ('宿舍', '宿舍'),
]

# 廢棄物處置地點
WASTE_LOCATION_CHOICES = [
    ('廢棄物焚化處理服務(岡山垃圾焚化廠)', '廢棄物焚化處理服務(岡山垃圾焚化廠)'),
    ('廢棄物焚化處理服務(苗栗縣垃圾焚化廠)', '廢棄物焚化處理服務(苗栗縣垃圾焚化廠)'),
    ('廢棄物焚化處理服務(臺南市永康垃圾資源回收(焚化)廠)', '廢棄物焚化處理服務(臺南市永康垃圾資源回收(焚化)廠)'),
    ('廢棄物焚化處理服務(臺南市城西垃圾焚化廠)', '廢棄物焚化處理服務(臺南市城西垃圾焚化廠)'),
    ('廢棄物焚化清理服務(南部科學工業園區-台南園區)', '廢棄物焚化清理服務(南部科學工業園區-台南園區)'),
]



class CompanyForm(forms.ModelForm):
    class Meta:
        model = company
        fields = ('company_name', 'tax_id', 'address', 'headcount', 'superintendent', 'contact_person', 'contact_telephone', 'contact_email', 'industry_classification', 'parent_code')
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'tax_id': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'headcount': forms.TextInput(attrs={'class': 'form-control'}),
            'superintendent': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.TextInput(attrs={'class': 'form-control'}),
            # 'contact_email': forms.EmailField(required=True),
            'industry_classification': forms.Select(attrs={'class': 'form-control'}, choices=[('製造業', '製造業')]),
            # 'parent_code': forms.Select(choices=[('abc', 'abc')]),
            # 'parent_code': forms.Select(choices=parent.objects.all()),
            # 'parent_code': forms.ModelChoiceField(queryset=parent.objects.all()),
        }


# 柴油發電機
class EGform(forms.ModelForm):
    class Meta:
        model = emergency_generators
        fields = ('device_id', 'device_capacity', 'position', 'department', 'estimate',
                  'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
                  'november', 'december', 'image_note', 'message_board')
        widgets = {
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_capacity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '單位:公升'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'estimate': forms.CheckboxInput(attrs={'class': 'form-check-input estimate', 'id': 'estimate', 'type': 'checkbox', 'data-bs-toggle': 'collapse', 'href': '#estimate-collapse', 'aria-expanded': 'false', 'aria-controls': 'estimate-collapse'}),
            'january': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'february': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'march': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'april': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'june': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'july': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'august': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'september': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'october': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'november': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'december': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄(最多可輸入255個字元)'}),
        }

    def __init__(self, request, *args, **kwargs):
        super(EGform, self).__init__(*args, **kwargs)
        self.fields['department'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_device_id(self):
        device_id = self.cleaned_data.get('device_id')
        if not re.match(r'^[a-zA-Z0-9_-]*$', str(device_id)):
            raise forms.ValidationError("只能輸入'英文'、'數字'、'-'、'_'", 'invalid')
        return device_id

    def clean_device_capacity(self):
        device_capacity = self.cleaned_data.get('device_capacity')
        if device_capacity < 0:
            raise forms.ValidationError("只能輸入正整數")
        elif device_capacity == 0:
            raise forms.ValidationError("輸入數值不得為零")
        return device_capacity

    def clean(self):
        cleaned_data = self.cleaned_data
        months = ['january', 'february', 'march', 'april', 'may', 'june',
                  'july', 'august', 'september', 'october', 'november', 'december']
        for month in months:
            value = cleaned_data.get(month)
            if value:
                if not value >= 0:
                    self._errors["數值必須大於等於零"] = ["數值必須大於等於零"]
                    self._errors[month] = [month]
                    # break
        return cleaned_data


# 燃燒設備
class CEform(forms.ModelForm):
    class Meta:
        model = combustion_equipment
        fields = ('device_name', 'device_id', 'fuel_type', 'fuel_january',
                  'fuel_february', 'fuel_march', 'fuel_april', 'fuel_may', 'fuel_june', 'fuel_july', 'fuel_august',
                  'fuel_september', 'fuel_october', 'fuel_november', 'fuel_december', 'heat_january', 'heat_february',
                  'heat_march', 'heat_april', 'heat_may', 'heat_june', 'heat_july', 'heat_august', 'heat_september',
                  'heat_october', 'heat_november', 'heat_december', 'image_note', 'message_board')
        widgets = {
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'fuel_type': forms.Select(choices=CE_FUEL_TYPE_CHOICES),
            'fuel_january': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'fuel_february': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'fuel_march': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'fuel_april': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'fuel_may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'fuel_june': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'fuel_july': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'fuel_august': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'fuel_september': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'fuel_october': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'fuel_november': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'fuel_december': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'heat_january': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'heat_february': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'heat_march': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'heat_april': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'heat_may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'heat_june': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'heat_july': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'heat_august': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'heat_september': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'heat_october': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'heat_november': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'heat_december': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '熱值註解!'})
        }

    def __init__(self, request, *args, **kwargs):
        super(CEform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_device_id(self):
        device_id = self.cleaned_data.get('device_id')
        if not re.match(r'^[a-zA-Z0-9_-]*$', str(device_id)):
            raise forms.ValidationError("只能輸入'英文'、'數字'、'-'、'_'", 'invalid')
        return device_id

    def clean(self):
        cleaned_data = self.cleaned_data
        months = ['fuel_january', 'fuel_february', 'fuel_march', 'fuel_april', 'fuel_may', 'fuel_june',
                  'fuel_july', 'fuel_august', 'fuel_september', 'fuel_october', 'fuel_november', 'fuel_december',
                  'heat_january', 'heat_february', 'heat_march', 'heat_april', 'heat_may', 'heat_june',
                  'heat_july', 'heat_august', 'heat_september', 'heat_october', 'heat_november', 'heat_december']
        for month in months:
            value = cleaned_data.get(month)
            if value:
                if not value >= 0:
                    self._errors["數值必須大於等於零"] = ["數值必須大於等於零"]
                    self._errors[month] = [month]
                    # break
        return cleaned_data


# 公務車
class OFform(forms.ModelForm):
    class Meta:
        model = official_car
        fields = ('vehicle_type', 'device_id', 'fuel_type', 'department',
                  'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
                  'september', 'october', 'november', 'december',
                  'urea_total', 'urea_content_median', 'urea_water_median', 'image_note', 'message_board')
        widgets = {
            'vehicle_type': forms.Select(attrs={'id': 'vehicle_type', 'style': 'width:150px'}, choices=VEHICLE_TYPE_CHOICES),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'fuel_type': forms.Select(attrs={'id': 'fuel_type', 'style': 'width:150px'}, choices=FUEL_TYPE_CHOICES),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'january': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'february': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'march': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'april': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'june': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'july': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'august': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'september': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'october': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'november': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'december': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'urea_total': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "無添加尿素則無需填寫"}),
            'urea_content_median': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '預設中油參考值(32.5)。'}),
            'urea_water_median': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '預設中油參考值(1.09)。'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(OFform, self).__init__(*args, **kwargs)
        self.fields['department'].required = False
        self.fields['urea_total'].required = False
        self.fields['urea_content_median'].required = False
        self.fields['urea_water_median'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_device_id(self):
        device_id = self.cleaned_data.get('device_id')
        if not re.match(r'^[a-zA-Z0-9_-]*$', str(device_id)):
            raise forms.ValidationError("只能輸入'英文'、'數字'、'-'、'_'", 'invalid')
        return device_id

    def clean_vehicle_type(self):
        vehicle_type = self.cleaned_data['vehicle_type']
        for VEHICLE_TYPE in VEHICLE_TYPE_CHOICES:
            if vehicle_type == VEHICLE_TYPE[0]:
                return vehicle_type
        print('亂改表單內容:', vehicle_type)
        raise forms.ValidationError("請勿自行更改下拉選單", 'invalid')

    def clean_fuel_type(self):
        fuel_type = self.cleaned_data['fuel_type']
        for FUEL_TYPE in FUEL_TYPE_CHOICES:
            if fuel_type == FUEL_TYPE[0]:
                return fuel_type
        print('亂改表單內容:', fuel_type)
        raise forms.ValidationError("請勿自行更改下拉選單", 'invalid')

    def clean(self):
        cleaned_data = self.cleaned_data
        months = ['january', 'february', 'march', 'april', 'may', 'june',
                  'july', 'august', 'september', 'october', 'november', 'december',
                  ]
        for month in months:
            value = cleaned_data.get(month)
            if value:
                if not value >= 0:
                    self._errors["數值必須大於等於零"] = ["數值必須大於等於零"]
                    self._errors[month] = [month]
                    # break
        # 尿素驗證
        urea_total = cleaned_data.get('urea_total')
        urea_content_median = cleaned_data.get('urea_content_median')
        urea_water_median = cleaned_data.get('urea_water_median')
        if urea_total or urea_content_median or urea_water_median is not None:
            if urea_total is not None:
                if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(urea_total)):
                    self._errors["urea_total"] = ["只能輸入正實數(小數點後四位)"]
                if urea_content_median is None:
                    self._errors["urea_content_median"] = ["請輸入該欄位，中油參考值(32.5)"]
                if urea_water_median is None:
                    self._errors["urea_water_median"] = ["請輸入該欄位，中油參考值(1.09)"]

            if urea_content_median is not None:
                if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(urea_content_median)):
                    self._errors["urea_content_median"] = ["只能輸入正實數(小數點後四位)"]
                if urea_total is None:
                    self._errors["urea_total"] = ["請輸入該欄位"]
                if urea_water_median is None:
                    self._errors["urea_water_median"] = ["請輸入該欄位，中油參考值(1.09)"]

            if urea_water_median is not None:
                if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(urea_water_median)):
                    self._errors["urea_water_median"] = ["只能輸入正實數(小數點後四位)"]
                if urea_total is None:
                    self._errors["urea_total"] = ["請輸入該欄位"]
                if urea_content_median is None:
                    self._errors["urea_content_median"] = ["請輸入該欄位，中油參考值(32.5)"]
        return cleaned_data


# 原物料使用
class MTform(forms.ModelForm):
    class Meta:
        model = material
        fields = ('welding_rod_id', 'welding_rod_name', 'welding_rod_format', 'carbon_content', 'january', 'february', 'march', 'april', 'may',
                  'june', 'july', 'august', 'september', 'october', 'november', 'december', 'image_note', 'message_board')
        widgets = {
            'welding_rod_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'welding_rod_name': forms.TextInput(attrs={'class': 'form-control'}),
            'welding_rod_format': forms.TextInput(attrs={'class': 'form-control'}),
            'carbon_content': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入正實數(小數點後兩位)'}),
            'january': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'february': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'march': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'april': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'june': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'july': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'august': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'september': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'october': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'november': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'december': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(MTform, self).__init__(*args, **kwargs)
        self.fields['welding_rod_id'].required = False
        self.fields['welding_rod_name'].required = False
        self.fields['welding_rod_format'].required = False
        self.fields['carbon_content'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False
        # self.fields['material_id'].validators[]

    def clean_welding_rod_id(self):
        welding_rod_id = self.cleaned_data.get('welding_rod_id')
        if not re.match(r'^[a-zA-Z0-9_-]*$', str(welding_rod_id)):
            raise forms.ValidationError("只能輸入'英文'、'數字'、'-'、'_'", 'invalid')
        return welding_rod_id

    def clean_carbon_content(self):
        carbon_content = self.cleaned_data.get('carbon_content')
        if carbon_content is None or re.match(r'^[0-9]+(.[0-9]{0,2})?$', str(carbon_content)):
            return carbon_content
        else:
            raise forms.ValidationError("只能輸入正實數(小數點後兩位)", 'invalid')

    def clean(self):
        cleaned_data = self.cleaned_data
        months = ['january', 'february', 'march', 'april', 'may', 'june',
                  'july', 'august', 'september', 'october', 'november', 'december']
        for month in months:
            value = cleaned_data.get(month)
            if value:
                if not value >= 0:
                    self._errors["數值必須大於等於零"] = ["數值必須大於等於零"]
                    self._errors[month] = [month]
        return cleaned_data


# 製程添加化學品
class PCform(forms.ModelForm):
    class Meta:
        model = process
        fields = ('process_stage', 'chemical_id', 'chemical_coefficient', 'burn', 'process_add_name', 'chemical_name', 'chemical_formula',
                  'CAS_NO', 'unit', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
                  'october', 'november', 'december', 'image_note', 'message_board')
        widgets = {
            'process_stage': forms.TextInput(attrs={'class': 'form-control'}),
            'chemical_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'chemical_coefficient': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入正實數(小數點後十位)"}),
            'burn': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
            'process_add_name': forms.TextInput(attrs={'class': 'form-control'}),
            'chemical_name': forms.TextInput(attrs={'class': 'form-control'}),
            'chemical_formula': forms.TextInput(attrs={'class': 'form-control'}),
            'CAS_NO': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.Select(choices=PROCESS_UNIT_CHOICES),
            'january': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'february': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'march': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'april': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'june': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'july': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'august': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'september': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'october': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'november': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'december': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})

        }

    def __init__(self, request, *args, **kwargs):
        super(PCform, self).__init__(*args, **kwargs)
        self.fields['process_stage'].required = False
        self.fields['chemical_name'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_material_id(self):
        material_id = self.cleaned_data.get('material_id')
        if not re.match(r'^[a-zA-Z0-9_-]*$', str(material_id)):
            raise forms.ValidationError("只能輸入'英文'、'數字'、'-'、'_'", 'invalid')
        return material_id

    def clean_carbon_content(self):
        carbon_content = self.cleaned_data.get('carbon_content')
        if not re.match(r'^[0-9]+(.[0-9]{0,2})?$', str(carbon_content)):
            raise forms.ValidationError("只能輸入正實數(小數點後兩位)", 'invalid')
        return carbon_content

    def clean(self):
        cleaned_data = self.cleaned_data
        months = ['january', 'february', 'march', 'april', 'may', 'june',
                  'july', 'august', 'september', 'october', 'november', 'december']
        for month in months:
            value = cleaned_data.get(month)
            if value:
                if not value >= 0:
                    self._errors["數值必須大於等於零"] = ["數值必須大於等於零"]
                    self._errors[month] = [month]
        return cleaned_data


# 冰箱清單
class RFform(forms.ModelForm):
    class Meta:
        model = refrigerator
        fields = ('device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                  'filling_volume', 'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'message_board')
        widgets = {
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'years_purchased': forms.TextInput(attrs={'class': 'form-control', 'id': 'years_purchased'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入正實數(小數點後四位)"}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '0.5', 'placeholder': "只能輸入正實數(小數點後四位)"}),
            'refrigerant_type': forms.Select(attrs={'id': 'refrigerant_type', 'style': 'width:150px'}, choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(RFform, self).__init__(*args, **kwargs)
        self.fields['years_purchased'].required = False
        self.fields['brand_name'].required = False
        self.fields['position'].required = False
        self.fields['filling_volume'].required = False
        self.fields['filling_fix_volume'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_device_id(self):
        device_id = self.cleaned_data.get('device_id')
        if not re.match(r'^[a-zA-Z0-9_-]*$', str(device_id)):
            raise forms.ValidationError("只能輸入'英文'、'數字'、'-'、'_'", 'invalid')
        return device_id

    def clean_filling_volume(self):
        filling_volume = self.cleaned_data.get('filling_volume')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(filling_volume)):
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return filling_volume

    def clean_effusion_rate(self):
        effusion_rate = self.cleaned_data.get('effusion_rate')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(effusion_rate)):
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return effusion_rate


# 冷氣清單
class ACform(forms.ModelForm):
    class Meta:
        model = airconditioner
        fields = ('device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                  'filling_volume', 'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'message_board')
        widgets = {
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'years_purchased': forms.TextInput(attrs={'class': 'form-control', 'id': 'years_purchased'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入正實數(小數點後四位)"}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '5.5', 'placeholder': "只能輸入正實數(小數點後四位)"}),
            'refrigerant_type': forms.Select(attrs={'id': 'refrigerant_type', 'style': 'width:150px'}, choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(ACform, self).__init__(*args, **kwargs)
        self.fields['years_purchased'].required = False
        self.fields['brand_name'].required = False
        self.fields['position'].required = False
        self.fields['filling_volume'].required = False
        self.fields['filling_fix_volume'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_device_id(self):
        device_id = self.cleaned_data.get('device_id')
        if not re.match(r'^[a-zA-Z0-9_-]*$', str(device_id)):
            raise forms.ValidationError("只能輸入'英文'、'數字'、'-'、'_'", 'invalid')
        return device_id

    def clean_filling_volume(self):
        filling_volume = self.cleaned_data.get('filling_volume')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(filling_volume)):
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return filling_volume

    def clean_effusion_rate(self):
        effusion_rate = self.cleaned_data.get('effusion_rate')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(effusion_rate)):
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return effusion_rate


# 車輛清單
class VCform(forms.ModelForm):
    class Meta:
        model = vehicle
        fields = ('device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                  'filling_volume', 'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'message_board')
        widgets = {
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'years_purchased': forms.TextInput(attrs={'class': 'form-control', 'id': 'years_purchased'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入正實數(小數點後四位)"}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '15', 'placeholder': "只能輸入正實數(小數點後四位)"}),
            'refrigerant_type': forms.Select(attrs={'id': 'refrigerant_type', 'style': 'width:150px'}, choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(VCform, self).__init__(*args, **kwargs)
        self.fields['years_purchased'].required = False
        self.fields['brand_name'].required = False
        self.fields['position'].required = False
        self.fields['filling_volume'].required = False
        self.fields['filling_fix_volume'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_device_id(self):
        device_id = self.cleaned_data.get('device_id')
        if not re.match(r'^[a-zA-Z0-9_-]*$', str(device_id)):
            raise forms.ValidationError("只能輸入'英文'、'數字'、'-'、'_'", 'invalid')
        return device_id

    def clean_filling_volume(self):
        filling_volume = self.cleaned_data.get('filling_volume')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(filling_volume)):
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return filling_volume

    def clean_effusion_rate(self):
        effusion_rate = self.cleaned_data.get('effusion_rate')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(effusion_rate)):
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return effusion_rate


# 飲水機清單
class WDform(forms.ModelForm):
    class Meta:
        model = water_dispenser
        fields = ('device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                  'filling_volume', 'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'message_board')
        widgets = {
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'years_purchased': forms.TextInput(attrs={'class': 'form-control', 'id': 'years_purchased'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入正實數(小數點後四位)"}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '0.3', 'placeholder': "只能輸入正實數(小數點後四位)"}),
            'refrigerant_type': forms.Select(attrs={'id': 'refrigerant_type', 'style': 'width:150px'}, choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(WDform, self).__init__(*args, **kwargs)
        self.fields['years_purchased'].required = False
        self.fields['brand_name'].required = False
        self.fields['position'].required = False
        self.fields['filling_volume'].required = False
        self.fields['filling_fix_volume'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_device_id(self):
        device_id = self.cleaned_data.get('device_id')
        if not re.match(r'^[a-zA-Z0-9_-]*$', str(device_id)):
            raise forms.ValidationError("只能輸入'英文'、'數字'、'-'、'_'", 'invalid')
        return device_id

    def clean_filling_volume(self):
        filling_volume = self.cleaned_data.get('filling_volume')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(filling_volume)):
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return filling_volume

    def clean_effusion_rate(self):
        effusion_rate = self.cleaned_data.get('effusion_rate')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(effusion_rate)):
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return effusion_rate


# 冰水機清單
class IWDform(forms.ModelForm):
    class Meta:
        model = ice_water_dispenser
        fields = ('device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                  'filling_volume', 'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'message_board')
        widgets = {
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'years_purchased': forms.TextInput(attrs={'class': 'form-control', 'id': 'years_purchased'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入正實數(小數點後四位)"}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '9', 'placeholder': "只能輸入正實數(小數點後四位)"}),
            'refrigerant_type': forms.Select(attrs={'id': 'refrigerant_type', 'style': 'width:150px'}, choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(IWDform, self).__init__(*args, **kwargs)
        self.fields['years_purchased'].required = False
        self.fields['brand_name'].required = False
        self.fields['position'].required = False
        self.fields['filling_volume'].required = False
        self.fields['filling_fix_volume'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_device_id(self):
        device_id = self.cleaned_data.get('device_id')
        if not re.match(r'^[a-zA-Z0-9_-]*$', str(device_id)):
            raise forms.ValidationError("只能輸入'英文'、'數字'、'-'、'_'", 'invalid')
        return device_id

    def clean_filling_volume(self):
        filling_volume = self.cleaned_data.get('filling_volume')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(filling_volume)):
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return filling_volume

    def clean_effusion_rate(self):
        effusion_rate = self.cleaned_data.get('effusion_rate')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(effusion_rate)):
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return effusion_rate


# 製冰機清單
class IMform(forms.ModelForm):
    class Meta:
        model = ice_maker
        fields = ('device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                  'filling_volume', 'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'message_board')
        widgets = {
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'years_purchased': forms.TextInput(attrs={'class': 'form-control', 'id': 'years_purchased'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入正實數(小數點後四位)"}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '16', 'placeholder': "只能輸入正實數(小數點後四位)"}),
            'refrigerant_type': forms.Select(attrs={'id': 'refrigerant_type', 'style': 'width:150px'}, choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(IMform, self).__init__(*args, **kwargs)
        self.fields['years_purchased'].required = False
        self.fields['brand_name'].required = False
        self.fields['position'].required = False
        self.fields['filling_volume'].required = False
        self.fields['filling_fix_volume'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_device_id(self):
        device_id = self.cleaned_data.get('device_id')
        if not re.match(r'^[a-zA-Z0-9_-]*$', str(device_id)):
            raise forms.ValidationError("只能輸入'英文'、'數字'、'-'、'_'", 'invalid')
        return device_id

    def clean_filling_volume(self):
        filling_volume = self.cleaned_data.get('filling_volume')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(filling_volume)):
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return filling_volume

    def clean_effusion_rate(self):
        effusion_rate = self.cleaned_data.get('effusion_rate')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(effusion_rate)):
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return effusion_rate


# 冷媒
class ODform(forms.ModelForm):
    class Meta:
        model = other_device
        fields = ('device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                  'filling_volume', 'device_amount', 'effusion_rate', 'device_type', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'message_board')
        fields = ('device_id', 'device_name', 'device_amount', 'brand_name', 'model_type', 'position', 'years_purchased',
                  'filling_volume', 'effusion_rate', 'device_type', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'message_board')
        widgets = {
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'device_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入正整數"}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'years_purchased': forms.TextInput(attrs={'class': 'form-control', 'id': 'years_purchased'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入正實數(小數點後四位)"}),
            'effusion_rate': forms.TextInput(attrs={'id': 'effusion_rate', 'class': 'form-control'}),
            'device_type': forms.Select(attrs={'id': 'device_type', 'style': 'width:250px'}, choices=DEVICE_TYPE_CHOICES),
            'refrigerant_type': forms.Select(attrs={'id': 'refrigerant_type', 'style': 'width:250px'}, choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(ODform, self).__init__(*args, **kwargs)
        self.fields['years_purchased'].required = False
        self.fields['brand_name'].required = False
        self.fields['position'].required = False
        self.fields['filling_fix_volume'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_device_id(self):
        device_id = self.cleaned_data.get('device_id')
        if not re.match(r'^[a-zA-Z0-9_-]*$', str(device_id)):
            raise forms.ValidationError("只能輸入'英文'、'數字'、'-'、'_'", 'invalid')
        return device_id

    def clean_device_amount(self):
        device_amount = self.cleaned_data.get('device_amount')
        if device_amount < 1:
            raise forms.ValidationError("只能輸入正整數(須大於0)", 'invalid')
        return device_amount

    def clean_filling_volume(self):
        filling_volume = self.cleaned_data.get('filling_volume')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(filling_volume)):
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return filling_volume

    def clean_device_amount(self):
        device_amount = self.cleaned_data.get('device_amount')
        if not device_amount > 0:
            raise forms.ValidationError("該欄位必須大於零", 'invalid')
        return device_amount

    def clean_effusion_rate(self):
        effusion_rate = self.cleaned_data.get('effusion_rate')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(effusion_rate)):
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return effusion_rate


# 滅火器
class EXform(forms.ModelForm):
    class Meta:
        model = extinguisher
        fields = ('device_id', 'position', 'extinguisher_type',
                  'inventory', 'chemical_weight', 'filling_amount', 'filling_date',
                  'image_note', 'message_board')
        widgets = {
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'extinguisher_type': forms.Select(attrs={'id': 'extinguisher_type'}, choices=EXTINGUISHER_TYPE_CHOICES),
            'inventory': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入正整數字'}),
            'chemical_weight': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入正實數(小數點後四位)'}),
            'filling_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入數字，無更換/填充則無需填寫'}),
            'filling_date': forms.TextInput(attrs={'class': 'form-control', 'id': 'replace_filling_date', 'placeholder': '無更換/填充則無需填寫'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(EXform, self).__init__(*args, **kwargs)
        self.fields['device_id'].required = False
        self.fields['position'].required = False
        self.fields['filling_amount'].required = False
        self.fields['filling_date'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_device_id(self):
        device_id = self.cleaned_data.get('device_id')
        if not re.match(r'^[a-zA-Z0-9_-]*$', str(device_id)):
            raise forms.ValidationError("只能輸入'英文'、'數字'、'-'、'_'", 'invalid')
        return device_id

    def clean_classification(self):
        extinguisher_type = self.cleaned_data['extinguisher_type']
        for EXTINGUISHER_TYPE in EXTINGUISHER_TYPE_CHOICES:
            if extinguisher_type == EXTINGUISHER_TYPE[0]:
                return extinguisher_type
        print('亂改表單內容:', extinguisher_type)
        raise forms.ValidationError("請勿自行更改下拉選單", 'invalid')

    def clean_inventory(self):
        inventory = self.cleaned_data.get('inventory')
        if not inventory > 0:
            raise forms.ValidationError("該欄位必須大於零", 'invalid')
        return inventory

    def clean_chemical_weight(self):
        chemical_weight = self.cleaned_data.get('chemical_weight')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(chemical_weight)):
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return chemical_weight

    def clean_filling_amount(self):
        filling_amount = self.cleaned_data.get('filling_amount')
        if filling_amount:
            if not re.match(r'^[0-9]+', str(filling_amount)):
                raise forms.ValidationError("只能輸入正整數", 'invalid')
        return filling_amount


# 人添清冊
class PIform(forms.ModelForm):
    class Meta:
        model = personnel_inventory
        fields = ('classification',
                  'people_number_jan', 'people_number_feb', 'people_number_mar', 'people_number_apr', 'people_number_may',
                  'people_number_jun', 'people_number_jul', 'people_number_aug', 'people_number_sept', 'people_number_oct', 'people_number_nov', 'people_number_dec',
                  'daily_working_hours_jan', 'daily_working_hours_feb', 'daily_working_hours_mar', 'daily_working_hours_apr', 'daily_working_hours_may',
                  'daily_working_hours_jun', 'daily_working_hours_jul', 'daily_working_hours_aug', 'daily_working_hours_sept', 'daily_working_hours_oct', 'daily_working_hours_nov', 'daily_working_hours_dec',
                  'work_day_jan', 'work_day_feb', 'work_day_mar', 'work_day_apr', 'work_day_may', 'work_day_jun', 'work_day_jul', 'work_day_aug', 'work_day_sept', 'work_day_oct', 'work_day_nov', 'work_day_dec',
                  'holidays_jan', 'holidays_feb', 'holidays_mar', 'holidays_apr', 'holidays_may', 'holidays_jun', 'holidays_jul', 'holidays_aug', 'holidays_sept', 'holidays_oct', 'holidays_nov', 'holidays_dec',
                  'overtime_jan', 'overtime_feb', 'overtime_mar', 'overtime_apr', 'overtime_may', 'overtime_jun', 'overtime_jul', 'overtime_aug', 'overtime_sept', 'overtime_oct', 'overtime_nov', 'overtime_dec',
                  'leave_hours_jan', 'leave_hours_feb', 'leave_hours_mar', 'leave_hours_apr', 'leave_hours_may', 'leave_hours_jun', 'leave_hours_jul', 'leave_hours_aug', 'leave_hours_sept', 'leave_hours_oct', 'leave_hours_nov', 'leave_hours_dec',
                  'compensatory_leave_hours_jan', 'compensatory_leave_hours_feb', 'compensatory_leave_hours_mar', 'compensatory_leave_hours_apr', 'compensatory_leave_hours_may',
                  'compensatory_leave_hours_jun', 'compensatory_leave_hours_jul', 'compensatory_leave_hours_aug', 'compensatory_leave_hours_sept', 'compensatory_leave_hours_oct', 'compensatory_leave_hours_nov', 'compensatory_leave_hours_dec',
                  'image_note', 'message_board')
        widgets = {
            'classification': forms.Select(attrs={'id': 'classification', 'style': 'width:100px'}, choices=CLASSIFICATION_CHOICES),
            'people_number_jan': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'people_number_feb': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'people_number_mar': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'people_number_apr': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'people_number_may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'people_number_jun': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'people_number_jul': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'people_number_aug': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'people_number_sept': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'people_number_oct': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'people_number_nov': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'people_number_dec': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'daily_working_hours_jan': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'daily_working_hours_feb': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'daily_working_hours_mar': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'daily_working_hours_apr': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'daily_working_hours_may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'daily_working_hours_jun': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'daily_working_hours_jul': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'daily_working_hours_aug': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'daily_working_hours_sept': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'daily_working_hours_oct': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'daily_working_hours_nov': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'daily_working_hours_dec': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'work_day_jan': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'work_day_feb': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'work_day_mar': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'work_day_apr': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'work_day_may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'work_day_jun': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'work_day_jul': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'work_day_aug': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'work_day_sept': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'work_day_oct': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'work_day_nov': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'work_day_dec': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'holidays_jan': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'holidays_feb': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'holidays_mar': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'holidays_apr': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'holidays_may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'holidays_jun': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'holidays_jul': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'holidays_aug': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'holidays_sept': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'holidays_oct': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'holidays_nov': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'holidays_dec': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'overtime_jan': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'overtime_feb': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'overtime_mar': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'overtime_apr': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'overtime_may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'overtime_jun': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'overtime_jul': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'overtime_aug': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'overtime_sept': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'overtime_oct': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'overtime_nov': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'overtime_dec': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'leave_hours_jan': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'leave_hours_feb': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'leave_hours_mar': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'leave_hours_apr': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'leave_hours_may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'leave_hours_jun': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'leave_hours_jul': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'leave_hours_aug': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'leave_hours_sept': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'leave_hours_oct': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'leave_hours_nov': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'leave_hours_dec': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'compensatory_leave_hours_jan': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'compensatory_leave_hours_feb': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'compensatory_leave_hours_mar': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'compensatory_leave_hours_apr': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'compensatory_leave_hours_may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'compensatory_leave_hours_jun': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'compensatory_leave_hours_jul': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'compensatory_leave_hours_aug': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'compensatory_leave_hours_sept': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'compensatory_leave_hours_oct': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'compensatory_leave_hours_nov': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'compensatory_leave_hours_dec': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(PIform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_classification(self):
        classification = self.cleaned_data['classification']
        for CLASSIFICATION in CLASSIFICATION_CHOICES:
            if classification == CLASSIFICATION[0]:
                return classification
        print('亂改表單內容:', classification)
        raise forms.ValidationError("請勿自行更改下拉選單", 'invalid')

    def clean(self):
        cleaned_data = self.cleaned_data
        months = ['people_number_jan', 'people_number_feb', 'people_number_mar', 'people_number_apr', 'people_number_may',
                  'people_number_jun', 'people_number_jul', 'people_number_aug', 'people_number_sept', 'people_number_oct', 'people_number_nov', 'people_number_dec',
                  'daily_working_hours_jan', 'daily_working_hours_feb', 'daily_working_hours_mar', 'daily_working_hours_apr', 'daily_working_hours_may',
                  'daily_working_hours_jun', 'daily_working_hours_jul', 'daily_working_hours_aug', 'daily_working_hours_sept', 'daily_working_hours_oct', 'daily_working_hours_nov', 'daily_working_hours_dec',
                  'work_day_jan', 'work_day_feb', 'work_day_mar', 'work_day_apr', 'work_day_may', 'work_day_jun', 'work_day_jul', 'work_day_aug', 'work_day_sept', 'work_day_oct', 'work_day_nov', 'work_day_dec',
                  'holidays_jan', 'holidays_feb', 'holidays_mar', 'holidays_apr', 'holidays_may', 'holidays_jun', 'holidays_jul', 'holidays_aug', 'holidays_sept', 'holidays_oct', 'holidays_nov', 'holidays_dec',
                  'overtime_jan', 'overtime_feb', 'overtime_mar', 'overtime_apr', 'overtime_may', 'overtime_jun', 'overtime_jul', 'overtime_aug', 'overtime_sept', 'overtime_oct', 'overtime_nov', 'overtime_dec',
                  'leave_hours_jan', 'leave_hours_feb', 'leave_hours_mar', 'leave_hours_apr', 'leave_hours_may', 'leave_hours_jun', 'leave_hours_jul', 'leave_hours_aug', 'leave_hours_sept', 'leave_hours_oct', 'leave_hours_nov', 'leave_hours_dec',
                  'compensatory_leave_hours_jan', 'compensatory_leave_hours_feb', 'compensatory_leave_hours_mar', 'compensatory_leave_hours_apr', 'compensatory_leave_hours_may',
                  'compensatory_leave_hours_jun', 'compensatory_leave_hours_jul', 'compensatory_leave_hours_aug', 'compensatory_leave_hours_sept', 'compensatory_leave_hours_oct', 'compensatory_leave_hours_nov', 'compensatory_leave_hours_dec'
                  ]
        for month in months:
            value = cleaned_data.get(month)
            if value:
                if not value >= 0:
                    print('value', month)
                    self._errors["數值必須大於等於零"] = ["數值必須大於等於零"]
                    self._errors[month] = [month]
                    # break
        return cleaned_data


# 廢水
class WASTEWATERform(forms.ModelForm):
    class Meta:
        model = waste_water
        fields = ('years', 'Pi', 'Wi', 'CODi', 'Si', 'MCFj', 'Bo', 'Ri', 'COD_total',
                  'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
            'Pi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若沒有則無需填寫'}),
            'Wi': forms.TextInput(attrs={'class': 'form-control', 'id': 'Wi'}),
            'CODi': forms.TextInput(attrs={'class': 'form-control', 'id': 'CODi'}),
            'Si': forms.TextInput(attrs={'class': 'form-control'}),
            'MCFj': forms.TextInput(attrs={'class': 'form-control', 'id': 'MCFj', 'value': '0.8'}),
            'Bo': forms.TextInput(attrs={'class': 'form-control', 'id': 'Bo', 'value': '0.25'}),
            'Ri': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '無回收，填"0"'}),
            'COD_total': forms.TextInput(attrs={'class': 'form-control', 'id': 'COD_total'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(WASTEWATERform, self).__init__(*args, **kwargs)
        self.fields['years'].initial = request.session.get('years')
        self.fields['Pi'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_Pi(self):
        pi = self.cleaned_data.get('Pi')
        if pi is None:
            pass
        else:
            if pi <= 0:
                raise forms.ValidationError("Pi 必須大於 1", 'invalid')
        return pi


# 廢淤泥
class WasteSludgeForm(forms.ModelForm):
    class Meta:
        model = waste_sludge
        fields = ('waste_sludge_treatment_name', 'waste_sludge_inflow_rate', 'average_inlet_MLSS_concentration',
                  'CH4_capture_system_rate', 'combustion_equipment_efficiency', 'image_note', 'message_board')
        widgets = {
            'waste_sludge_treatment_name': forms.TextInput(attrs={'class': 'form-control'}),
            'waste_sludge_inflow_rate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入正整數字'}),
            'average_inlet_MLSS_concentration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入正整數字'}),
            'CH4_capture_system_rate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入正實數(小數點後四位)'}),
            'combustion_equipment_efficiency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入正實數(小數點後四位)'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(WasteSludgeForm, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_combustion_equipment_efficiency(self):
        combustion_equipment_efficiency = self.cleaned_data.get('combustion_equipment_efficiency')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(combustion_equipment_efficiency)):
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return combustion_equipment_efficiency

    def clean_average_inlet_MLSS_concentration(self):
        average_inlet_MLSS_concentration = self.cleaned_data.get('average_inlet_MLSS_concentration')
        if not re.match(r'^[0-9]+$', str(average_inlet_MLSS_concentration)):
            raise forms.ValidationError("只能輸入正整數字", 'invalid')
        return average_inlet_MLSS_concentration

    def clean_waste_sludge_inflow_rate(self):
        waste_sludge_inflow_rate = self.cleaned_data.get('waste_sludge_inflow_rate')
        if not re.match(r'^[0-9]+$', str(waste_sludge_inflow_rate)):
            raise forms.ValidationError("只能輸入正整數字", 'invalid')
        return waste_sludge_inflow_rate

    def clean_CH4_capture_system_rate(self):
        CH4_capture_system_rate = self.cleaned_data.get('CH4_capture_system_rate')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(CH4_capture_system_rate)):
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return CH4_capture_system_rate


# 溶劑、噴霧劑
class SolventAerosolEmissionSourcesForm(forms.ModelForm):
    class Meta:
        model = solvent_aerosol_emission_sources
        fields = ('receipt_date', 'solvent_name', 'solvent_amount', 'image_note', 'message_board')
        widgets = {
            'receipt_date': forms.TextInput(attrs={'class': 'form-control', 'id': 'receipt_date'}),
            'solvent_name': forms.TextInput(attrs={'class': 'form-control'}),
            'solvent_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入正整數'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(SolventAerosolEmissionSourcesForm, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_solvent_amount(self):
        solvent_amount = self.cleaned_data.get('solvent_amount')
        if not re.match(r'^[0-9]+$', str(solvent_amount)):
            raise forms.ValidationError("只能輸入正整數字", 'invalid')
        if str(solvent_amount) == '0':
            raise forms.ValidationError("數量需大於0", "invalid")
        return solvent_amount


# 添加氣體(溶劑噴霧劑表中表)
class GasAddFormSet(forms.ModelForm):
    class Meta:
        model = gas_add
        fields = ('solvent_capacity', 'solvent_capacity_unit', 'gas_ratio', 'density',)
        widgets = {
            'solvent_capacity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入正實數(小數點後四位)'}),
            'solvent_capacity_unit': forms.Select(attrs={'id': 'solvent_capacity_unit', 'style': 'width:100px'}, choices=(("毫升", "毫升"), ("公升", "公升"), ("oz", "oz"))),
            'gas_ratio': forms.TextInput(attrs={'class': 'form-control'}),
            'density': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入正實數(小數點後十位)'}),
        }

    def clean_solvent_capacity(self):
        solvent_capacity = self.cleaned_data.get('solvent_capacity')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(solvent_capacity)):
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return solvent_capacity

    def clean_gas_ratio(self):
        gas_ratio = self.cleaned_data.get('gas_ratio')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(gas_ratio)):
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return gas_ratio

    def clean_density(self):
        density = self.cleaned_data.get('density')
        if not re.match(r'^[0-9]+(.[0-9]{0,10})?$', str(density)):
            raise forms.ValidationError("只能輸入正實數(小數點後十位)", 'invalid')
        return density


GasAddFormSet = inlineformset_factory(solvent_aerosol_emission_sources, gas_add, form=GasAddFormSet, extra=1)


# 發電量
class ELECform(forms.ModelForm):
    class Meta:
        model = electricity
        fields = ('EMI_id', 'meter_location', 'address', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
                  'september', 'october', 'november', 'december', 'image_note', 'message_board')
        widgets = {
            # 'EMI_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'EMI_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'meter_location': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'january': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'february': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'march': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'april': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'june': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'july': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'august': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'september': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'october': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'november': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'december': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(ELECform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_EMI_id(self):
        EMI_id = self.cleaned_data.get('EMI_id')
        if not re.match(r'^[a-zA-Z0-9_-]*$', str(EMI_id)):
            raise forms.ValidationError("只能輸入'英文'、'數字'、'-'、'_'", 'invalid')
        return EMI_id

    def clean(self):
        cleaned_data = self.cleaned_data
        months = ['january', 'february', 'march', 'april', 'may', 'june',
                  'july', 'august', 'september', 'october', 'november', 'december']
        for month in months:
            value = cleaned_data.get(month)
            if value:
                if not value >= 0:
                    self._errors["數值必須大於等於零"] = ["數值必須大於等於零"]
                    self._errors[month] = [month]
                    # break
        return cleaned_data


# 上游運輸
class UTform(forms.ModelForm):
    class Meta:
        model = upstream_transportation
        fields = ('acceptance_receipt', 'commodity_name', 'weight', 'commodity_NW', 'customer',
                  'trade_term', 'receiving_address', 'delivery_address',
                  'transport_distance', 'transport_country', 'transport_type', 'transport_fuel', 'trips', 'image_note',
                  'overseas_transport_distance_nm', 'overseas_transport_distance_km', 'overseas_delivery', 'overseas_arrive',
                  'overseas_trips', 'overseas_image_note',
                  'special_transport_distance', 'special_transport_country', 'special_transport_type', 'special_transport_fuel',
                  'special_trips', 'special_image_note',
                  'air_transport_distance', 'air_delivery', 'air_arrive', 'air_trips', 'air_image_note', 'message_board')

        widgets = {
            'acceptance_receipt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '無單號請輸入: 0'}),
            'commodity_name': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.Select(attrs={'id': 'weight', 'style': 'width:65px'}, choices=WEIGHT_CHOICES),
            'commodity_NW': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入正整數字'}),
            'trade_term': forms.Select(attrs={'id': 'trade_term', 'style': 'width:150px'}, choices=TRADE_TERM_CHOICES),
            'customer': forms.Select(attrs={'id': 'customer', 'style': 'width:100px'}, choices=CUSTOMER_CHOICES),
            'receiving_address': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_address': forms.TextInput(attrs={'class': 'form-control'}),
            'transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(供應商/機場/港口至公司)'}),
            'transport_country': forms.TextInput(attrs={'class': 'form-control'}),
            'transport_type': forms.Select(attrs={'id': 'transport_type', 'style': 'width:250px'}, choices=TRANSPORT_TYPE_CHOICES),
            'transport_fuel': forms.RadioSelect(choices=TRANSPORT_FUEL_CHOICES),
            'trips': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入正整數字', 'placeholder': '只能輸入正整數字'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'overseas_transport_distance_nm': forms.TextInput(attrs={'id': 'overseas_nm', 'class': 'form-control', 'placeholder': '1海里 = 1.852公里'}),
            'overseas_transport_distance_km': forms.TextInput(attrs={'id': 'overseas_km', 'class': 'form-control', 'placeholder': '1海里 = 1.852公里'}),
            'overseas_delivery': forms.TextInput(attrs={'class': 'form-control'}),
            'overseas_arrive': forms.TextInput(attrs={'class': 'form-control'}),
            'overseas_trips': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入正整數字', 'placeholder': '只能輸入正整數字'}),
            'overseas_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'special_transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(供應商/機場/港口至公司)'}),
            'special_transport_country': forms.TextInput(attrs={'class': 'form-control'}),
            'special_transport_type': forms.Select(attrs={'id': 'special_transport_type', 'style': 'width:250px'}, choices=TRANSPORT_TYPE_CHOICES),
            'special_transport_fuel': forms.RadioSelect(choices=TRANSPORT_FUEL_CHOICES),
            'special_trips': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入正整數字', 'placeholder': '只能輸入正整數字'}),
            'special_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'air_transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(供應商/機場/港口至公司)'}),
            'air_delivery': forms.TextInput(attrs={'class': 'form-control'}),
            'air_arrive': forms.TextInput(attrs={'class': 'form-control'}),
            'air_trips': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入正整數字', 'placeholder': '只能輸入正整數字'}),
            'air_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(UTform, self).__init__(*args, **kwargs)
        self.fields['transport_distance'].required = False
        self.fields['transport_country'].required = False
        self.fields['transport_type'].required = False
        self.fields['transport_fuel'].required = False
        self.fields['trips'].required = False
        self.fields['image_note'].required = False
        self.fields['overseas_transport_distance_nm'].required = False
        self.fields['overseas_transport_distance_km'].required = False
        self.fields['overseas_delivery'].required = False
        self.fields['overseas_arrive'].required = False
        self.fields['overseas_trips'].required = False
        self.fields['overseas_image_note'].required = False
        self.fields['special_transport_distance'].required = False
        self.fields['special_transport_country'].required = False
        self.fields['special_transport_type'].required = False
        self.fields['special_transport_fuel'].required = False
        self.fields['special_trips'].required = False
        self.fields['special_image_note'].required = False
        self.fields['air_transport_distance'].required = False
        self.fields['air_delivery'].required = False
        self.fields['air_arrive'].required = False
        self.fields['air_trips'].required = False
        self.fields['air_image_note'].required = False
        self.fields['message_board'].required = False

    def clean_acceptance_receipt(self):
        acceptance_receipt = self.cleaned_data.get('acceptance_receipt')
        if not re.match(r'^[a-zA-Z0-9_-]*$', str(acceptance_receipt)):
            raise forms.ValidationError("只能輸入'英文'、'數字'、'-'、'_'", 'invalid')
        return acceptance_receipt

    def clean_commodity_NW(self):
        commodity_NW = self.cleaned_data.get('commodity_NW')
        if not re.match(r'^[0-9]+$', str(commodity_NW)):
            raise forms.ValidationError("只能輸入正整數字", 'invalid')
        if str(commodity_NW) == '0':
            raise forms.ValidationError("數量需大於0", "invalid")
        return commodity_NW


# 下游運輸
class DTform(forms.ModelForm):
    class Meta:
        model = downstream_transportation
        fields = ('acceptance_receipt', 'commodity_name', 'weight', 'commodity_NW', 'customer', 'trade_term', 'receiving_address', 'delivery_address',
                  'transport_distance', 'transport_country', 'paid', 'transport_type', 'transport_fuel', 'trips', 'image_note',
                  'overseas_transport_distance_nm', 'overseas_transport_distance_km', 'overseas_paid', 'overseas_delivery', 'overseas_arrive',
                  'overseas_trips', 'overseas_image_note',
                  'special_transport_distance', 'special_transport_country', 'special_paid', 'special_transport_type', 'special_transport_fuel',
                  'special_trips', 'special_image_note',
                  'air_transport_distance', 'air_delivery', 'air_arrive', 'air_paid', 'air_trips', 'air_image_note', 'message_board')
        widgets = {
            'acceptance_receipt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '無單號請輸入: 0'}),
            'commodity_name': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.Select(attrs={'id': 'weight', 'style': 'width:65px'}, choices=WEIGHT_CHOICES),
            'commodity_NW': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入正整數字'}),
            'customer': forms.Select(attrs={'id': 'customer', 'style': 'width:100px'}, choices=CUSTOMER_CHOICES),
            'trade_term': forms.Select(attrs={'id': 'trade_term', 'style': 'width:150px'}, choices=TRADE_TERM_CHOICES),
            'receiving_address': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_address': forms.TextInput(attrs={'class': 'form-control'}),
            'transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(供應商/機場/港口至公司)'}),
            'transport_country': forms.TextInput(attrs={'class': 'form-control'}),
            'paid': forms.RadioSelect(choices=DOWN_PAID_CHOICES),
            'transport_type': forms.Select(attrs={'id': 'transport_type', 'style': 'width:250px'}, choices=TRANSPORT_TYPE_CHOICES),
            'transport_fuel': forms.RadioSelect(choices=TRANSPORT_FUEL_CHOICES),
            'trips': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入正整數字', 'placeholder': '只能輸入正整數字'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'overseas_transport_distance_nm': forms.TextInput(attrs={'id': 'overseas_nm', 'class': 'form-control', 'placeholder': '1海里 = 1.852公里'}),
            'overseas_transport_distance_km': forms.TextInput(attrs={'id': 'overseas_km', 'class': 'form-control', 'placeholder': '1海里 = 1.852公里'}),
            'overseas_paid': forms.RadioSelect(choices=DOWN_PAID_CHOICES),
            'overseas_delivery': forms.TextInput(attrs={'class': 'form-control'}),
            'overseas_arrive': forms.TextInput(attrs={'class': 'form-control'}),
            'overseas_trips': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入正整數字', 'placeholder': '只能輸入正整數字'}),
            'overseas_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'special_transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(供應商/機場/港口至公司)'}),
            'special_transport_country': forms.TextInput(attrs={'class': 'form-control'}),
            'special_paid': forms.RadioSelect(choices=DOWN_PAID_CHOICES),
            'special_transport_type': forms.Select(attrs={'id': 'special_transport_type', 'style': 'width:250px'}, choices=TRANSPORT_TYPE_CHOICES),
            'special_transport_fuel': forms.RadioSelect(choices=TRANSPORT_FUEL_CHOICES),
            'special_trips': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入正整數字', 'placeholder': '只能輸入正整數字'}),
            'special_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'air_transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(供應商/機場/港口至公司)'}),
            'air_delivery': forms.TextInput(attrs={'class': 'form-control'}),
            'air_arrive': forms.TextInput(attrs={'class': 'form-control'}),
            'air_trips': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入正整數字', 'placeholder': '只能輸入正整數字'}),
            'air_paid': forms.RadioSelect(choices=DOWN_PAID_CHOICES),
            'air_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(DTform, self).__init__(*args, **kwargs)
        self.fields['transport_distance'].required = False
        self.fields['transport_country'].required = False
        self.fields['paid'].required = False
        self.fields['transport_type'].required = False
        self.fields['transport_fuel'].required = False
        self.fields['trips'].required = False
        self.fields['image_note'].required = False
        self.fields['overseas_transport_distance_nm'].required = False
        self.fields['overseas_transport_distance_km'].required = False
        self.fields['overseas_paid'].required = False
        self.fields['overseas_delivery'].required = False
        self.fields['overseas_arrive'].required = False
        self.fields['overseas_trips'].required = False
        self.fields['overseas_image_note'].required = False
        self.fields['special_transport_distance'].required = False
        self.fields['special_transport_country'].required = False
        self.fields['special_paid'].required = False
        self.fields['special_transport_type'].required = False
        self.fields['special_transport_fuel'].required = False
        self.fields['special_trips'].required = False
        self.fields['special_image_note'].required = False
        self.fields['air_transport_distance'].required = False
        self.fields['air_delivery'].required = False
        self.fields['air_arrive'].required = False
        self.fields['air_trips'].required = False
        self.fields['air_paid'].required = False
        self.fields['air_image_note'].required = False
        self.fields['message_board'].required = False


# 員工通勤
class ECform(forms.ModelForm):
    class Meta:
        model = employee_commute
        fields = ('employee_id', 'employee_name', 'department', 'work_days', 'city',
                  'township', 'address', 'commute_distance', 'image_note', 'message_board')
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'employee_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'work_days': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '有來就算一天(請輸入阿拉伯數字)'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'township': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'commute_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入正整數字"}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(ECform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_employee_id(self):
        employee_id = self.cleaned_data.get('employee_id')
        if not re.match(r'^[a-zA-Z0-9_-]*$', str(employee_id)):
            raise forms.ValidationError("只能輸入'英文'、'數字'、'-'、'_'", 'invalid')
        return employee_id

    def clean_work_days(self):
        work_days = self.cleaned_data.get('work_days')
        if not work_days > 0:
            raise forms.ValidationError("該欄位必須大於零", 'invalid')
        return work_days

    def clean_commute_distance(self):
        commute_distance = self.cleaned_data.get('commute_distance')
        if not commute_distance > 0:
            raise forms.ValidationError("該欄位必須大於零", 'invalid')
        return commute_distance


# 通勤段數(員工通勤表中表)
class CommuteFormSet(forms.ModelForm):
    class Meta:
        model = transportation_way
        fields = ('transportation',)
        widgets = {
            'transportation': forms.Select(choices=TRANSPORTATION_CHOICES, attrs={'class': 'form-control'}),
        }

    def clean_transportation(self):
        transportation = self.cleaned_data['transportation']
        for COMMUTE_TRANSPORTATION in TRANSPORTATION_CHOICES:
            if transportation == COMMUTE_TRANSPORTATION[0]:
                return transportation
        print('亂改表單內容:', transportation)
        raise forms.ValidationError("請勿自行更改下拉選單", 'invalid')


CommuteFormSet = inlineformset_factory(employee_commute, transportation_way, form=CommuteFormSet, extra=1)


# 員工出差
class EBTform(forms.ModelForm):
    class Meta:
        model = employee_business_trip
        fields = ('business_trip_location', 'business_trip_date', 'business_trip_number', 'employee_id', 'employee_name',
                  'department', 'bt_image_note', 'rtd_image_note', 'message_board')
        widgets = {
            'business_trip_location': forms.TextInput(attrs={'class': 'form-control'}),
            'business_trip_date': forms.TextInput(attrs={'class': 'form-control', 'id': 'business_trip_date'}),
            'business_trip_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'employee_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'bt_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'rtd_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(EBTform, self).__init__(*args, **kwargs)
        self.fields['employee_id'].required = False
        self.fields['bt_image_note'].required = False
        self.fields['rtd_image_note'].required = False
        self.fields['message_board'].required = False

    def clean_business_trip_number(self):
        business_trip_number = self.cleaned_data.get('business_trip_number')
        if not re.match(r'^[a-zA-Z0-9_-]*$', str(business_trip_number)):
            raise forms.ValidationError("只能輸入'英文'、'數字'、'-'、'_'", 'invalid')
        return business_trip_number

    def clean_employee_id(self):
        employee_id = self.cleaned_data.get('employee_id')
        if employee_id is None or re.match(r'^[a-zA-Z0-9_-]*$', str(employee_id)):
            return employee_id
        else:
            raise forms.ValidationError("只能輸入'英文'、'數字'、'-'、'_'", 'invalid')


# 出差段數(員工出差表中表)
class TripSectionFormSet(forms.ModelForm):
    class Meta:
        model = trip_section
        fields = ('departure', 'transportation', 'distance',)
        widgets = {
            'departure': forms.TextInput(attrs={'class': 'form-control'}),
            'transportation': forms.Select(choices=EBT_TRANSPORTATION_CHOICES, attrs={'class': 'form-control'}),
            'distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入正實數(小數點後四位)'})
        }

    def clean_transportation(self):
        transportation = self.cleaned_data['transportation']
        for BUSINESS_TRANSPORTATION in EBT_TRANSPORTATION_CHOICES:
            if transportation == BUSINESS_TRANSPORTATION[0]:
                return transportation
        print('亂改表單內容:', transportation)
        raise forms.ValidationError("請勿自行更改下拉選單", 'invalid')

    def clean_distance(self):
        distance = self.cleaned_data.get('distance')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(distance)) or distance <= 0:
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return distance


TripSectionFormSet = inlineformset_factory(employee_business_trip, trip_section, form=TripSectionFormSet, extra=1)


# 廢棄物運輸
class WPform(forms.ModelForm):
    class Meta:
        model = waste_process
        fields = ('waste_name', 'waste_weigh', 'waste_date', 'waste_location', 'waste_disposal', 'waste_disposal_vendor',
                  'transport_type', 'transport_fuel', 'transport_distance',
                  'image_note', 'message_board')
        widgets = {
            'waste_name': forms.TextInput(attrs={'class': 'form-control'}),
            'waste_weigh': forms.TextInput(attrs={'class': 'form-control'}),
            'waste_date': forms.TextInput(attrs={'class': 'form-control', 'id': 'waste_date'}),
            'waste_location': forms.Select(attrs={'id': 'waste_location'}, choices=WASTE_LOCATION_CHOICES),
            'waste_disposal': forms.Select(choices=WASTE_DISPOSAL_CHOICES),
            'waste_disposal_vendor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入處理廠商名稱'}),
            'transport_type': forms.Select(choices=TRANSPORT_TYPE_CHOICES, attrs={'required': 'required'}),
            'transport_fuel': forms.RadioSelect(choices=TRANSPORT_FUEL_CHOICES),
            'transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '僅公司責任需要填寫'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(WPform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_waste_weigh(self):
        waste_weigh = self.cleaned_data.get('waste_weigh')
        if not waste_weigh > 0:
            raise forms.ValidationError("該欄位必須大於零", 'invalid')
        return waste_weigh

    def clean_waste_location(self):
        waste_location = self.cleaned_data['waste_location']
        for WASTE_LOCATION in WASTE_LOCATION_CHOICES:
            if waste_location == WASTE_LOCATION[0]:
                return waste_location
        print('亂改表單內容:', waste_location)
        raise forms.ValidationError("請勿自行更改下拉選單", 'invalid')

    def clean_waste_disposal(self):
        waste_disposal = self.cleaned_data['waste_disposal']
        for WASTE_DISPOSAL in WASTE_DISPOSAL_CHOICES:
            if waste_disposal == WASTE_DISPOSAL[0]:
                return waste_disposal
        print('亂改表單內容:', waste_disposal)
        raise forms.ValidationError("請勿自行更改下拉選單", 'invalid')

    def clean_transport_type(self):
        transport_type = self.cleaned_data['transport_type']
        if transport_type is None:
            raise forms.ValidationError("請選擇下拉選單", 'invalid')
        else:
            for TRANSPORT_TYPE in TRANSPORT_TYPE_CHOICES:
                if transport_type == TRANSPORT_TYPE[0]:
                    return transport_type
            print('亂改表單內容:', transport_type)
            raise forms.ValidationError("請勿自行更改下拉選單", 'invalid')

    def clean_transport_distance(self):
        transport_distance = self.cleaned_data.get('transport_distance')
        if transport_distance is not None:
            if not transport_distance > 0:
                raise forms.ValidationError("該欄位必須大於零", 'invalid')
            else:
                return transport_distance
        else:
            return transport_distance


# 廢棄物
class WASTEform(forms.ModelForm):
    class Meta:
        model = waste
        fields = ('waste_name', 'waste_weigh', 'waste_date', 'waste_location', 'waste_disposal', 'waste_disposal_vendor',
                  'image_note', 'message_board')
        widgets = {
            'waste_name': forms.TextInput(attrs={'class': 'form-control'}),
            'waste_weigh': forms.TextInput(attrs={'class': 'form-control'}),
            'waste_date': forms.TextInput(attrs={'class': 'form-control', 'id': 'waste_date'}),
            'waste_location': forms.Select(attrs={'id': 'waste_location'}, choices=WASTE_LOCATION_CHOICES),
            'waste_disposal': forms.Select(choices=WASTE_DISPOSAL_CHOICES),
            'waste_disposal_vendor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入處理廠商名稱'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(WASTEform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_waste_weigh(self):
        waste_weigh = self.cleaned_data.get('waste_weigh')
        if not waste_weigh > 0:
            raise forms.ValidationError("該欄位必須大於零", 'invalid')
        return waste_weigh

    def clean_waste_location(self):
        waste_location = self.cleaned_data['waste_location']
        for WASTE_LOCATION in WASTE_LOCATION_CHOICES:
            if waste_location == WASTE_LOCATION[1]:
                return waste_location
        print('亂改表單內容:', waste_location)
        raise forms.ValidationError("請勿自行更改下拉選單", 'invalid')

    def clean_waste_disposal(self):
        waste_disposal = self.cleaned_data['waste_disposal']
        for WASTE_DISPOSAL in WASTE_DISPOSAL_CHOICES:
            if waste_disposal == WASTE_DISPOSAL[1]:
                return waste_disposal
        print('亂改表單內容:', waste_disposal)
        raise forms.ValidationError("請勿自行更改下拉選單", 'invalid')

    def clean_transport_type(self):
        transport_type = self.cleaned_data['transport_type']
        if transport_type is None:
            raise forms.ValidationError("請選擇下拉選單", 'invalid')
        else:
            for TRANSPORT_TYPE in TRANSPORT_TYPE_CHOICES:
                if transport_type == TRANSPORT_TYPE[1]:
                    return transport_type
            print('亂改表單內容:', transport_type)
            raise forms.ValidationError("請勿自行更改下拉選單", 'invalid')

    def clean_transport_distance(self):
        transport_distance = self.cleaned_data.get('transport_distance')
        if transport_distance is not None:
            if not transport_distance > 0:
                raise forms.ValidationError("該欄位必須大於零", 'invalid')
            else:
                return transport_distance
        else:
            return transport_distance


# VOC1
class VOCsOneForm(forms.ModelForm):
    class Meta:
        model = VOCs_one
        fields = ('years', 'process_stage', 'material_id', 'process_add_name', 'chemical_name', 'chemical_formula', 'purchase_volume', 'consumption', 'purchase_unit',
                  'CO2', 'CH4', 'N2O', 'HFC', 'PFC', 'SF6', 'NF3', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
            'process_stage': forms.TextInput(attrs={'class': 'form-control'}),
            'material_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'process_add_name': forms.TextInput(attrs={'class': 'form-control process_add_name', 'id': 'process_add_name'}),
            'chemical_name': forms.TextInput(attrs={'class': 'form-control chemical_name', 'id': 'chemical_name'}),
            'chemical_formula': forms.TextInput(attrs={'class': 'form-control chemical_formula'}),
            'purchase_volume': forms.TextInput(attrs={'class': 'form-control process_add_name', 'id': 'process_add_name'}),
            'consumption': forms.TextInput(attrs={'class': 'form-control chemical_name', 'id': 'chemical_name'}),
            'purchase_unit': forms.Select(choices=VOC1_UNIT_CHOICES),
            'CO2': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
            'CH4': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
            'N2O': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
            'HFC': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
            'PFC': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
            'SF6': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
            'NF3': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(VOCsOneForm, self).__init__(*args, **kwargs)
        self.fields['years'].initial = request.session.get('years')
        self.fields['process_add_name'].required = False
        self.fields['chemical_name'].required = False
        self.fields['chemical_formula'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


# VOC2
class VOCsTwoForm(forms.ModelForm):
    class Meta:
        model = VOCs_two
        fields = ('years', 'process_name', 'burn', 'disposal_volume', 'concentration_entrance', 'concentration_exit', 'builtIn_rate', 'custom_rate', 'concentration_ch4', 'voc_capture_rate', 'combustion_equipment_rate', 'radio_VOCs', 'radio_concentration', 'radio_co2_emission', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
            'process_name': forms.TextInput(attrs={'class': 'form-control'}),
            'burn': forms.RadioSelect(choices=((1, "未經燃燒"), (2, "經過燃燒")), attrs={'class': 'form-check-input', 'id': 'radio_burn'}),
            'disposal_volume': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': r'^[0-9]+(.[0-9]{0,4})?$', 'title': '只能輸入正實數(小數點後四位)', 'placeholder': '只能輸入正實數(小數點後四位)'}),
            'concentration_entrance': forms.TextInput(
                attrs={'class': 'form-control concentration_entrance', "id": "concentration_entrance", 'autocomplete': 'off', 'pattern': r'^[0-9]+(.[0-9]{0,4})?$', 'title': '只能輸入正實數(小數點後四位)', 'placeholder': '只能輸入正實數(小數點後四位)', "disabled": ""}),
            'concentration_exit': forms.TextInput(attrs={'class': 'form-control concentration_exit', "id": "concentration_exit", 'autocomplete': 'off', 'pattern': r'^[0-9]+(.[0-9]{0,4})?$', 'title': '只能輸入正實數(小數點後四位)', 'placeholder': '只能輸入正實數(小數點後四位)', "disabled": ""}),
            'builtIn_rate': forms.TextInput(attrs={'class': 'form-control builtIn_rate', 'id': 'builtIn_rate', 'autocomplete': 'off', 'pattern': r'^[0-9]+(.[0-9]{0,10})?$', 'title': '只能輸入正實數(小數點後十位)', 'placeholder': '只能輸入正實數(小數點後十位)', "disabled": ""}),
            'custom_rate': forms.TextInput(attrs={'class': 'form-control custom_rate', 'id': 'custom_rate', 'autocomplete': 'off', 'pattern': r'^[0-9]+(.[0-9]{0,10})?$', 'title': '只能輸入正實數(小數點後十位)', 'placeholder': '只能輸入正實數(小數點後十位)', "disabled": ""}),
            'concentration_ch4': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': r'^[0-9]+(.[0-9]{0,4})?$', 'title': '只能輸入正實數(小數點後四位)', 'placeholder': '只能輸入正實數(小數點後四位)'}),
            'voc_capture_rate': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': r'^[0-9]+(.[0-9]{0,4})?$', 'title': '只能輸入正實數(小數點後四位)', 'placeholder': '只能輸入正實數(小數點後四位)'}),
            'combustion_equipment_rate': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': r'^[0-9]+(.[0-9]{0,4})?$', 'title': '只能輸入正實數(小數點後四位)', 'placeholder': '只能輸入正實數(小數點後四位)'}),
            'radio_VOCs': forms.RadioSelect(choices=((1, "已知VOCs濃度"), (2, "未知VOCs濃度或已知CO\u2082濃度'排放係數")), attrs={'class': 'form-check-input', 'id': 'radio_VOCs'}),
            'radio_concentration': forms.RadioSelect(choices=((1, "入口濃度"), (2, "出口濃度")), attrs={'class': 'form-check-input m-0', 'id': 'radio_concentration', "disabled": ""}),
            'radio_co2_emission': forms.RadioSelect(choices=((1, "內設值"), (2, "自訂值")), attrs={'class': 'form-check-input m-0', 'id': 'radio_co2_emission', "disabled": ""}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(VOCsTwoForm, self).__init__(*args, **kwargs)
        self.fields['concentration_entrance'].required = False
        self.fields['concentration_exit'].required = False
        self.fields['builtIn_rate'].required = False
        self.fields['custom_rate'].required = False
        self.fields['radio_co2_emission'].required = False
        self.fields['radio_concentration'].required = False
        self.fields['message_board'].required = False


# 納管廢水
class PWform(forms.ModelForm):
    class Meta:
        model = pipe_wastewater
        fields = ('pipe_id', 'address', 'factory', 'january', 'february', 'march', 'april', 'may', 'june', 'july',
                  'august', 'september', 'october', 'november', 'december', 'image_note', 'message_board')
        widgets = {
            'pipe_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'factory': forms.TextInput(attrs={'class': 'form-control'}),
            'january': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'february': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'march': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'april': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'june': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'july': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'august': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'september': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'october': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'november': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'december': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(PWform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_pipe_id(self):
        pipe_id = self.cleaned_data.get('pipe_id')
        if not re.match(r'^[a-zA-Z0-9_-]*$', str(pipe_id)):
            raise forms.ValidationError("只能輸入'英文'、'數字'、'-'、'_'", 'invalid')
        return pipe_id

    def clean(self):
        cleaned_data = self.cleaned_data
        months = ['january', 'february', 'march', 'april', 'may', 'june',
                  'july', 'august', 'september', 'october', 'november', 'december']
        for month in months:
            value = cleaned_data.get(month)
            if value:
                if not value >= 0:
                    self._errors["數值必須大於等於零"] = ["數值必須大於等於零"]
                    self._errors[month] = [month]
                    # break
        return cleaned_data


# 採購原物料
class PMform(forms.ModelForm):
    class Meta:
        model = purchase_material
        fields = ('product_id', 'product_name', 'vendor', 'category_name', 'material_type', 'january', 'february', 'march', 'april', 'may', 'june', 'july',
                  'august', 'september', 'october', 'november', 'december', 'image_note', 'message_board')
        widgets = {
            'product_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'vendor': forms.TextInput(attrs={'class': 'form-control'}),
            'category_name': forms.Select(choices=DropdownOption.objects.filter(option_group='大類名稱').values_list('option_value', 'option_label')),
            'material_type': forms.Select(choices=MATERIAL_TYPE_CHOICE),
            'january': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'february': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'march': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'april': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'june': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'july': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'august': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'september': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'october': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'november': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'december': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'}),
        }

    def __init__(self, request, *args, **kwargs):
        super(PMform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_product_id(self):
        product_id = self.cleaned_data.get('product_id')
        if not re.match(r'^[a-zA-Z0-9_-]*$', str(product_id)):
            raise forms.ValidationError("只能輸入'英文'、'數字'、'-'、'_'", 'invalid')
        return product_id

    def clean_category_name(self):
        category_name = self.cleaned_data['category_name']
        if category_name is None:
            raise forms.ValidationError("請選擇下拉選單", 'invalid')
        else:
            dropdown_choices = DropdownOption.objects.filter(option_group='大類名稱').all()
            for option in dropdown_choices:
                if category_name == option.option_value:
                    return category_name
            print('亂改表單內容:', category_name)
            raise forms.ValidationError("請勿自行更改下拉選單", 'invalid')

    def clean_material_type(self):
        material_type = self.cleaned_data['material_type']
        if material_type is None:
            raise forms.ValidationError("請選擇下拉選單", 'invalid')
        else:
            for MATERIAL_TYPE in MATERIAL_TYPE_CHOICE:
                if material_type == MATERIAL_TYPE[0]:
                    return material_type
            print('亂改表單內容:', material_type)
            raise forms.ValidationError("請勿自行更改下拉選單", 'invalid')

    def clean(self):
        cleaned_data = self.cleaned_data
        months = ['january', 'february', 'march', 'april', 'may', 'june',
                  'july', 'august', 'september', 'october', 'november', 'december']
        for month in months:
            value = cleaned_data.get(month)
            if value:
                if not value >= 0:
                    self._errors["數值必須大於等於零"] = ["數值必須大於等於零"]
                    self._errors[month] = [month]
                    # break
        return cleaned_data


# 產品間接排放
class PIEform(forms.ModelForm):
    class Meta:
        model = product_indirect_emissions
        fields = ('product_id', 'product_name', 'january', 'february', 'march', 'april', 'may', 'june', 'july',
                  'august', 'september', 'october', 'november', 'december', 'image_note', 'message_board')
        widgets = {
            'product_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'january': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'february': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'march': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'april': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'june': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'july': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'august': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'september': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'october': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'november': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'december': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'}),
        }

    def __init__(self, request, *args, **kwargs):
        super(PIEform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_product_id(self):
        product_id = self.cleaned_data.get('product_id')
        if not re.match(r'^[a-zA-Z0-9_-]*$', str(product_id)):
            raise forms.ValidationError("只能輸入'英文'、'數字'、'-'、'_'", 'invalid')
        return product_id

    def clean(self):
        cleaned_data = self.cleaned_data
        months = ['january', 'february', 'march', 'april', 'may', 'june',
                  'july', 'august', 'september', 'october', 'november', 'december']
        for month in months:
            value = cleaned_data.get(month)
            if value:
                if not value >= 0:
                    self._errors["數值必須大於等於零"] = ["數值必須大於等於零"]
                    self._errors[month] = [month]
                    # break
        return cleaned_data


# 製程-氣體
class PGform(forms.ModelForm):
    class Meta:
        model = process_gas
        fields = ('receipt_number', 'department', 'receipt_date', 'amount', 'unit', 'per_amount', 'per_unit', 'image_note', 'message_board')
        widgets = {
            'receipt_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'receipt_date': forms.TextInput(attrs={'class': 'form-control', 'id': 'receipt_date'}),
            'amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入正數到小數點第四位'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "ex.瓶、罐"}),
            'per_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入正數到小數點第四位'}),
            'per_unit': forms.Select(choices=PROCESS_UNIT_CHOICES),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄，最多可輸入127個字。'})
        }

    def __init__(self, request, *args, **kwargs):
        super(PGform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    def clean_receipt_number(self):
        receipt_number = self.cleaned_data.get('receipt_number')
        if not re.match(r'^[a-zA-Z0-9_-]*$', str(receipt_number)):
            raise forms.ValidationError("只能輸入'英文'、'數字'、'-'、'_'", 'invalid')
        return receipt_number

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(amount)):
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return amount

    def clean_unit(self):
        unit = self.cleaned_data.get('unit')
        if unit == '瓶' or unit == '罐':
            return unit
        else:
            raise forms.ValidationError("只能輸入'瓶'或'罐'", 'invalid')

    def clean_per_amount(self):
        per_amount = self.cleaned_data.get('per_amount')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(per_amount)):
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return per_amount

    def clean_per_unit(self):
        per_unit = self.cleaned_data['per_unit']
        if per_unit is None:
            raise forms.ValidationError("請選擇下拉選單", 'invalid')
        else:
            for PROCESS_UNIT in PROCESS_UNIT_CHOICES:
                if per_unit == PROCESS_UNIT[0]:
                    return per_unit
            print('亂改表單內容:', per_unit)
            raise forms.ValidationError("請勿自行更改下拉選單", 'invalid')


# 混合氣體(製程氣體表中表)
class ProcessGasAddFormSet(forms.ModelForm):
    class Meta:
        model = ProcessGasAdd
        fields = ('gas_name', 'gas_ratio',)
        widgets = {
            'gas_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gas_ratio': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_gas_ratio(self):
        gas_ratio = self.cleaned_data.get('gas_ratio')
        if not re.match(r'^[0-9]+(.[0-9]{0,4})?$', str(gas_ratio)):
            raise forms.ValidationError("只能輸入正實數(小數點後四位)", 'invalid')
        return gas_ratio


ProcessGasAddFormSet = inlineformset_factory(process_gas, ProcessGasAdd, form=ProcessGasAddFormSet, extra=1)



# 圖片
class ImageForm(forms.ModelForm):
    class Meta:
        model = image
        fields = ('stage', 'image_path')
        widgets = {
            'stage': forms.TextInput(attrs={'class': 'form-control', 'value': '柴油發電機'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file', 'multiple': True, 'type': 'file', 'accept': 'image/*, .pdf, application/*'}),
        }

    def __init__(self, request, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['stage'].required = False
        self.fields['image_path'].required = False

    def clean_image_path(self):
        uploaded_file = self.cleaned_data.get('image_path')
        if uploaded_file is None:
            return None
        allowed_type = ['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx']
        file_type = uploaded_file.name.split('.')[-1].lower()
        print(file_type)
        if file_type not in allowed_type:
            raise forms.ValidationError('只允許上傳以下檔案類型：PDF, JPG, PNG, DOC, DOCX, XLS, XLSX, PPT, PPTX')
        return uploaded_file
