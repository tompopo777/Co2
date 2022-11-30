from django import forms
from .models import *


class EGform(forms.ModelForm):

    class Meta:
        model = emergency_generators
        fields = ('device_id', 'period_starttime', 'period_endtime', 'device_capacity', 'position', 'department',
                  'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
                  'november', 'december', 'image_note', 'image_path')
        widgets = {
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'value': '123456789'}),
            'period_starttime': forms.DateInput(attrs={'type': 'date'}),
            'period_endtime': forms.DateInput(attrs={'type': 'date'}),
            'device_capacity': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off',
                                                      'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '單位:公升'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'value': '資訊管理系'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'value': '管理學院'}),
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
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'value': 'test'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'})
        }


class CEform(forms.ModelForm):

    class Meta:
        model = combustion_equipment
        fields = ('device_name', 'device_id', 'fuel_type', 'period_starttime', 'period_endtime', 'fuel_january',
                  'fuel_february', 'fuel_march', 'fuel_april', 'fuel_may', 'fuel_june', 'fuel_july', 'fuel_august',
                  'fuel_september', 'fuel_october', 'fuel_november', 'fuel_december', 'heat_january', 'heat_february',
                  'heat_march', 'heat_april', 'heat_may', 'heat_june', 'heat_july', 'heat_august', 'heat_september',
                  'heat_october', 'heat_november', 'heat_december', 'image_note', 'image_path')
        widgets = {
            'device_name': forms.TextInput(attrs={'class': 'form-control', 'value': '123456789'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'value': '123456789'}),
            'fuel_type': forms.TextInput(attrs={'class': 'form-control', 'value': '123456789'}),
            'period_starttime': forms.DateInput(attrs={'type': 'date'}),
            'period_endtime': forms.DateInput(attrs={'type': 'date'}),
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
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'value': 'test'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'})
        }

class OFform(forms.ModelForm):

    class Meta:
        model = official_car
        fields = ('vehicle_type', 'device_id', 'fuel_type', 'period_starttime', 'period_endtime', 'department',
                  'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
                  'november', 'december', 'image_note', 'image_path', 'urea', 'urea_add_quantity', 'urea_add_date',
                  'urea_image_note', 'urea_image_path')
        widgets = {
            'vehicle_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '如:汽車、堆高機...等'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '只能輸入數字'}),
            'fuel_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'period_starttime': forms.DateInput(attrs={'type': 'date'}),
            'period_endtime': forms.DateInput(attrs={'type': 'date'}),
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
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'}),
            'urea': forms.CheckboxInput(attrs={'class': 'checkbox form-check-input'}),
            'urea_add_quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '單位:公升'}),
            'urea_add_date': forms.DateInput(attrs={'type': 'date'}),
            'urea_image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'urea_image_path': forms.FileInput(attrs={'class': 'form-control-file'})
        }

class MTform(forms.ModelForm):

    class Meta:
        model = material
        fields = ('material_name', 'material_id', 'material_type', 'january', 'february', 'march', 'april', 'may',
                  'june', 'july', 'august', 'september', 'october', 'november', 'december')
        widgets = {
            'material_name': forms.TextInput(attrs={'class': 'form-control'}),
            'material_id': forms.TextInput(attrs={'class': 'form-control'}),
            'material_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex. 原料/物料'}),
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
            'december': forms.TextInput(attrs={'class': 'col-6', 'value': '0'})
        }

class PCform(forms.ModelForm):

    class Meta:
        model = process
        fields = ('process_add_name', 'chemical_name', 'chemical_formula', 'process_stage', 'material_id', 'CAS_NO',
                  'burn', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
                  'october', 'november', 'december', 'image_note', 'image_path')
        widgets = {
            'process_add_name': forms.TextInput(attrs={'class': 'form-control'}),
            'chemical_name': forms.TextInput(attrs={'class': 'form-control'}),
            'chemical_formula': forms.TextInput(attrs={'class': 'form-control'}),
            'process_stage': forms.TextInput(attrs={'class': 'form-control'}),
            'material_id': forms.TextInput(attrs={'class': 'form-control'}),
            'CAS_NO': forms.TextInput(attrs={'class': 'form-control'}),
            'burn': forms.TextInput(attrs={'class': 'form-control'}),
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
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'})
        }

class RFform(forms.ModelForm):

    class Meta:
        model = refrigerator
        fields = ('device_name', 'device_id', 'brand_name', 'model_type', 'years', 'position', 'refrigerant_type',
                  'filling_volume', 'filling_fix_volume', 'filling_date', 'effusion_rate', 'image_note', 'image_path')
        widgets = {
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'years': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex. 2022'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'refrigerant_type': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'filling_date': forms.DateInput(attrs={'type': 'date'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'})
        }


