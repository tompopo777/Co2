import re

import django.contrib.auth.models
from django import forms

from .models import *
from django.core.validators import RegexValidator, validate_slug
from django.core.exceptions import ValidationError
from django.forms import widgets, RegexField, inlineformset_factory
from django.forms import fields
import datetime

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
    ('------', '------'),
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
    ('92汽油', '92汽油'),
    ('95汽油', '95汽油'),
    ('98汽油', '98汽油'),
    ('柴油', '柴油'),
    ('電動車', '電動車'),
]
METERING_METHOD_CHOICES = [
    ('油車', '油車'),
    ('電動車', '電動車'),
    ('公里數', '公里數'),
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
    ('液化天然氣', '液化天然氣'),
    ('燃煤', '燃煤')
]
VEHICLE_TYPE_CHOICES = [
    ('汽車', '汽車'),
    ('貨車', '貨車'),
    ('堆高機', '堆高機'),
    ('電動車', '電動車'),
    ('摩托車', '摩托車')
]
PROCESS_UNIT_CHOICES = [
    ('公斤', '公斤'),
    ('公升', '公升'),
    ('立方公尺', '立方公尺')
]
REFRIGERANT_TYPE_CHOICES = [
    ('R11', 'R11'),
    ('R12', 'R12'),
    ('R115', 'R115'),
    ('R22', 'R22'),
    ('R123', 'R123'),
    ('R124', 'R124'),
    ('R32', 'R32'),
    ('R134a', 'R134a'),
    ('R404A', 'R404A'),
    ('R407A', 'R407A'),
    ('R407F', 'R407F'),
    ('R442A', 'R442A'),
    ('R410A', 'R410A'),
    ('R-1234yf', 'R-1234yf'),
    ('R513A', 'R513A'),
    ('CO2 R-744', 'CO2 R-744'),
    ('NH3 R-717', 'NH3 R-717')
]
EXTINGUISHER_TYPE_CHOICES = [
    ('ABC型乾粉滅火器', 'ABC型乾粉滅火器'),
    ('KBC型乾粉滅火器', 'KBC型乾粉滅火器'),
    ('BC型乾粉滅火器', 'BC型乾粉滅火器'),
    ('二氧化碳滅火器', '二氧化碳滅火器'),
    ('泡沫滅火器', '泡沫滅火器'),
    ('潔淨滅火器HFC-227ea（FM-200、FE-227）', '潔淨滅火器HFC-227ea（FM-200、FE-227）'),
    ('潔淨滅火器HFC-125', '潔淨滅火器HFC-125'),
    ('潔淨滅火器Novec 1230', '潔淨滅火器Novec 1230'),
    ('潔淨滅火器Inergen（IG-541、IG-55）', '潔淨滅火器Inergen（IG-541、IG-55）'),
    ('潔淨滅火器Ar（IG-01）HFC-236fa(FE36)', '潔淨滅火器Ar（IG-01）HFC-236fa(FE36)'),
    ('金屬火災滅火器', '金屬火災滅火器')
]
TRANSPORT_TYPE_CHOICES = [
    ('', '請選擇運輸工具'),
    ('5.5噸以下(小型貨車)', '5.5噸以下(小型貨車)'),
    ('7.5噸-26噸(中型貨車)', '7.5噸-26噸(中型貨車)'),
    ('35 噸貨車(重型貨車)', '35 噸貨車(重型貨車)'),
    ('43 噸(重型貨車)', '43 噸(重型貨車)'),
    ('46 噸(重型貨車)', '46 噸(重型貨車)'),
    ('拖掛車(拖架)', '拖掛車(拖架)'),
    ('牽引車(拖頭)', '牽引車(拖頭)'),
    ('貨櫃車-35噸（20英呎貨櫃）', '貨櫃車-35噸（20英呎貨櫃）'),
    ('貨櫃車-43噸（40/45英呎貨櫃）', '貨櫃車-43噸（40/45英呎貨櫃）'),
    ('平板卡車(拖車)', '平板卡車(拖車)')
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
ORGANIZATIONAL_USE_PRODUCTS_CHOICES = [
    ('組織購買原/物料開採、製造與加工過程所產生溫室氣體排放', '組織購買原/物料開採、製造與加工過程所產生溫室氣體排放'),
    ('資本財製造與加工過程所產生溫室氣體排放', '資本財製造與加工過程所產生溫室氣體排放'),
    ('處置固體與液體廢棄物產生之運輸排放', '處置固體與液體廢棄物產生之運輸排放'),
    ('資本財租賃使用之溫室氣體排放', '資本財租賃使用之溫室氣體排放'),
    ('輔導、清潔、維護、郵遞、銀行業務等服務所產生的溫室氣體排放', '輔導、清潔、維護、郵遞、銀行業務等服務所產生的溫室氣體排放')
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
PAID_CHOICES = [
    ('公司支付', '公司支付'),
    ('客戶支付', '客戶支付'),
    ('供應商支付', '供應商支付')
]
BUSINESS_TRANSPORTATION_CHOICES = [
    ('------', '------'),
    ('自駕汽車', '自駕汽車'),
    ('高鐵', '高鐵'),
    ('火車(電聯)', '火車(電聯)'),
    ('火車(柴聯)', '火車(柴聯)'),
    ('計程車', '計程車'),
    ('機車', '機車'),
    ('捷運', '捷運'),
    ('飛機', '飛機'),
    ('船舶', '船舶'),
]


# 前面: 存DB，後面: 顯示
# COMPANY_CHOICES = []
# company_name = company.objects.values("company_name")
# for name in company_name:
#     value = name.get('company_name')
#     id_query = django.contrib.auth.models.Group.objects.filter(name=value).values("id")
#     for a in id_query:
#         key = a.get("id")
#         COMPANY_CHOICES.append((key, value))
# print("COMPANY_CHOICES:", COMPANY_CHOICES)

class EGform(forms.ModelForm):
    class Meta:
        model = emergency_generators
        fields = ('years', 'device_id', 'device_capacity', 'position', 'department',
                  'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
                  'november', 'december', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_capacity': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '單位:公升'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
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
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'}),
        }

    def __init__(self, *args, **kwargs):
        super(EGform, self).__init__(*args, **kwargs)
        self.fields['department'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False

    # def clean_device_id(self):
    #     device_id = self.cleaned_data.get('device_id')
    #     if emergency_generators.objects.filter(device_id=device_id):
    #         raise forms.ValidationError("設備編號重複!")
    #     return device_id


class CEform(forms.ModelForm):
    class Meta:
        model = combustion_equipment
        fields = ('years', 'device_name', 'device_id', 'fuel_type', 'fuel_january',
                  'fuel_february', 'fuel_march', 'fuel_april', 'fuel_may', 'fuel_june', 'fuel_july', 'fuel_august',
                  'fuel_september', 'fuel_october', 'fuel_november', 'fuel_december', 'heat_january', 'heat_february',
                  'heat_march', 'heat_april', 'heat_may', 'heat_june', 'heat_july', 'heat_august', 'heat_september',
                  'heat_october', 'heat_november', 'heat_december', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
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

    def __init__(self, *args, **kwargs):
        super(CEform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


class OFform(forms.ModelForm):
    class Meta:
        model = official_car
        fields = ('years', 'vehicle_type', 'device_id', 'fuel_type', 'department', 'metering_method',
                  'oil_january', 'oil_february', 'oil_march', 'oil_april', 'oil_may', 'oil_june', 'oil_july', 'oil_august',
                  'oil_september', 'oil_october', 'oil_november', 'oil_december', 'elec_january', 'elec_february',
                  'elec_march', 'elec_april', 'elec_may', 'elec_june', 'elec_july', 'elec_august', 'elec_september',
                  'elec_october', 'elec_november', 'elec_december', 'km_january', 'km_february', 'km_march', 'km_april',
                  'km_may', 'km_june', 'km_july', 'km_august', 'km_september', 'km_october', 'km_november', 'km_december',
                  'urea_january', 'urea_february', 'urea_march', 'urea_april', 'urea_may', 'urea_june', 'urea_july',
                  'urea_august', 'urea_september', 'urea_october', 'urea_november', 'urea_december', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'vehicle_type': forms.Select(choices=VEHICLE_TYPE_CHOICES),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'fuel_type': forms.Select(choices=FUEL_TYPE_CHOICES), 'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'metering_method': forms.RadioSelect(choices=METERING_METHOD_CHOICES),
            'oil_january': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'oil_february': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'oil_march': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'oil_april': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'oil_may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'oil_june': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'oil_july': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'oil_august': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'oil_september': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'oil_october': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'oil_november': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'oil_december': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'elec_january': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'elec_february': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'elec_march': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'elec_april': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'elec_may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'elec_june': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'elec_july': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'elec_august': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'elec_september': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'elec_october': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'elec_november': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'elec_december': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'km_january': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'km_february': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'km_march': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'km_april': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'km_may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'km_june': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'km_july': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'km_august': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'km_september': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'km_october': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'km_november': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'km_december': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'urea_january': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'urea_february': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'urea_march': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'urea_april': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'urea_may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'urea_june': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'urea_july': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'urea_august': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'urea_september': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'urea_october': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'urea_november': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'urea_december': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(OFform, self).__init__(*args, **kwargs)
        self.fields['department'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


class MTform(forms.ModelForm):
    class Meta:
        model = material
        fields = ('years', 'material_name', 'material_id', 'material_type', 'chemical', 'process_add_name', 'chemical_name', 'chemical_formula', 'january', 'february', 'march', 'april', 'may',
                  'june', 'july', 'august', 'september', 'october', 'november', 'december', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'material_name': forms.TextInput(attrs={'class': 'form-control'}),
            'material_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'material_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex. 原料/物料'}),
            'chemical': forms.CheckboxInput(attrs={'class': 'form-check-input chemical', 'id': 'chemical', 'type': 'checkbox', 'data-bs-toggle': 'collapse', 'href': '#collapsePee', 'aria-expanded': 'false', 'aria-controls': 'collapsePee'}),
            'process_add_name': forms.TextInput(attrs={'class': 'form-control process_add_name', 'id': 'process_add_name'}),
            'chemical_name': forms.TextInput(attrs={'class': 'form-control chemical_name', 'id': 'chemical_name'}),
            'chemical_formula': forms.TextInput(attrs={'class': 'form-control chemical_formula'}),
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
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(MTform, self).__init__(*args, **kwargs)
        self.fields['process_add_name'].required = False
        self.fields['chemical_name'].required = False
        self.fields['chemical_formula'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False
        # self.fields['material_id'].validators[]


class PCform(forms.ModelForm):
    class Meta:
        model = process
        fields = ('years', 'process_add_name', 'chemical_name', 'chemical_formula', 'process_stage', 'material_id', 'CAS_NO',
                  'burn', 'VOCs', 'unit', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
                  'october', 'november', 'december', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'process_stage': forms.TextInput(attrs={'class': 'form-control'}),
            'material_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'process_add_name': forms.TextInput(attrs={'class': 'form-control process_add_name'}),
            'chemical_name': forms.TextInput(attrs={'class': 'form-control chemical_name'}),
            'chemical_formula': forms.TextInput(attrs={'class': 'form-control chemical_formula'}),
            'CAS_NO': forms.TextInput(attrs={'class': 'form-control'}),
            'burn': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
            'VOCs': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
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
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})

        }

    def __init__(self, *args, **kwargs):
        super(PCform, self).__init__(*args, **kwargs)
        self.fields['chemical_formula'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


class RFform(forms.ModelForm):
    class Meta:
        model = refrigerator
        fields = ('years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'filling_volume',
                  'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '0.5'}),
            'refrigerant_type': forms.Select(choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            # 'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(RFform, self).__init__(*args, **kwargs)
        self.fields['brand_name'].required = False
        self.fields['position'].required = False
        self.fields['filling_volume'].required = False
        self.fields['filling_fix_volume'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


class ACform(forms.ModelForm):
    class Meta:
        model = airconditioner
        fields = ('years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'filling_volume',
                  'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '5.5'}),
            'refrigerant_type': forms.Select(choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            # 'image_path': forms.FileInput(attrs={'class': 'form-control-file', 'multiple': 'multiple', 'accept': 'image/*, .pdf'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(ACform, self).__init__(*args, **kwargs)
        self.fields['brand_name'].required = False
        self.fields['position'].required = False
        self.fields['filling_volume'].required = False
        self.fields['filling_fix_volume'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


class VCform(forms.ModelForm):
    class Meta:
        model = vehicle
        fields = ('years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'filling_volume',
                  'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '15'}),
            'refrigerant_type': forms.Select(choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(VCform, self).__init__(*args, **kwargs)
        self.fields['brand_name'].required = False
        self.fields['position'].required = False
        self.fields['filling_volume'].required = False
        self.fields['filling_fix_volume'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


class WDform(forms.ModelForm):
    class Meta:
        model = water_dispenser
        fields = ('years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'filling_volume',
                  'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '0.3'}),
            'refrigerant_type': forms.Select(choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(WDform, self).__init__(*args, **kwargs)
        self.fields['brand_name'].required = False
        self.fields['position'].required = False
        self.fields['filling_volume'].required = False
        self.fields['filling_fix_volume'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


class IWDform(forms.ModelForm):
    class Meta:
        model = ice_water_dispenser
        fields = ('years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'filling_volume',
                  'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '9'}),
            'refrigerant_type': forms.Select(choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(IWDform, self).__init__(*args, **kwargs)
        self.fields['brand_name'].required = False
        self.fields['position'].required = False
        self.fields['filling_volume'].required = False
        self.fields['filling_fix_volume'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


class IMform(forms.ModelForm):
    class Meta:
        model = ice_maker
        fields = ('years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'filling_volume',
                  'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '16'}),
            'refrigerant_type': forms.Select(choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(IMform, self).__init__(*args, **kwargs)
        self.fields['brand_name'].required = False
        self.fields['position'].required = False
        self.fields['filling_volume'].required = False
        self.fields['filling_fix_volume'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


class ODform(forms.ModelForm):
    class Meta:
        model = other_device
        fields = ('years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'filling_volume',
                  'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control'}),
            'refrigerant_type': forms.Select(choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(ODform, self).__init__(*args, **kwargs)
        self.fields['brand_name'].required = False
        self.fields['position'].required = False
        self.fields['filling_volume'].required = False
        self.fields['filling_fix_volume'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


class EXform(forms.ModelForm):
    class Meta:
        model = extinguisher
        fields = ('years', 'extinguisher_type', 'device_id', 'position', 'extinguisher_vendor', 'chemical_weight',
                  'inventory', 'using_amount', 'monthly', 'replace_filling_amount',
                  'replace_filling_date', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'extinguisher_type': forms.Select(choices=EXTINGUISHER_TYPE_CHOICES),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'extinguisher_vendor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '選填'}),
            'chemical_weight': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入數字'}),
            'inventory': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'using_amount': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'monthly': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker2'}),
            'replace_filling_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入數字'}),
            'replace_filling_date': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker3'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(EXform, self).__init__(*args, **kwargs)
        self.fields['device_id'].required = False
        self.fields['extinguisher_vendor'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


class PIform(forms.ModelForm):
    class Meta:
        model = personnel_inventory
        fields = ('years', 'WKhours_january', 'WKhours_february', 'WKhours_march', 'WKhours_april', 'WKhours_may',
                  'WKhours_june', 'WKhours_july', 'WKhours_august', 'WKhours_september', 'WKhours_october', 'WKhours_november',
                  'WKhours_december', 'WKnum_january', 'WKnum_february', 'WKnum_march', 'WKnum_april', 'WKnum_may', 'WKnum_june',
                  'WKnum_july', 'WKnum_august', 'WKnum_september', 'WKnum_october', 'WKnum_november', 'WKnum_december', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'WKhours_january': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_february': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_march': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_april': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_june': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_july': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_august': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_september': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_october': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_november': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_december': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKnum_january': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKnum_february': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKnum_march': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKnum_april': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKnum_may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKnum_june': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKnum_july': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKnum_august': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKnum_september': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKnum_october': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKnum_november': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKnum_december': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(PIform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


class EMPform(forms.ModelForm):
    class Meta:
        model = employee
        fields = ('years', 'career',
                  'employeeNum_january', 'employeeNum_february', 'employeeNum_march', 'employeeNum_april', 'employeeNum_may', 'employeeNum_june', 'employeeNum_july', 'employeeNum_august',
                  'employeeNum_september', 'employeeNum_october', 'employeeNum_november', 'employeeNum_december',
                  'WKdays_january', 'WKdays_february', 'WKdays_march', 'WKdays_april', 'WKdays_may', 'WKdays_june', 'WKdays_july', 'WKdays_august',
                  'WKdays_september', 'WKdays_october', 'WKdays_november', 'WKdays_december',
                  'WKhours_january', 'WKhours_february', 'WKhours_march', 'WKhours_april', 'WKhours_may', 'WKhours_june', 'WKhours_july', 'WKhours_august',
                  'WKhours_september', 'WKhours_october', 'WKhours_november', 'WKhours_december',
                  'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'career': forms.Select(choices=CAREER_CHOICES),
            'employeeNum_january': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'employeeNum_february': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'employeeNum_march': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'employeeNum_april': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'employeeNum_may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'employeeNum_june': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'employeeNum_july': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'employeeNum_august': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'employeeNum_september': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'employeeNum_october': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'employeeNum_november': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'employeeNum_december': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKdays_january': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKdays_february': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKdays_march': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKdays_april': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKdays_may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKdays_june': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKdays_july': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKdays_august': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKdays_september': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKdays_october': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKdays_november': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKdays_december': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_january': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_february': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_march': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_april': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_may': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_june': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_july': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_august': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_september': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_october': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_november': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'WKhours_december': forms.TextInput(attrs={'class': 'col-6', 'value': '0'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(EMPform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


# 廢水
class WASTEWATERform(forms.ModelForm):
    class Meta:
        model = waste_water
        fields = ('years', 'waste_water_treatment_name', 'waste_water_inflow_rate', 'average_inlet_COD_concentration',
                  'average_COD_removal_rate', 'CH4_capture_system_rate', 'combustion_equipment_efficiency',
                  'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'waste_water_treatment_name': forms.TextInput(attrs={'class': 'form-control'}),
            'waste_water_inflow_rate': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'average_inlet_COD_concentration': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'average_COD_removal_rate': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'CH4_capture_system_rate': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9].[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'combustion_equipment_efficiency': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9].[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(WASTEWATERform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


# 廢淤泥
class WasteSludgeForm(forms.ModelForm):
    class Meta:
        model = waste_sludge
        fields = ('years', 'waste_sludge_treatment_name', 'waste_sludge_inflow_rate', 'average_inlet_MLSS_concentration',
                  'CH4_capture_system_rate', 'combustion_equipment_efficiency', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'waste_sludge_treatment_name': forms.TextInput(attrs={'class': 'form-control'}),
            'waste_sludge_inflow_rate': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'average_inlet_MLSS_concentration': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'CH4_capture_system_rate': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9].[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'combustion_equipment_efficiency': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9].[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(WasteSludgeForm, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


# 溶劑、噴霧劑
class SolventAerosolEmissionSourcesForm(forms.ModelForm):
    class Meta:
        model = solvent_aerosol_emission_sources
        fields = ('years', 'solvent_name', 'solvent_amount', 'solvent_amount_unit', 'solvent_capacity',
                  'solvent_capacity_unit', 'fugitive_recharge', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'solvent_name': forms.TextInput(attrs={'class': 'form-control'}),
            'solvent_amount': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[0-9]+(.[0-9]{0,4})?$', 'title': '只能輸入正實數(小數點後四位)', 'placeholder': '只能輸入正實數(小數點後四位)'}),
            'solvent_amount_unit': forms.Select(choices=(("瓶", "瓶"), ("罐", "罐"))),
            'solvent_capacity': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[0-9]+(.[0-9]{0,4})?$', 'title': '只能輸入正實數(小數點後四位)', 'placeholder': '只能輸入正實數(小數點後四位)'}),
            'solvent_capacity_unit': forms.Select(choices=(("毫升", "毫升"), ("公升", "公升"), ("oz", "oz"))),
            'fugitive_recharge': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[0-9]+(.[0-9]{0,4})?$', 'title': '只能輸入正實數(小數點後四位)', 'placeholder': '只能輸入正實數(小數點後四位)'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(SolventAerosolEmissionSourcesForm, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


AdditiveFormSet = inlineformset_factory(solvent_aerosol_emission_sources, additive_section,
                                        fields=('additive_name', 'additive_amount', 'additive_unit', 'additive_ingredient', 'additive_ratio'), extra=1,
                                        widgets={'additive_name': forms.TextInput(attrs={'class': 'form-control'}),
                                                 'additive_amount': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[0-9]+(.[0-9]{0,4})?$', 'title': '只能輸入正實數(小數點後四位)', 'placeholder': '只能輸入正實數(小數點後四位)'}),
                                                 'additive_unit': forms.Select(choices=(("毫升", "毫升"), ("公升", "公升"), ("公克", "公克"), ("oz", "oz"))),
                                                 'additive_ingredient': forms.TextInput(attrs={'class': 'form-control'}),
                                                 'additive_ratio': forms.TextInput(attrs={'class': 'form-control'}),
                                                 })


class ELECform(forms.ModelForm):
    class Meta:
        model = electricity
        fields = ('years', 'EMI_id', 'address', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
                  'september', 'october', 'november', 'december', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'EMI_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
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
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(ELECform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


class UTform(forms.ModelForm):
    class Meta:
        model = upstream_transportation
        fields = ('acceptance_receipt', 'commodity_name', 'weight', 'commodity_NW', 'organizational_use_products', 'customer', 'supplier',
                  'supplier_address', 'trade_term', 'receiving_address', 'delivery_address',
                  'transport_distance', 'transport_country', 'paid', 'transport_type', 'transport_fuel', 'trips', 'image_note',
                  'overseas_transport_distance', 'overseas_paid', 'overseas_delivery', 'overseas_arrive',
                  'overseas_trips', 'overseas_image_note',
                  'special_transport_distance', 'special_transport_country', 'special_paid', 'special_transport_type', 'special_transport_fuel',
                  'special_trips', 'special_image_note',
                  'air_transport_distance', 'air_delivery', 'air_arrive', 'air_paid', 'air_trips', 'air_image_note', 'message_board')

        widgets = {
            'acceptance_receipt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '無單號請輸入: 0'}),
            'commodity_name': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.Select(choices=WEIGHT_CHOICES),
            'commodity_NW': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入數字'}),
            'organizational_use_products': forms.Select(choices=ORGANIZATIONAL_USE_PRODUCTS_CHOICES),
            'customer': forms.Select(choices=CUSTOMER_CHOICES),
            'supplier': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier_address': forms.TextInput(attrs={'class': 'form-control'}),
            'trade_term': forms.Select(choices=TRADE_TERM_CHOICES),
            'receiving_address': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_address': forms.TextInput(attrs={'class': 'form-control'}),
            'transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(供應商/機場/港口至公司)'}),
            'transport_country': forms.TextInput(attrs={'class': 'form-control'}),
            'paid': forms.RadioSelect(choices=PAID_CHOICES),
            'transport_type': forms.Select(choices=TRANSPORT_TYPE_CHOICES),
            'transport_fuel': forms.RadioSelect(choices=TRANSPORT_FUEL_CHOICES),
            'trips': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'overseas_transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1海里 = 1.852公里'}),
            'overseas_paid': forms.RadioSelect(choices=PAID_CHOICES),
            'overseas_delivery': forms.TextInput(attrs={'class': 'form-control'}),
            'overseas_arrive': forms.TextInput(attrs={'class': 'form-control'}),
            'overseas_trips': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'overseas_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'special_transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(供應商/機場/港口至公司)'}),
            'special_transport_country': forms.TextInput(attrs={'class': 'form-control'}),
            'special_paid': forms.RadioSelect(choices=PAID_CHOICES),
            'special_transport_type': forms.Select(choices=TRANSPORT_TYPE_CHOICES),
            'special_transport_fuel': forms.RadioSelect(choices=TRANSPORT_FUEL_CHOICES),
            'special_trips': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'special_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'air_transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(供應商/機場/港口至公司)'}),
            'air_delivery': forms.TextInput(attrs={'class': 'form-control'}),
            'air_arrive': forms.TextInput(attrs={'class': 'form-control'}),
            'air_trips': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'air_paid': forms.RadioSelect(choices=PAID_CHOICES),
            'air_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(UTform, self).__init__(*args, **kwargs)
        self.fields['transport_distance'].required = False
        self.fields['transport_country'].required = False
        self.fields['paid'].required = False
        self.fields['transport_type'].required = False
        self.fields['transport_fuel'].required = False
        self.fields['trips'].required = False
        self.fields['image_note'].required = False
        self.fields['overseas_transport_distance'].required = False
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


class DTform(forms.ModelForm):
    class Meta:
        model = downstream_transportation
        fields = ('acceptance_receipt', 'commodity_name', 'weight', 'commodity_NW', 'customer', 'supplier',
                  'supplier_address', 'trade_term', 'receiving_address', 'delivery_address',
                  'transport_distance', 'transport_country', 'paid', 'transport_type', 'transport_fuel', 'trips', 'image_note',
                  'overseas_transport_distance', 'overseas_paid', 'overseas_delivery', 'overseas_arrive',
                  'overseas_trips', 'overseas_image_note',
                  'special_transport_distance', 'special_transport_country', 'special_paid', 'special_transport_type', 'special_transport_fuel',
                  'special_trips', 'special_image_note',
                  'air_transport_distance', 'air_delivery', 'air_arrive', 'air_paid', 'air_trips', 'air_image_note', 'message_board')
        widgets = {
            'acceptance_receipt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '無單號請輸入: 0'}),
            'commodity_name': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.Select(choices=WEIGHT_CHOICES),
            'commodity_NW': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入數字'}),
            'customer': forms.Select(choices=CUSTOMER_CHOICES),
            'supplier': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier_address': forms.TextInput(attrs={'class': 'form-control'}),
            'trade_term': forms.Select(choices=TRADE_TERM_CHOICES),
            'receiving_address': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_address': forms.TextInput(attrs={'class': 'form-control'}),
            'transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(供應商/機場/港口至公司)'}),
            'transport_country': forms.TextInput(attrs={'class': 'form-control'}),
            'paid': forms.RadioSelect(choices=PAID_CHOICES),
            'transport_type': forms.Select(choices=TRANSPORT_TYPE_CHOICES),
            'transport_fuel': forms.RadioSelect(choices=TRANSPORT_FUEL_CHOICES),
            'trips': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'overseas_transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1海里 = 1.852公里'}),
            'overseas_paid': forms.RadioSelect(choices=PAID_CHOICES),
            'overseas_delivery': forms.TextInput(attrs={'class': 'form-control'}),
            'overseas_arrive': forms.TextInput(attrs={'class': 'form-control'}),
            'overseas_trips': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'overseas_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'special_transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(供應商/機場/港口至公司)'}),
            'special_transport_country': forms.TextInput(attrs={'class': 'form-control'}),
            'special_paid': forms.RadioSelect(choices=PAID_CHOICES),
            'special_transport_type': forms.Select(choices=TRANSPORT_TYPE_CHOICES),
            'special_transport_fuel': forms.RadioSelect(choices=TRANSPORT_FUEL_CHOICES),
            'special_trips': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'special_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'air_transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(供應商/機場/港口至公司)'}),
            'air_delivery': forms.TextInput(attrs={'class': 'form-control'}),
            'air_arrive': forms.TextInput(attrs={'class': 'form-control'}),
            'air_trips': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'air_paid': forms.RadioSelect(choices=PAID_CHOICES),
            'air_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(DTform, self).__init__(*args, **kwargs)
        self.fields['transport_distance'].required = False
        self.fields['transport_country'].required = False
        self.fields['paid'].required = False
        self.fields['transport_type'].required = False
        self.fields['transport_fuel'].required = False
        self.fields['trips'].required = False
        self.fields['image_note'].required = False
        self.fields['overseas_transport_distance'].required = False
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


class ECform(forms.ModelForm):
    class Meta:
        model = employee_commute
        fields = ('years', 'employee_id', 'employee_name', 'department', 'work_days', 'city',
                  'township', 'address', 'commute_distance', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'employee_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'work_days': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '有來就算一天'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'township': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'commute_distance': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[0-9.]*$', 'title': "只能輸入數字", 'placeholder': "只能輸入數字"}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(ECform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


CommuteFormSet = inlineformset_factory(employee_commute, transportation_way, fields=('transportation',), extra=1,
                                       widgets={'transportation': forms.Select(choices=TRANSPORTATION_CHOICES, attrs={'class': 'form-control'})})


class EBTform(forms.ModelForm):
    class Meta:
        model = employee_business_trip
        fields = ('business_trip_location', 'business_trip_date', 'business_trip_number', 'employee_id', 'employee_name',
                  'department', 'bt_image_note', 'rtd_image_note', 'message_board')
        widgets = {
            'business_trip_location': forms.TextInput(attrs={'class': 'form-control'}),
            'business_trip_date': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'business_trip_number': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'employee_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'bt_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'rtd_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(EBTform, self).__init__(*args, **kwargs)
        self.fields['employee_id'].required = False
        self.fields['bt_image_note'].required = False
        self.fields['rtd_image_note'].required = False
        self.fields['message_board'].required = False


TripSectionFormSet = inlineformset_factory(employee_business_trip, trip_section, fields=('departure', 'transportation', 'distance'), extra=1,
                                           widgets={'departure': forms.TextInput(attrs={'class': 'form-control'}),
                                                    'transportation': forms.Select(choices=BUSINESS_TRANSPORTATION_CHOICES, attrs={'class': 'form-control'}),
                                                    'distance': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': r'^[0-9]+(.[0-9]{0,4})?$', 'title': '只能輸入正實數(小數點後四位)', 'placeholder': '只能輸入正實數(小數點後四位)'})})


class WASTEform(forms.ModelForm):
    class Meta:
        model = waste
        fields = ('waste_name', 'waste_weigh', 'waste_date', 'waste_location', 'waste_disposal', 'waste_disposal_vendor',
                  'transport_type', 'transport_fuel', 'transport_distance', 'image_note', 'message_board')
        widgets = {
            'waste_name': forms.TextInput(attrs={'class': 'form-control'}),
            'waste_weigh': forms.TextInput(attrs={'class': 'form-control'}),
            'waste_date': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'waste_location': forms.TextInput(attrs={'class': 'form-control'}),
            'waste_disposal': forms.Select(choices=WASTE_DISPOSAL_CHOICES),
            'waste_disposal_vendor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入處理廠商名稱'}),
            'transport_type': forms.Select(choices=TRANSPORT_TYPE_CHOICES),
            'transport_fuel': forms.RadioSelect(choices=TRANSPORT_FUEL_CHOICES),
            'transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '僅公司責任需要填寫'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(WASTEform, self).__init__(*args, **kwargs)
        self.fields['transport_type'].required = False
        self.fields['transport_fuel'].required = False
        self.fields['transport_distance'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


class VOCsOneForm(forms.ModelForm):
    class Meta:
        model = VOCs_one
        fields = ('years', 'emission', 'concentration_ch4', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'emission': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': r'^[0-9]+(.[0-9]{0,4})?$', 'title': '只能輸入正實數(小數點後四位)', 'placeholder': '只能輸入正實數(小數點後四位)'}),
            'concentration_ch4': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': r'^[0-9]+(.[0-9]{0,4})?$', 'title': '只能輸入正實數(小數點後四位)', 'placeholder': '只能輸入正實數(小數點後四位)'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(VOCsOneForm, self).__init__(*args, **kwargs)
        self.fields['message_board'].required = False


class VOCsTwoForm(forms.ModelForm):
    class Meta:
        model = VOCs_two
        fields = ('years', 'disposal_volume', 'concentration_entrance', 'concentration_exit', 'builtIn_rate', 'custom_rate', 'concentration_ch4', 'voc_capture_rate', 'combustion_equipment_rate', 'radio_VOCs', 'radio_concentration', 'radio_co2_emission', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
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
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
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
        fields = ('years', 'pipe_id', 'address', 'factory', 'january', 'february', 'march', 'april', 'may', 'june', 'july',
                  'august', 'september', 'october', 'november', 'december', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
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
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(PWform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


# 採購原物料
class PMform(forms.ModelForm):
    class Meta:
        model = purchase_material
        fields = ('years', 'product_id', 'product_name', 'january', 'february', 'march', 'april', 'may', 'june', 'july',
                  'august', 'september', 'october', 'november', 'december', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
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
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'}),
        }

    def __init__(self, *args, **kwargs):
        super(PMform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


# 產品間接排放
class PIEform(forms.ModelForm):
    class Meta:
        model = product_indirect_emissions
        fields = ('years', 'product_id', 'product_name', 'january', 'february', 'march', 'april', 'may', 'june', 'july',
                  'august', 'september', 'october', 'november', 'december', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
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
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'}),
        }

    def __init__(self, *args, **kwargs):
        super(PIEform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False
