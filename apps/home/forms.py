from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *
from django.forms import inlineformset_factory

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
    ('R-11', 'R-11'),
    ('R-12', 'R-12'),
    ('R-115', 'R-115'),
    ('R-22', 'R-22'),
    ('R-123', 'R-123'),
    ('R-124', 'R-124'),
    ('R-32', 'R-32'),
    ('R-134a', 'R-134a'),
    ('R-404A', 'R-404A'),
    ('R-407A', 'R-407A'),
    ('R-407F', 'R-407F'),
    ('R-442A', 'R-442A'),
    ('R-410A', 'R-410A'),
    ('R-1234yf', 'R-1234yf'),
    ('R-513A', 'R-513A'),
    ('CO2 R-744', 'CO2 R-744'),
    ('NH3 R-717', 'NH3 R-717')
]
EXTINGUISHER_TYPE_CHOICES = [
    ('二氧化碳滅火器', '二氧化碳滅火器'),
    ('潔淨滅火器HFC-227ea（FM-200、FE-227)', '潔淨滅火器HFC-227ea（FM-200、FE-227）'),
    ('潔淨滅火器HFC-125', '潔淨滅火器HFC-125'),
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

# 人添清冊
CLASSIFICATION_CHOICES = [
    ('員工', '員工'),
    ('員工宿舍', '員工宿舍'),
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

# profile form(user)
# class CustomUserCreationForm(UserCreationForm):
#     company = forms.ModelChoiceField(queryset=company.objects.all())
#     factory = forms.ModelChoiceField(queryset=factory.objects.all())
#
#     class Meta:
#         model = User
#         fields = ('username', 'password1', 'password2', 'company', 'factory')
#
#     # def save(self, commit=True):
#     #     user = super().save(commit=False)
#     #     user_profile = Profile(user=user, company=self.cleaned_data['company'], factory=self.cleaned_data['factory'])
#     #     if commit:
#     #         user.save()
#     #         user_profile.save()
#     #     return user


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
        fields = ('years', 'device_id', 'device_capacity', 'position', 'department', 'estimate',
                  'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
                  'november', 'december', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_capacity': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '單位:公升'}),
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


# 燃燒設備
class CEform(forms.ModelForm):
    class Meta:
        model = combustion_equipment
        fields = ('years', 'device_name', 'device_id', 'fuel_type', 'fuel_january',
                  'fuel_february', 'fuel_march', 'fuel_april', 'fuel_may', 'fuel_june', 'fuel_july', 'fuel_august',
                  'fuel_september', 'fuel_october', 'fuel_november', 'fuel_december', 'heat_january', 'heat_february',
                  'heat_march', 'heat_april', 'heat_may', 'heat_june', 'heat_july', 'heat_august', 'heat_september',
                  'heat_october', 'heat_november', 'heat_december', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
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


# 公務車
class OFform(forms.ModelForm):
    class Meta:
        model = official_car
        fields = ('years', 'vehicle_type', 'device_id', 'fuel_type', 'department', 'metering_method',
                  'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
                  'september', 'october', 'november', 'december',
                  'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
            'vehicle_type': forms.Select(choices=VEHICLE_TYPE_CHOICES),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'fuel_type': forms.Select(choices=FUEL_TYPE_CHOICES),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'metering_method': forms.RadioSelect(choices=METERING_METHOD_CHOICES, attrs={'class': 'form-check-input'}),
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
        super(OFform, self).__init__(*args, **kwargs)
        self.fields['department'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


# 原物料使用
class MTform(forms.ModelForm):
    class Meta:
        model = material
        fields = ('years', 'material_name', 'material_id', 'material_type', 'chemical', 'process_add_name', 'chemical_name', 'chemical_formula', 'january', 'february', 'march', 'april', 'may',
                  'june', 'july', 'august', 'september', 'october', 'november', 'december', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
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


# 製成添加物
class PCform(forms.ModelForm):
    class Meta:
        model = process
        fields = ('years', 'process_add_name', 'carbon_content', 'process_stage', 'material_id',
                  'burn', 'VOCs', 'unit', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
                  'october', 'november', 'december', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
            'process_stage': forms.TextInput(attrs={'class': 'form-control'}),
            'material_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'process_add_name': forms.TextInput(attrs={'class': 'form-control process_add_name'}),
            'carbon_content': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[0-9]+(.[0-9]{0,2})?$', 'title': '只能輸入正實數(小數點後兩位)', 'placeholder': '只能輸入正實數(小數點後兩位)'}),
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
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


# 冰箱清單
class RFform(forms.ModelForm):
    class Meta:
        model = refrigerator
        fields = ('years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                  'filling_volume', 'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'years_purchased': forms.TextInput(attrs={'class': 'form-control', 'id': 'years_purchased'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '0.5'}),
            'refrigerant_type': forms.Select(attrs={'id': 'refrigerant_type', 'style': 'width:150px'}, choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
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


# 冷氣清單
class ACform(forms.ModelForm):
    class Meta:
        model = airconditioner
        fields = ('years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                  'filling_volume', 'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'years_purchased': forms.TextInput(attrs={'class': 'form-control', 'id': 'years_purchased'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '5.5'}),
            'refrigerant_type': forms.Select(attrs={'id': 'refrigerant_type', 'style': 'width:150px'}, choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
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


# 車輛清單
class VCform(forms.ModelForm):
    class Meta:
        model = vehicle
        fields = ('years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                  'filling_volume', 'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'years_purchased': forms.TextInput(attrs={'class': 'form-control', 'id': 'years_purchased'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '15'}),
            'refrigerant_type': forms.Select(attrs={'id': 'refrigerant_type', 'style': 'width:150px'}, choices=REFRIGERANT_TYPE_CHOICES),
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


# 飲水機清單
class WDform(forms.ModelForm):
    class Meta:
        model = water_dispenser
        fields = ('years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                  'filling_volume', 'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'years_purchased': forms.TextInput(attrs={'class': 'form-control', 'id': 'years_purchased'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '0.3'}),
            'refrigerant_type': forms.Select(attrs={'id': 'refrigerant_type', 'style': 'width:150px'}, choices=REFRIGERANT_TYPE_CHOICES),
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


# 冰水機清單
class IWDform(forms.ModelForm):
    class Meta:
        model = ice_water_dispenser
        fields = ('years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                  'filling_volume', 'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'years_purchased': forms.TextInput(attrs={'class': 'form-control', 'id': 'years_purchased'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '9'}),
            'refrigerant_type': forms.Select(attrs={'id': 'refrigerant_type', 'style': 'width:150px'}, choices=REFRIGERANT_TYPE_CHOICES),
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


# 製冰機清單
class IMform(forms.ModelForm):
    class Meta:
        model = ice_maker
        fields = ('years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                  'filling_volume', 'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'years_purchased': forms.TextInput(attrs={'class': 'form-control', 'id': 'years_purchased'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '16'}),
            'refrigerant_type': forms.Select(attrs={'id': 'refrigerant_type', 'style': 'width:150px'}, choices=REFRIGERANT_TYPE_CHOICES),
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


# 設備清單
class ODform(forms.ModelForm):
    class Meta:
        model = other_device
        fields = ('years', 'device_id', 'device_name', 'brand_name', 'model_type', 'position', 'years_purchased',
                  'filling_volume', 'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'years_purchased': forms.TextInput(attrs={'class': 'form-control', 'id': 'years_purchased'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control'}),
            'refrigerant_type': forms.Select(attrs={'id': 'refrigerant_type', 'style': 'width:150px'}, choices=REFRIGERANT_TYPE_CHOICES),
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


# 滅火器
class EXform(forms.ModelForm):
    class Meta:
        model = extinguisher
        fields = ('years', 'extinguisher_type', 'device_id', 'position', 'extinguisher_vendor', 'chemical_weight',
                  'inventory', 'using_amount', 'monthly', 'replace_filling_amount',
                  'replace_filling_date', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
            'extinguisher_type': forms.Select(attrs={'id': 'extinguisher_type'}, choices=EXTINGUISHER_TYPE_CHOICES),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[a-zA-Z0-9_-]*$', 'title': "'英文'、'數字'、'-'、'_'", 'placeholder': "只能輸入'英文'、'數字'、'-'、'_'"}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'extinguisher_vendor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '選填'}),
            'chemical_weight': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入數字'}),
            'inventory': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'using_amount': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'monthly': forms.TextInput(attrs={'class': 'form-control', 'id': 'monthly'}),
            'replace_filling_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入數字'}),
            'replace_filling_date': forms.TextInput(attrs={'class': 'form-control', 'id': 'replace_filling_date'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(EXform, self).__init__(*args, **kwargs)
        self.fields['device_id'].required = False
        self.fields['extinguisher_vendor'].required = False
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


# 人添清冊
class PIform(forms.ModelForm):
    class Meta:
        model = personnel_inventory
        fields = ('years', 'classification', 'WKhours_january', 'WKhours_february', 'WKhours_march', 'WKhours_april', 'WKhours_may',
                  'WKhours_june', 'WKhours_july', 'WKhours_august', 'WKhours_september', 'WKhours_october', 'WKhours_november',
                  'WKhours_december', 'WKnum_january', 'WKnum_february', 'WKnum_march', 'WKnum_april', 'WKnum_may', 'WKnum_june',
                  'WKnum_july', 'WKnum_august', 'WKnum_september', 'WKnum_october', 'WKnum_november', 'WKnum_december', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
            'classification': forms.Select(attrs={'id': 'classification', 'style': 'width:100px'}, choices=CLASSIFICATION_CHOICES),
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


# 委外人員清冊
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
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
            'career': forms.Select(attrs={'id': 'career', 'style': 'width:100px'}, choices=CAREER_CHOICES),
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
        fields = ('years', 'Pi', 'Wi', 'CODi', 'COD_total', 'Si', 'MCFj', 'Bo', 'Ri',
                  'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
            'Pi': forms.TextInput(attrs={'class': 'form-control', 'value': '0'}),
            'Wi': forms.TextInput(attrs={'class': 'form-control', 'value': '0'}),
            'CODi': forms.TextInput(attrs={'class': 'form-control', 'value': '0'}),
            'COD_total': forms.TextInput(attrs={'class': 'form-control', 'value': '0'}),
            'Si': forms.TextInput(attrs={'class': 'form-control', 'value': '0'}),
            'MCFj': forms.TextInput(attrs={'class': 'form-control', 'value': '0'}),
            'Bo': forms.TextInput(attrs={'class': 'form-control', 'value': '0'}),
            'Ri': forms.TextInput(attrs={'class': 'form-control', 'value': '0'}),
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
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
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
        fields = ('years', 'solvent_name', 'solvent_amount', 'solvent_capacity', 'solvent_capacity_unit',
                  'gas_name', 'gas_ratio', 'density', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
            'solvent_name': forms.TextInput(attrs={'class': 'form-control'}),
            'solvent_amount': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^\+?[1-9][0-9]*$', 'title': '只能輸入正整數', 'placeholder': '只能輸入正整數'}),
            'solvent_capacity': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[0-9]+(.[0-9]{0,4})?$', 'title': '只能輸入正實數(小數點後四位)', 'placeholder': '只能輸入正實數(小數點後四位)'}),
            'solvent_capacity_unit': forms.Select(attrs={'id': 'solvent_capacity_unit', 'style': 'width:100px'}, choices=(("毫升", "毫升"), ("公升", "公升"), ("oz", "oz"))),
            'gas_name': forms.Select(attrs={'id': 'gas_name'}, choices=SOLVENT_GAS_CHOICES),
            'gas_ratio': forms.TextInput(attrs={'class': 'form-control'}),
            'density': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^[0-9]+(.[0-9]{0,10})?$', 'title': '只能輸入正實數(小數點後十位)', 'placeholder': '只能輸入正實數(小數點後十位)'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(SolventAerosolEmissionSourcesForm, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['message_board'].required = False


# 發電量
class ELECform(forms.ModelForm):
    class Meta:
        model = electricity
        fields = ('years', 'EMI_id', 'address', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
                  'september', 'october', 'november', 'december', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
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


# 上游運輸
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


# 下游運輸
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


# 員工通勤
class ECform(forms.ModelForm):
    class Meta:
        model = employee_commute
        fields = ('years', 'employee_id', 'employee_name', 'department', 'work_days', 'city',
                  'township', 'address', 'commute_distance', 'image_note', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
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

department_CHOICES = [
    ('資材部', '資材部'),
    ('業務部', '業務部'),
    ('行銷部', '行銷部'),
    ('管理部', '管理部'),
    ('工程部', '工程部'),
    ('客服部', '客服部'),
    ('會計部', '會計部'),
    ('後勤部', '後勤部'),
    ('產品研發部', '產品研發部'),
]


# 員工出差
class EBTform(forms.ModelForm):
    class Meta:
        model = employee_business_trip
        fields = ('business_trip_location', 'business_trip_date', 'business_trip_number', 'employee_id', 'employee_name',
                  'department', 'bt_image_note', 'rtd_image_note', 'message_board')
        widgets = {
            'business_trip_location': forms.TextInput(attrs={'class': 'form-control'}),
            'business_trip_date': forms.TextInput(attrs={'class': 'form-control', 'id': 'business_trip_date'}),
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


# 廢棄物
class WASTEform(forms.ModelForm):
    class Meta:
        model = waste
        fields = ('waste_name', 'waste_weigh', 'waste_date', 'waste_location', 'waste_disposal', 'waste_disposal_vendor',
                  'transport_type', 'transport_fuel', 'transport_distance', 'image_note', 'message_board')
        widgets = {
            'waste_name': forms.TextInput(attrs={'class': 'form-control'}),
            'waste_weigh': forms.TextInput(attrs={'class': 'form-control'}),
            'waste_date': forms.TextInput(attrs={'class': 'form-control', 'id': 'waste_date'}),
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


# VOC1
class VOCsOneForm(forms.ModelForm):
    class Meta:
        model = VOCs_one
        fields = ('years', 'emission', 'concentration_ch4', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
            'emission': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': r'^[0-9]+(.[0-9]{0,4})?$', 'title': '只能輸入正實數(小數點後四位)', 'placeholder': '只能輸入正實數(小數點後四位)'}),
            'concentration_ch4': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': r'^[0-9]+(.[0-9]{0,4})?$', 'title': '只能輸入正實數(小數點後四位)', 'placeholder': '只能輸入正實數(小數點後四位)'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(VOCsOneForm, self).__init__(*args, **kwargs)
        self.fields['message_board'].required = False


# VOC2
class VOCsTwoForm(forms.ModelForm):
    class Meta:
        model = VOCs_two
        fields = ('years', 'disposal_volume', 'concentration_entrance', 'concentration_exit', 'builtIn_rate', 'custom_rate', 'concentration_ch4', 'voc_capture_rate', 'combustion_equipment_rate', 'radio_VOCs', 'radio_concentration', 'radio_co2_emission', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
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
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
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
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
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
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'years'}),
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
