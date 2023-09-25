import decimal

from import_export import resources, fields
from import_export.widgets import DecimalWidget

from .models import *


class EmergencyGeneratorsResource(resources.ModelResource):
    device_id = fields.Field(attribute='device_id', column_name='緊急發電機編號')
    device_capacity = fields.Field(attribute='device_capacity', column_name='緊急發電機容量\n(千瓦)', widget=DecimalWidget())
    # device_capacity = fields.Field(attribute='device_capacity', column_name='device_capacity', widget=DecimalWidget())
    position = fields.Field(attribute='position', column_name='設置地點')
    department = fields.Field(attribute='department', column_name='所屬單位')
    estimate = fields.Field(attribute='estimate', column_name='是否推估')
    # january = fields.Field(attribute='january', column_name='1月', widget=DecimalWidget())
    january = fields.Field(attribute='january', column_name='數量 (公升)', widget=DecimalWidget())
    february = fields.Field(attribute='february', column_name='2月', widget=DecimalWidget())
    march = fields.Field(attribute='march', column_name='3月', widget=DecimalWidget())
    april = fields.Field(attribute='april', column_name='4月', widget=DecimalWidget())
    may = fields.Field(attribute='may', column_name='5月', widget=DecimalWidget())
    june = fields.Field(attribute='june', column_name='6月', widget=DecimalWidget())
    july = fields.Field(attribute='july', column_name='7月', widget=DecimalWidget())
    august = fields.Field(attribute='august', column_name='8月', widget=DecimalWidget())
    september = fields.Field(attribute='september', column_name='9月', widget=DecimalWidget())
    october = fields.Field(attribute='october', column_name='10月', widget=DecimalWidget())
    november = fields.Field(attribute='november', column_name='11月', widget=DecimalWidget())
    december = fields.Field(attribute='december', column_name='12月', widget=DecimalWidget())
    company_id = fields.Field(attribute='company_id')

    def __init__(self, factory_id, *args, **kwargs):
        self.factory_id = factory_id
        super().__init__(**kwargs)

    class Meta:
        model = emergency_generators
        fields = ('device_id', 'device_capacity', 'position', 'department',
                  # 'estimate',
                  'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
                  'november', 'december',
                  # 'image_note', 'message_board'
                  'company_id',
                  )
        exclude = (
            # 'id',
            'did', 'years', 'image_note', 'message_board', 'company_id', 'estimate', 'image_note', 'message_board',
                   # 'company_id',
                   )
        skip_unchanged = False
        report_skipped = True
        import_id_fields = ('device_id',)

    def before_import_row(self, row, row_number=None, **kwargs):
        factory_id = self.factory_id
        row['company_id'] = factory_id  # Set a default value

        february = row.get('2月')
        if february:
            # print('january')
            try:
                row['2月'] = decimal.Decimal(february)
            except:
                raise ValueError(f"輸入格式有誤! (序號={row_number}，欄位2月)")
        march = row.get('3月')
        if march:
            # print('january')
            try:
                row['2月'] = decimal.Decimal(march)
            except:
                raise ValueError(f"輸入格式有誤! (序號={row_number}，欄位2月)")


        # if "是否推估" in row.keys():
        #     if row["是否推估"] == "是":
        #         row["是否推估"] = True
        #     if row["是否推估"] == "否":
        #         row["是否推估"] = False

    # def clean_january(self, value, row):
    #     print('clean')
    #     try:
    #         return decimal.Decimal(value)
    #     except Exception as e:
    #         raise ValueError(f"Error converting '{value}' to Decimal: {str(e)}")
