from django import forms
from .models import *
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

# 前面: 存DB，後面: 顯示
# CHEMICAL_CHOICES = []
# chemical = chemical_table.objects.values("chemical_add")
# for add in chemical:
#     chemical_add = add.get('chemical_add')
#     CHEMICAL_CHOICES.append((chemical_add, chemical_add))

class EGform(forms.ModelForm):
    class Meta:
        model = emergency_generators
        fields = ('device_id', 'years', 'device_capacity', 'position', 'department',
                  'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
                  'november', 'december', 'image_note', 'image_path', 'message_board')
        widgets = {
            'device_id': forms.TextInput(attrs={'class': 'form-control'}),
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'device_capacity': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off',
                                                      'pattern': '[0-9]+', 'title': '只能輸入數字',
                                                      'placeholder': '單位:公升'}),
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
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(EGform, self).__init__(*args, **kwargs)
        self.fields['department'].required = False
        self.fields['image_note'].required = False
        self.fields['image_path'].required = False
        self.fields['message_board'].required = False


class CEform(forms.ModelForm):
    class Meta:
        model = combustion_equipment
        fields = ('device_name', 'device_id', 'fuel_type', 'years', 'fuel_january',
                  'fuel_february', 'fuel_march', 'fuel_april', 'fuel_may', 'fuel_june', 'fuel_july', 'fuel_august',
                  'fuel_september', 'fuel_october', 'fuel_november', 'fuel_december', 'heat_january', 'heat_february',
                  'heat_march', 'heat_april', 'heat_may', 'heat_june', 'heat_july', 'heat_august', 'heat_september',
                  'heat_october', 'heat_november', 'heat_december', 'image_note', 'image_path', 'message_board')
        widgets = {
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control'}),
            'fuel_type': forms.Select(choices=CE_FUEL_TYPE_CHOICES),
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
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
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '熱值註解!'})
        }

    def __init__(self, *args, **kwargs):
        super(CEform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['image_path'].required = False
        self.fields['message_board'].required = False


class OFform(forms.ModelForm):
    class Meta:
        model = official_car
        fields = ('vehicle_type', 'years', 'fuel_type', 'device_id', 'department', 'metering_method',
                  'oil_january', 'oil_february', 'oil_march', 'oil_april', 'oil_may', 'oil_june', 'oil_july', 'oil_august',
                  'oil_september', 'oil_october', 'oil_november', 'oil_december', 'elec_january', 'elec_february',
                  'elec_march', 'elec_april', 'elec_may', 'elec_june', 'elec_july', 'elec_august', 'elec_september',
                  'elec_october', 'elec_november', 'elec_december', 'km_january', 'km_february', 'km_march', 'km_april',
                  'km_may', 'km_june', 'km_july', 'km_august', 'km_september', 'km_october', 'km_november', 'km_december',
                  'urea_january', 'urea_february', 'urea_march', 'urea_april', 'urea_may', 'urea_june', 'urea_july',
                  'urea_august', 'urea_september', 'urea_october', 'urea_november', 'urea_december', 'image_note', 'image_path', 'message_board')
        widgets = {
            'vehicle_type': forms.Select(choices=VEHICLE_TYPE_CHOICES),
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'fuel_type': forms.Select(choices=FUEL_TYPE_CHOICES),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
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
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'urea_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入尿素單據名稱'}),
            'urea_image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(OFform, self).__init__(*args, **kwargs)
        self.fields['department'].required = False
        self.fields['image_note'].required = False
        self.fields['image_path'].required = False
        self.fields['message_board'].required = False


