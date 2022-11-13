from django import forms


class EGform(forms.Form):
    device_id = forms.CharField(label='設備編號', max_length=10)
    period_starttime = forms.DateField(label='燃料使用開始時間')
    period_endttime = forms.DateField(label='燃料使用結束時間')
    device_capacity = forms.CharField(label='發電機容量', max_length=30)
    position = forms.CharField(label='設置地點', max_length=30)
    department = forms.CharField(label='所屬單位', max_length=100)
    january = forms.FloatField()
    february = forms.FloatField()
    march = forms.FloatField()
    april = forms.FloatField()
    may = forms.FloatField()
    june = forms.FloatField()
    july = forms.FloatField()
    august = forms.FloatField()
    september = forms.FloatField()
    october = forms.FloatField()
    november = forms.FloatField()
    december = forms.FloatField()
    image_note = forms.CharField(label='上傳引用單據', max_length=30)
    image_path = forms.CharField(max_length=100)
