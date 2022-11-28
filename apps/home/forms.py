from django import forms
from .models import emergency_generators, combustion_equipment


class EGform(forms.ModelForm):

    class Meta:
        model = emergency_generators
        fields = ('device_id', 'period_starttime', 'period_endtime', 'device_capacity', 'position', 'department', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'image_note', 'image_path')
        widgets = {
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'value': '123456789'}),
            'period_starttime': forms.DateInput(attrs={'type': 'date'}),
            'period_endtime': forms.DateInput(attrs={'type': 'date'}),
            'device_capacity': forms.NumberInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': '只能輸入數字', 'placeholder': '單位:公升'}),
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
        fields = ('device_name', 'device_id', 'fuel_type', 'period_starttime', 'period_endtime', 'fuel_january', 'fuel_february', 'fuel_march', 'fuel_april', 'fuel_may', 'fuel_june', 'fuel_july', 'fuel_august', 'fuel_september', 'fuel_october', 'fuel_november', 'fuel_december', 'heat_january', 'heat_february', 'heat_march', 'heat_april', 'heat_may', 'heat_june', 'heat_july', 'heat_august', 'heat_september', 'heat_october', 'heat_november', 'heat_december', 'image_note', 'image_path')
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