class MTform(forms.ModelForm):
    class Meta:
        model = material
        fields = ('years', 'material_name', 'material_id', 'material_type', 'chemical', 'process_add_name', 'chemical_name', 'chemical_formula', 'january', 'february', 'march', 'april', 'may',
                  'june', 'july', 'august', 'september', 'october', 'november', 'december', 'image_note', 'image_path', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'material_name': forms.TextInput(attrs={'class': 'form-control'}),
            'material_id': forms.TextInput(attrs={'class': 'form-control'}),
            'material_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex. 原料/物料'}),
            'chemical': forms.CheckboxInput(attrs={'class': 'form-check-input chemical chemical', 'id': 'chemical', 'type': 'checkbox', 'data-bs-toggle': 'collapse', 'href': '#collapsePee', 'aria-expanded': 'false', 'aria-controls': 'collapsePee'}),
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
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(MTform, self).__init__(*args, **kwargs)
        self.fields['process_add_name'].required = False
        self.fields['chemical_name'].required = False
        self.fields['chemical_formula'].required = False
        self.fields['image_note'].required = False
        self.fields['image_path'].required = False
        self.fields['message_board'].required = False


class PCform(forms.ModelForm):
    class Meta:
        model = process
        fields = ('years', 'process_add_name', 'chemical_name', 'chemical_formula', 'process_stage', 'material_id', 'CAS_NO',
                  'burn', 'VOCs', 'unit', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
                  'october', 'november', 'december', 'image_note', 'image_path', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'process_add_name': forms.TextInput(attrs={'class': 'form-control process_add_name'}),
            'chemical_name': forms.TextInput(attrs={'class': 'form-control chemical_name'}),
            'chemical_formula': forms.TextInput(attrs={'class': 'form-control chemical_formula'}),
            'process_stage': forms.TextInput(attrs={'class': 'form-control'}),
            'material_id': forms.TextInput(attrs={'class': 'form-control'}),
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
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})

        }

    def __init__(self, *args, **kwargs):
        super(PCform, self).__init__(*args, **kwargs)
        self.fields['chemical_formula'].required = False
        self.fields['image_note'].required = False
        self.fields['image_path'].required = False
        self.fields['message_board'].required = False