class ACform(forms.ModelForm):
    class Meta:
        model = airconditioner
        fields = ('device_name', 'device_id', 'brand_name', 'model_type', 'years', 'position', 'refrigerant_type',
                  'filling_volume', 'filling_fix_volume', 'filling_date', 'effusion_rate', 'image_note', 'image_path')
        widgets = {
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'years': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex. 2022'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'refrigerant_type': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'filling_date': forms.DateInput(attrs={'type': 'date'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'})
        }


class VCform(forms.ModelForm):
    class Meta:
        model = vehicle
        fields = ('device_name', 'device_id', 'brand_name', 'model_type', 'years', 'position', 'refrigerant_type',
                  'filling_volume', 'filling_fix_volume', 'filling_date', 'effusion_rate', 'image_note', 'image_path')
        widgets = {
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'years': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex. 2022'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'refrigerant_type': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'filling_date': forms.DateInput(attrs={'type': 'date'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'})
        }


class WDform(forms.ModelForm):
    class Meta:
        model = water_dispenser
        fields = ('device_name', 'device_id', 'brand_name', 'model_type', 'years', 'position', 'refrigerant_type',
                  'filling_volume', 'filling_fix_volume', 'filling_date', 'effusion_rate', 'image_note', 'image_path')
        widgets = {
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'years': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex. 2022'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'refrigerant_type': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'filling_date': forms.DateInput(attrs={'type': 'date'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'})
        }


class IWDform(forms.ModelForm):
    class Meta:
        model = ice_water_dispenser
        fields = ('device_name', 'device_id', 'brand_name', 'model_type', 'years', 'position', 'refrigerant_type',
                  'filling_volume', 'filling_fix_volume', 'filling_date', 'effusion_rate', 'image_note', 'image_path')
        widgets = {
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'years': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex. 2022'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'refrigerant_type': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'filling_date': forms.DateInput(attrs={'type': 'date'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'})
        }


class IMform(forms.ModelForm):
    class Meta:
        model = ice_maker
        fields = ('device_name', 'device_id', 'brand_name', 'model_type', 'years', 'position', 'refrigerant_type',
                  'filling_volume', 'filling_fix_volume', 'filling_date', 'effusion_rate', 'image_note', 'image_path')
        widgets = {
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'years': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex. 2022'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'refrigerant_type': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'filling_date': forms.DateInput(attrs={'type': 'date'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'})
        }


class ODform(forms.ModelForm):
    class Meta:
        model = other_device
        fields = ('device_name', 'device_id', 'brand_name', 'model_type', 'years', 'position', 'refrigerant_type',
                  'filling_volume', 'filling_fix_volume', 'filling_date', 'effusion_rate', 'image_note', 'image_path')
        widgets = {
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'years': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex. 2022'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'refrigerant_type': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'filling_date': forms.DateInput(attrs={'type': 'date'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'})
        }


class RTTform(forms.ModelForm):
    class Meta:
        model = refrigerant_total_table
        fields = ('device_name', 'device_id', 'brand_name', 'model_type', 'years', 'position', 'refrigerant_type',
                  'filling_volume', 'filling_fix_volume', 'filling_date', 'effusion_rate', 'image_note', 'image_path')
        widgets = {
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'device_id': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'model_type': forms.TextInput(attrs={'class': 'form-control'}),
            'years': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex. 2022'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'refrigerant_type': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
            'filling_date': forms.DateInput(attrs={'type': 'date'}),
            'effusion_rate': forms.TextInput(attrs={'class': 'form-control'}),
            'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control-file'})
        }


# class ACform(forms.ModelForm):
#     class Meta:
#         model = airconditioner
#         fields = ('device_name', 'device_id', 'brand_name', 'model_type', 'years', 'position', 'refrigerant_type',
#                   'filling_volume', 'filling_fix_volume', 'filling_date', 'effusion_rate', 'image_note', 'image_path')
#         widgets = {
#             'device_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'device_id': forms.TextInput(attrs={'class': 'form-control'}),
#             'brand_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
#             'model_type': forms.TextInput(attrs={'class': 'form-control'}),
#             'years': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex. 2022'}),
#             'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
#             'refrigerant_type': forms.TextInput(attrs={'class': 'form-control'}),
#             'filling_volume': forms.TextInput(attrs={'class': 'form-control'}),
#             'filling_fix_volume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '非必填'}),
#             'filling_date': forms.DateInput(attrs={'type': 'date'}),
#             'effusion_rate': forms.TextInput(attrs={'class': 'form-control'}),
#             'image_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單據名稱'}),
#             'image_path': forms.FileInput(attrs={'class': 'form-control-file'})
#         }