class RFform(forms.ModelForm):
    class Meta:
        model = refrigerator
        fields = ('years', 'device_id', 'device_name', 'brand_name', 'model_type',  'position', 'filling_volume',
                  'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'image_path', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control'}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '0.5'}),
            'refrigerant_type': forms.Select(choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(RFform, self).__init__(*args, **kwargs)
        self.fields['brand_name'].required = False
        self.fields['position'].required = False
        self.fields['filling_volume'].required = False
        self.fields['filling_fix_volume'].required = False
        self.fields['image_note'].required = False
        self.fields['image_path'].required = False
        self.fields['message_board'].required = False


class ACform(forms.ModelForm):
    class Meta:
        model = airconditioner
        fields = ('years', 'device_id', 'device_name', 'brand_name', 'model_type',  'position', 'filling_volume',
                  'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'image_path', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control'}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '5.5'}),
            'refrigerant_type': forms.Select(choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(ACform, self).__init__(*args, **kwargs)
        self.fields['brand_name'].required = False
        self.fields['position'].required = False
        self.fields['filling_volume'].required = False
        self.fields['filling_fix_volume'].required = False
        self.fields['image_note'].required = False
        self.fields['image_path'].required = False
        self.fields['message_board'].required = False


class VCform(forms.ModelForm):
    class Meta:
        model = vehicle
        fields = ('years', 'device_id', 'device_name', 'brand_name', 'model_type',  'position', 'filling_volume',
                  'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'image_path', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control'}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '15'}),
            'refrigerant_type': forms.Select(choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(VCform, self).__init__(*args, **kwargs)
        self.fields['brand_name'].required = False
        self.fields['position'].required = False
        self.fields['filling_volume'].required = False
        self.fields['filling_fix_volume'].required = False
        self.fields['image_note'].required = False
        self.fields['image_path'].required = False
        self.fields['message_board'].required = False


class WDform(forms.ModelForm):
    class Meta:
        model = water_dispenser
        fields = ('years', 'device_id', 'device_name', 'brand_name', 'model_type',  'position', 'filling_volume',
                  'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'image_path', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control'}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '0.3'}),
            'refrigerant_type': forms.Select(choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(WDform, self).__init__(*args, **kwargs)
        self.fields['brand_name'].required = False
        self.fields['position'].required = False
        self.fields['filling_volume'].required = False
        self.fields['filling_fix_volume'].required = False
        self.fields['image_note'].required = False
        self.fields['image_path'].required = False
        self.fields['message_board'].required = False


class IWDform(forms.ModelForm):
    class Meta:
        model = ice_water_dispenser
        fields = ('years', 'device_id', 'device_name', 'brand_name', 'model_type',  'position', 'filling_volume',
                  'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'image_path', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control'}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '9'}),
            'refrigerant_type': forms.Select(choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(IWDform, self).__init__(*args, **kwargs)
        self.fields['brand_name'].required = False
        self.fields['position'].required = False
        self.fields['filling_volume'].required = False
        self.fields['filling_fix_volume'].required = False
        self.fields['image_note'].required = False
        self.fields['image_path'].required = False
        self.fields['message_board'].required = False


class IMform(forms.ModelForm):
    class Meta:
        model = ice_maker
        fields = ('years', 'device_id', 'device_name', 'brand_name', 'model_type',  'position', 'filling_volume',
                  'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'image_path', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control'}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control', 'value': '16'}),
            'refrigerant_type': forms.Select(choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(IMform, self).__init__(*args, **kwargs)
        self.fields['brand_name'].required = False
        self.fields['position'].required = False
        self.fields['filling_volume'].required = False
        self.fields['filling_fix_volume'].required = False
        self.fields['image_note'].required = False
        self.fields['image_path'].required = False
        self.fields['message_board'].required = False


class ODform(forms.ModelForm):
    class Meta:
        model = other_device
        fields = ('years', 'device_id', 'device_name', 'brand_name', 'model_type',  'position', 'filling_volume',
                  'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'image_path', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control'}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control'}),
            'refrigerant_type': forms.Select(choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(ODform, self).__init__(*args, **kwargs)
        self.fields['brand_name'].required = False
        self.fields['position'].required = False
        self.fields['filling_volume'].required = False
        self.fields['filling_fix_volume'].required = False
        self.fields['image_note'].required = False
        self.fields['image_path'].required = False
        self.fields['message_board'].required = False


class RTTform(forms.ModelForm):
    class Meta:
        model = refrigerant_total_table
        fields = ('years', 'device_id', 'device_name', 'brand_name', 'model_type',  'position', 'filling_volume',
                  'effusion_rate', 'refrigerant_type', 'filling_fix_volume', 'image_note', 'image_path', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control'}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control'}),
            'refrigerant_type': forms.Select(choices=REFRIGERANT_TYPE_CHOICES),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '若有維修，則規格填充量不必填'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(RTTform, self).__init__(*args, **kwargs)
        self.fields['brand_name'].required = False
        self.fields['position'].required = False
        self.fields['filling_volume'].required = False
        self.fields['filling_fix_volume'].required = False
        self.fields['image_note'].required = False
        self.fields['image_path'].required = False
        self.fields['message_board'].required = False


class EXform(forms.ModelForm):
    class Meta:
        model = extinguisher
        fields = ('extinguisher_name', 'extinguisher_type', 'device_id', 'position', 'extinguisher_vendor', 'inventory',
                  'chemical_spec', 'chemical_weight', 'using_amount', 'using_date', 'replace_filling_amount',
                  'replace_filling_date', 'image_note', 'image_path', 'message_board')
        widgets = {
            'extinguisher_name': forms.TextInput(attrs={'class': 'form-control'}),
            'extinguisher_type': forms.TextInput(attrs={'class': 'form-control'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入編號'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'extinguisher_vendor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '選填'}),
            'inventory': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入數字'}),
            'chemical_spec': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入數字'}),
            'chemical_weight': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入數字'}),
            'using_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入數字'}),
            'using_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'replace_filling_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入數字'}),
            'replace_filling_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(EXform, self).__init__(*args, **kwargs)
        self.fields['extinguisher_vendor'].required = False
        self.fields['image_note'].required = False
        self.fields['image_path'].required = False
        self.fields['message_board'].required = False


class PIform(forms.ModelForm):
    class Meta:
        model = personnel_inventory
        fields = ('years', 'monthly', 'employee_number', 'daily_hours', 'working_days', 'overtime', 'leave_hours',
                  'day_off_hours', 'image_note', 'image_path', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'monthly': forms.Select(choices=MONTH_CHOICES),
            'employee_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入數字'}),
            'daily_hours': forms.TextInput(attrs={'class': 'form-control'}),
            'working_days': forms.TextInput(attrs={'class': 'form-control'}),
            'overtime': forms.TextInput(attrs={'class': 'form-control'}),
            'leave_hours': forms.TextInput(attrs={'class': 'form-control'}),
            'day_off_hours': forms.TextInput(attrs={'class': 'form-control'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(PIform, self).__init__(*args, **kwargs)
        self.fields['daily_hours'].required = False
        self.fields['working_days'].required = False
        self.fields['overtime'].required = False
        self.fields['leave_hours'].required = False
        self.fields['day_off_hours'].required = False
        self.fields['image_note'].required = False
        self.fields['image_path'].required = False
        self.fields['message_board'].required = False


class SCform(forms.ModelForm):
    class Meta:
        model = security
        fields = ('years', 'monthly', 'security_number', 'daily_hours', 'working_days', 'image_note', 'image_path', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'monthly': forms.Select(choices=MONTH_CHOICES),
            'security_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入數字'}),
            'daily_hours': forms.TextInput(attrs={'class': 'form-control'}),
            'working_days': forms.TextInput(attrs={'class': 'form-control'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(SCform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['image_path'].required = False
        self.fields['message_board'].required = False


class ELECform(forms.ModelForm):
    class Meta:
        model = electricity
        fields = ('years', 'EMI_id', 'address', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
                  'september', 'october', 'november', 'december', 'image_note', 'image_path', 'message_board')
        widgets = {
            'years': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'EMI_id': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'january': forms.TextInput(attrs={'class': 'col-6'}),
            'february': forms.TextInput(attrs={'class': 'col-6'}),
            'march': forms.TextInput(attrs={'class': 'col-6'}),
            'april': forms.TextInput(attrs={'class': 'col-6'}),
            'may': forms.TextInput(attrs={'class': 'col-6'}),
            'june': forms.TextInput(attrs={'class': 'col-6'}),
            'july': forms.TextInput(attrs={'class': 'col-6'}),
            'august': forms.TextInput(attrs={'class': 'col-6'}),
            'september': forms.TextInput(attrs={'class': 'col-6'}),
            'october': forms.TextInput(attrs={'class': 'col-6'}),
            'november': forms.TextInput(attrs={'class': 'col-6'}),
            'december': forms.TextInput(attrs={'class': 'col-6'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(ELECform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['image_path'].required = False
        self.fields['message_board'].required = False


class UTform(forms.ModelForm):
    class Meta:
        model = upstream_transportation
        fields = ('acceptance_receipt', 'commodity_name', 'commodity_NW', 'customer', 'supplier', 'supplier_address',
                  'trade_term', 'receiving_address', 'delivery_address', 'transport_distance', 'transport_country',
                  'transport_type', 'vehicle_fuel', 'trips', 'image_note', 'image_path', 'overseas_transport_distance',
                  'overseas_transport_type', 'overseas_delivery', 'overseas_arrive', 'overseas_trips',
                  'overseas_image_note', 'overseas_image_path', 'special_transport_distance',
                  'special_transport_country', 'special_transport_type', 'special_vehicle_fuel', 'special_trips',
                  'special_image_note', 'special_image_path', 'message_board')

        widgets = {
            'acceptance_receipt': forms.TextInput(attrs={'class': 'form-control'}),
            'commodity_name': forms.TextInput(attrs={'class': 'form-control'}),
            'commodity_NW': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入數字'}),
            'customer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入: 國內/國外'}),
            'supplier': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier_address': forms.TextInput(attrs={'class': 'form-control'}),
            'trade_term': forms.TextInput(attrs={'class': 'form-control'}),
            'receiving_address': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_address': forms.TextInput(attrs={'class': 'form-control'}),
            'transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(供應商/機場/港口至公司)'}),
            'transport_country': forms.TextInput(attrs={'class': 'form-control'}),
            'transport_type': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_fuel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex. 柴油'}),
            'trips': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'overseas_transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1海裡 = 1.852公里'}),
            'overseas_transport_type': forms.TextInput(attrs={'class': 'form-control'}),
            'overseas_delivery': forms.TextInput(attrs={'class': 'form-control'}),
            'overseas_arrive': forms.TextInput(attrs={'class': 'form-control'}),
            'overseas_trips': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'overseas_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'overseas_image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'special_transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(供應商/機場/港口至公司)'}),
            'special_transport_country': forms.TextInput(attrs={'class': 'form-control'}),
            'special_transport_type': forms.TextInput(attrs={'class': 'form-control'}),
            'special_vehicle_fuel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex. 柴油'}),
            'special_trips': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'special_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'special_image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(UTform, self).__init__(*args, **kwargs)
        self.fields['transport_distance'].required = False
        self.fields['transport_country'].required = False
        self.fields['transport_type'].required = False
        self.fields['vehicle_fuel'].required = False
        self.fields['trips'].required = False
        self.fields['image_note'].required = False
        self.fields['image_path'].required = False
        self.fields['overseas_transport_distance'].required = False
        self.fields['overseas_transport_type'].required = False
        self.fields['overseas_delivery'].required = False
        self.fields['overseas_arrive'].required = False
        self.fields['overseas_trips'].required = False
        self.fields['overseas_image_note'].required = False
        self.fields['overseas_image_path'].required = False
        self.fields['special_transport_distance'].required = False
        self.fields['special_transport_country'].required = False
        self.fields['special_transport_type'].required = False
        self.fields['special_vehicle_fuel'].required = False
        self.fields['special_trips'].required = False
        self.fields['special_image_note'].required = False
        self.fields['special_image_path'].required = False
        self.fields['message_board'].required = False


class DTform(forms.ModelForm):
    class Meta:
        model = downstream_transportation
        fields = ('acceptance_receipt', 'commodity_name', 'commodity_NW', 'customer', 'supplier', 'supplier_address',
                  'trade_term', 'receiving_address', 'delivery_address', 'transport_distance', 'transport_country',
                  'transport_type', 'vehicle_fuel', 'trips', 'image_note', 'image_path', 'overseas_transport_distance',
                  'overseas_transport_type', 'overseas_delivery', 'overseas_arrive', 'overseas_trips',
                  'overseas_image_note', 'overseas_image_path', 'special_transport_distance',
                  'special_transport_country', 'special_transport_type', 'special_vehicle_fuel', 'special_trips',
                  'special_image_note', 'special_image_path', 'message_board')
        widgets = {
            'acceptance_receipt': forms.TextInput(attrs={'class': 'form-control'}),
            'commodity_name': forms.TextInput(attrs={'class': 'form-control'}),
            'commodity_NW': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入數字'}),
            'customer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入: 國內/國外'}),
            'supplier': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier_address': forms.TextInput(attrs={'class': 'form-control'}),
            'trade_term': forms.TextInput(attrs={'class': 'form-control'}),
            'receiving_address': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_address': forms.TextInput(attrs={'class': 'form-control'}),
            'transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(供應商/機場/港口至公司)'}),
            'transport_country': forms.TextInput(attrs={'class': 'form-control'}),
            'transport_type': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_fuel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex. 柴油'}),
            'trips': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'overseas_transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1海裡 = 1.852公里'}),
            'overseas_transport_type': forms.TextInput(attrs={'class': 'form-control'}),
            'overseas_delivery': forms.TextInput(attrs={'class': 'form-control'}),
            'overseas_arrive': forms.TextInput(attrs={'class': 'form-control'}),
            'overseas_trips': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'overseas_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'overseas_image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'special_transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(供應商/機場/港口至公司)'}),
            'special_transport_country': forms.TextInput(attrs={'class': 'form-control'}),
            'special_transport_type': forms.TextInput(attrs={'class': 'form-control'}),
            'special_vehicle_fuel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex. 柴油'}),
            'special_trips': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '只能輸入數字'}),
            'special_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'special_image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(DTform, self).__init__(*args, **kwargs)
        self.fields['transport_distance'].required = False
        self.fields['transport_country'].required = False
        self.fields['transport_type'].required = False
        self.fields['vehicle_fuel'].required = False
        self.fields['trips'].required = False
        self.fields['image_note'].required = False
        self.fields['image_path'].required = False
        self.fields['overseas_transport_distance'].required = False
        self.fields['overseas_transport_type'].required = False
        self.fields['overseas_delivery'].required = False
        self.fields['overseas_arrive'].required = False
        self.fields['overseas_trips'].required = False
        self.fields['overseas_image_note'].required = False
        self.fields['overseas_image_path'].required = False
        self.fields['special_transport_distance'].required = False
        self.fields['special_transport_country'].required = False
        self.fields['special_transport_type'].required = False
        self.fields['special_vehicle_fuel'].required = False
        self.fields['special_trips'].required = False
        self.fields['special_image_note'].required = False
        self.fields['special_image_path'].required = False
        self.fields['message_board'].required = False


class ECform(forms.ModelForm):
    class Meta:
        model = employee_commute
        fields = ('employee_id', 'employee_name', 'department', 'work_days', 'transportation', 'displacement', 'city',
                  'township', 'address', 'commute_distance', 'image_note', 'image_path', 'message_board')
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'employee_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'work_days': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '有來就算一天'}),
            'transportation': forms.Select(choices=TRANSPORTATION_CHOICES),
            'displacement': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'township': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'commute_distance': forms.TextInput(attrs={'class': 'form-control'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(ECform, self).__init__(*args, **kwargs)
        self.fields['image_note'].required = False
        self.fields['image_path'].required = False
        self.fields['message_board'].required = False


class EBTform(forms.ModelForm):
    class Meta:
        model = employee_business_trip
        fields = ('business_trip_location', 'business_trip_date', 'transportation', 'employee_id', 'employee_name',
                  'department', 'departure', 'destination', 'bt_image_note', 'bt_image_path', 'round_trip_distance',
                  'rtd_image_note', 'rtd_image_path', 'message_board')
        widgets = {
            'business_trip_location': forms.TextInput(attrs={'class': 'form-control'}),
            'business_trip_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'transportation': forms.Select(choices=EBT_TRANSPORTATION_CHOICES),
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'employee_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'departure': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'bt_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'bt_image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'round_trip_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '「來回」距離'}),
            'rtd_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'rtd_image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(EBTform, self).__init__(*args, **kwargs)
        self.fields['bt_image_note'].required = False
        self.fields['bt_image_path'].required = False
        self.fields['rtd_image_note'].required = False
        self.fields['rtd_image_path'].required = False
        self.fields['message_board'].required = False


class WASTEform(forms.ModelForm):
    class Meta:
        model = waste
        fields = ('waste_name', 'waste_weigh', 'waste_date', 'waste_disposal', 'waste_location',
                  'waste_disposal_vendor', 'transport_type', 'transport_fuel', 'transport_distance', 'image_note',
                  'image_path', 'message_board')
        widgets = {
            'waste_name': forms.TextInput(attrs={'class': 'form-control'}),
            'waste_weigh': forms.TextInput(attrs={'class': 'form-control'}),
            'waste_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'waste_disposal': forms.Select(choices=WASTE_DISPOSAL_CHOICES),
            'waste_location': forms.TextInput(attrs={'class': 'form-control'}),
            'waste_disposal_vendor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入處理廠商名稱'}),
            'transport_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '僅公司責任需要填寫'}),
            'transport_fuel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '僅公司責任需要填寫'}),
            'transport_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '僅公司責任需要填寫'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'message_board': forms.Textarea(attrs={'class': 'form-control textarea', 'style': 'height: 150px; padding: 10px 20px', 'placeholder': '備註欄'})
        }

    def __init__(self, *args, **kwargs):
        super(WASTEform, self).__init__(*args, **kwargs)
        self.fields['transport_type'].required = False
        self.fields['transport_fuel'].required = False
        self.fields['transport_distance'].required = False
        self.fields['image_note'].required = False
        self.fields['image_path'].required = False
        self.fields['message_board'].required = False
