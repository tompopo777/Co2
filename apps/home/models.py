# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User, AbstractUser
# 限制文件
from django.core import validators
from django.utils import timezone


# Create your models here.
class parent(models.Model):
    parent_code = models.CharField(max_length=255, primary_key=True)
    company_name = models.CharField(max_length=255)

    def __str__(self):
        return self.parent_code


# 公司基本資料
class company(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255, verbose_name='公司名稱')
    tax_id = models.IntegerField(verbose_name='統一編號')
    address = models.CharField(max_length=255, verbose_name='地址')
    headcount = models.IntegerField(verbose_name='員工人數')
    superintendent = models.CharField(max_length=30, verbose_name='負責人')
    contact_person = models.CharField(max_length=30, verbose_name='聯絡人')
    contact_telephone = models.CharField(max_length=60, verbose_name='聯絡人電話')
    contact_email = models.CharField(max_length=50, verbose_name='聯絡人信箱')
    industry_classification = models.CharField(max_length=30, verbose_name='行業分類')
    parent_code = models.ForeignKey(parent, on_delete=models.CASCADE, db_column='parent_code')

    def __str__(self):
        return self.company_name


# 廠基本資料
class factory(models.Model):
    id = models.AutoField(primary_key=True)
    factory_name = models.CharField(max_length=255, verbose_name='工廠名稱')
    company_id = models.ForeignKey(company, on_delete=models.CASCADE, db_column='company_id', verbose_name='總公司名稱')

    def __str__(self):
        return self.factory_name


# profile資料
class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='使用者')
    company = models.ForeignKey(company, on_delete=models.CASCADE, null=True, db_column='company', verbose_name='該帳號屬於公司名稱')
    factory = models.ForeignKey(factory, on_delete=models.CASCADE, null=True, db_column='factory', verbose_name='該帳號屬於廠名稱')

    def __str__(self):
        return self.user.username


# # 客製權限
# class CustomUser(AbstractUser):
#     company = models.ForeignKey(company, on_delete=models.CASCADE)
#     factory = models.ForeignKey(factory, on_delete=models.CASCADE, null=True, blank=True)


# # 客製權限
# # class CustomUser(AbstractUser):
# class CustomUser(models.Model):
#     # pass
#     id = models.AutoField(primary_key=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     username = models.CharField(max_length=100)
#     company = models.ForeignKey(company, on_delete=models.CASCADE)


class section_one(models.Model):
    cpid = models.AutoField(primary_key=True)
    c_name = models.IntegerField()
    p_name = models.CharField(max_length=30)


class section_two(models.Model):
    did = models.AutoField(primary_key=True)
    d_name = models.CharField(max_length=30)
    cpid = models.ForeignKey(section_one, on_delete=models.CASCADE)
    t_name = models.CharField(max_length=50)


# 柴油發電機
class emergency_generators(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=1, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    device_id = models.CharField(max_length=30)
    device_capacity = models.FloatField()
    position = models.CharField(max_length=30)
    department = models.CharField(max_length=100, null=True)
    estimate = models.BooleanField(default=False)
    january = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    february = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    march = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    april = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    may = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    june = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    july = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    august = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    september = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    october = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    november = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    december = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 燃燒設備
class combustion_equipment(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=2, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    device_name = models.CharField(max_length=50)
    device_id = models.CharField(max_length=30)
    fuel_type = models.CharField(max_length=10)
    fuel_january = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    fuel_february = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    fuel_march = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    fuel_april = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    fuel_may = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    fuel_june = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    fuel_july = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    fuel_august = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    fuel_september = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    fuel_october = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    fuel_november = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    fuel_december = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    heat_january = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    heat_february = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    heat_march = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    heat_april = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    heat_may = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    heat_june = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    heat_july = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    heat_august = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    heat_september = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    heat_october = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    heat_november = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    heat_december = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 公務車
class official_car(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=3, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    vehicle_type = models.CharField(max_length=10)
    device_id = models.CharField(max_length=30)
    fuel_type = models.CharField(max_length=30)
    department = models.CharField(max_length=100, null=True)
    metering_method = models.CharField(max_length=20)
    january = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    february = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    march = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    april = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    may = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    june = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    july = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    august = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    september = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    october = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    november = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    december = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    urea_january = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    urea_february = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    urea_march = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    urea_april = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    urea_may = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    urea_june = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    urea_july = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    urea_august = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    urea_september = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    urea_october = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    urea_november = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    urea_december = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 原物料使用
class material(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=4, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    material_name = models.CharField(max_length=20)
    material_id = models.CharField(max_length=30)
    material_type = models.CharField(max_length=10)
    chemical = models.BooleanField(default=False)
    process_add_name = models.CharField(max_length=20, null=True)
    chemical_name = models.CharField(max_length=20, null=True)
    chemical_formula = models.CharField(max_length=20, null=True)
    carbon_content = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    january = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    february = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    march = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    april = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    may = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    june = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    july = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    august = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    september = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    october = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    november = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    december = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 製成添加物
class process(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=5, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    process_add_name = models.CharField(max_length=20)
    carbon_content = models.DecimalField(max_digits=20, decimal_places=2)
    process_stage = models.CharField(max_length=20)
    material_id = models.CharField(max_length=30)
    CAS_NO = models.CharField(max_length=20)
    burn = models.BooleanField(default=False)
    VOCs = models.BooleanField(default=False)
    unit = models.CharField(max_length=20)
    january = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    february = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    march = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    april = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    may = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    june = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    july = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    august = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    september = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    october = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    november = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    december = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 冰箱清單
class refrigerator(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=6, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    device_id = models.CharField(max_length=30)
    device_name = models.CharField(max_length=30)
    brand_name = models.CharField(max_length=30, null=True)
    model_type = models.CharField(max_length=50)
    position = models.CharField(max_length=100, null=True)
    years_purchased = models.IntegerField()
    filling_volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    effusion_rate = models.FloatField()
    refrigerant_type = models.CharField(max_length=20)
    filling_fix_volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 冷氣清單
class airconditioner(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=7, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    device_id = models.CharField(max_length=30)
    device_name = models.CharField(max_length=30)
    brand_name = models.CharField(max_length=30, null=True)
    model_type = models.CharField(max_length=50)
    position = models.CharField(max_length=100, null=True)
    years_purchased = models.IntegerField()
    filling_volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    effusion_rate = models.FloatField()
    refrigerant_type = models.CharField(max_length=20)
    filling_fix_volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 車輛清單
class vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=8, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    device_id = models.CharField(max_length=30)
    device_name = models.CharField(max_length=30)
    brand_name = models.CharField(max_length=30, null=True)
    model_type = models.CharField(max_length=50)
    position = models.CharField(max_length=100, null=True)
    years_purchased = models.IntegerField()
    filling_volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    effusion_rate = models.FloatField()
    refrigerant_type = models.CharField(max_length=20)
    filling_fix_volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 飲水機清單
class water_dispenser(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=9, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    device_id = models.CharField(max_length=30)
    device_name = models.CharField(max_length=30)
    brand_name = models.CharField(max_length=30, null=True)
    model_type = models.CharField(max_length=50)
    position = models.CharField(max_length=100, null=True)
    years_purchased = models.IntegerField()
    filling_volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    effusion_rate = models.FloatField()
    refrigerant_type = models.CharField(max_length=20)
    filling_fix_volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 冰水機清單
class ice_water_dispenser(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=10, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    device_id = models.CharField(max_length=30)
    device_name = models.CharField(max_length=30)
    brand_name = models.CharField(max_length=30, null=True)
    model_type = models.CharField(max_length=50)
    position = models.CharField(max_length=100, null=True)
    years_purchased = models.IntegerField()
    filling_volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    effusion_rate = models.FloatField()
    refrigerant_type = models.CharField(max_length=20)
    filling_fix_volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 製冰機清單
class ice_maker(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=11, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    device_id = models.CharField(max_length=30)
    device_name = models.CharField(max_length=30)
    brand_name = models.CharField(max_length=30, null=True)
    model_type = models.CharField(max_length=50)
    position = models.CharField(max_length=100, null=True)
    years_purchased = models.IntegerField()
    filling_volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    effusion_rate = models.FloatField()
    refrigerant_type = models.CharField(max_length=20)
    filling_fix_volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 設備清單
class other_device(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=12, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    device_id = models.CharField(max_length=30)
    device_name = models.CharField(max_length=30)
    brand_name = models.CharField(max_length=30, null=True)
    model_type = models.CharField(max_length=50)
    position = models.CharField(max_length=100, null=True)
    years_purchased = models.IntegerField()
    filling_volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    effusion_rate = models.FloatField()
    refrigerant_type = models.CharField(max_length=20)
    filling_fix_volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 滅火器
class extinguisher(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=13, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    extinguisher_type = models.CharField(max_length=50)
    device_id = models.CharField(max_length=30, null=True)
    position = models.CharField(max_length=100)
    extinguisher_vendor = models.CharField(max_length=30, null=True)
    chemical_weight = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    inventory = models.DecimalField(max_digits=20, decimal_places=0)
    using_amount = models.IntegerField(null=True)
    monthly = models.CharField(max_length=20, null=True)
    replace_filling_amount = models.DecimalField(max_digits=20, decimal_places=0)
    replace_filling_date = models.CharField(max_length=20, null=True)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 人添清冊
class personnel_inventory(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=14, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    classification = models.CharField(max_length=30)
    WKhours_january = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_february = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_march = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_april = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_may = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_june = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_july = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_august = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_september = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_october = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_november = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_december = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKnum_january = models.IntegerField(default=0)
    WKnum_february = models.IntegerField(default=0)
    WKnum_march = models.IntegerField(default=0)
    WKnum_april = models.IntegerField(default=0)
    WKnum_may = models.IntegerField(default=0)
    WKnum_june = models.IntegerField(default=0)
    WKnum_july = models.IntegerField(default=0)
    WKnum_august = models.IntegerField(default=0)
    WKnum_september = models.IntegerField(default=0)
    WKnum_october = models.IntegerField(default=0)
    WKnum_november = models.IntegerField(default=0)
    WKnum_december = models.IntegerField(default=0)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 委外人員清冊
class employee(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=15, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    career = models.CharField(max_length=10)
    employeeNum_january = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    employeeNum_february = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    employeeNum_march = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    employeeNum_april = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    employeeNum_may = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    employeeNum_june = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    employeeNum_july = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    employeeNum_august = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    employeeNum_september = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    employeeNum_october = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    employeeNum_november = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    employeeNum_december = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    WKdays_january = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKdays_february = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKdays_march = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKdays_april = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKdays_may = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKdays_june = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKdays_july = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKdays_august = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKdays_september = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKdays_october = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKdays_november = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKdays_december = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_january = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_february = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_march = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_april = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_may = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_june = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_july = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_august = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_september = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_october = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_november = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    WKhours_december = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 廢水
class waste_water(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=16, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    Pi = models.DecimalField(max_digits=20, decimal_places=10, null=True)
    Wi = models.DecimalField(max_digits=20, decimal_places=10)
    CODi = models.DecimalField(max_digits=20, decimal_places=10)
    Si = models.DecimalField(max_digits=20, decimal_places=10)
    MCFj = models.DecimalField(max_digits=20, decimal_places=10)
    Bo = models.DecimalField(max_digits=20, decimal_places=10)
    Ri = models.DecimalField(max_digits=20, decimal_places=10)
    COD_total = models.DecimalField(max_digits=20, decimal_places=10)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 廢汙泥
class waste_sludge(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=17, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    waste_sludge_treatment_name = models.CharField(max_length=50)
    waste_sludge_inflow_rate = models.IntegerField()
    average_inlet_MLSS_concentration = models.IntegerField()
    CH4_capture_system_rate = models.FloatField()
    combustion_equipment_efficiency = models.FloatField()
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 溶劑、噴霧劑
class solvent_aerosol_emission_sources(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=18, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    solvent_name = models.CharField(max_length=100)
    solvent_amount = models.DecimalField(max_digits=20, decimal_places=0)
    solvent_capacity = models.DecimalField(max_digits=20, decimal_places=4)
    solvent_capacity_unit = models.CharField(max_length=20)
    gas_name = models.CharField(max_length=20)
    gas_ratio = models.CharField(max_length=20)
    density = models.DecimalField(max_digits=30, decimal_places=10)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 用電量
class electricity(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=21, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    EMI_id = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    january = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    february = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    march = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    april = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    may = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    june = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    july = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    august = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    september = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    october = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    november = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    december = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 上游運輸
class upstream_transportation(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=22, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    acceptance_receipt = models.CharField(max_length=50)
    commodity_name = models.CharField(max_length=20)
    weight = models.CharField(max_length=10)
    commodity_NW = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    organizational_use_products = models.CharField(max_length=100)
    customer = models.CharField(max_length=50)
    supplier = models.CharField(max_length=30)
    supplier_address = models.CharField(max_length=100)
    trade_term = models.CharField(max_length=10)
    receiving_address = models.CharField(max_length=100)
    delivery_address = models.CharField(max_length=100)
    transport_distance = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    transport_country = models.CharField(max_length=20, null=True)
    paid = models.CharField(max_length=10, null=True)
    transport_type = models.CharField(max_length=20, null=True)
    transport_fuel = models.CharField(max_length=20, null=True)
    trips = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    image_note = models.CharField(max_length=30, null=True)
    overseas_transport_distance = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    overseas_paid = models.CharField(max_length=10, null=True)
    overseas_delivery = models.CharField(max_length=50, null=True)
    overseas_arrive = models.CharField(max_length=50, null=True)
    overseas_trips = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    overseas_image_note = models.CharField(max_length=30, null=True)
    special_transport_distance = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    special_transport_country = models.CharField(max_length=20, null=True)
    special_paid = models.CharField(max_length=10, null=True)
    special_transport_type = models.CharField(max_length=20, null=True)
    special_transport_fuel = models.CharField(max_length=20, null=True)
    special_trips = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    special_image_note = models.CharField(max_length=30, null=True)
    air_transport_distance = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    air_delivery = models.CharField(max_length=50, null=True)
    air_arrive = models.CharField(max_length=50, null=True)
    air_trips = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    air_paid = models.CharField(max_length=10, null=True)
    air_image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 下游運輸
class downstream_transportation(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=23, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    acceptance_receipt = models.CharField(max_length=50)
    commodity_name = models.CharField(max_length=20)
    weight = models.CharField(max_length=10)
    commodity_NW = models.FloatField()
    customer = models.CharField(max_length=50)
    supplier = models.CharField(max_length=30)
    supplier_address = models.CharField(max_length=100)
    trade_term = models.CharField(max_length=10)
    receiving_address = models.CharField(max_length=100)
    delivery_address = models.CharField(max_length=100)
    transport_distance = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    transport_country = models.CharField(max_length=20, null=True)
    paid = models.CharField(max_length=10, null=True)
    transport_type = models.CharField(max_length=20, null=True)
    transport_fuel = models.CharField(max_length=20, null=True)
    trips = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    image_note = models.CharField(max_length=30, null=True)
    overseas_transport_distance = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    overseas_paid = models.CharField(max_length=10, null=True)
    overseas_delivery = models.CharField(max_length=50, null=True)
    overseas_arrive = models.CharField(max_length=50, null=True)
    overseas_trips = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    overseas_image_note = models.CharField(max_length=30, null=True)
    special_transport_distance = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    special_transport_country = models.CharField(max_length=20, null=True)
    special_paid = models.CharField(max_length=10, null=True)
    special_transport_type = models.CharField(max_length=20, null=True)
    special_transport_fuel = models.CharField(max_length=20, null=True)
    special_trips = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    special_image_note = models.CharField(max_length=30, null=True)
    air_transport_distance = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    air_delivery = models.CharField(max_length=50, null=True)
    air_arrive = models.CharField(max_length=50, null=True)
    air_trips = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    air_paid = models.CharField(max_length=10, null=True)
    air_image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 員工通勤
class employee_commute(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=24, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    employee_id = models.CharField(max_length=30)
    employee_name = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    work_days = models.DecimalField(max_digits=20, decimal_places=0)
    city = models.CharField(max_length=100)
    township = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    commute_distance = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 員工通勤段數
class transportation_way(models.Model):
    id = models.AutoField(primary_key=True)
    transportation = models.CharField(max_length=30)
    commute = models.ForeignKey(employee_commute, on_delete=models.CASCADE, db_column='commute_id')


# 員工出差
class employee_business_trip(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=25, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    business_trip_location = models.CharField(max_length=100)
    business_trip_date = models.CharField(max_length=30)
    business_trip_number = models.CharField(max_length=30)
    employee_id = models.CharField(max_length=30, null=True)
    employee_name = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    bt_image_note = models.CharField(max_length=30, null=True)
    rtd_image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 員工出差段數
class trip_section(models.Model):
    id = models.AutoField(primary_key=True)
    departure = models.CharField(max_length=50)
    transportation = models.CharField(max_length=30)
    distance = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    trip_id = models.ForeignKey(employee_business_trip, on_delete=models.CASCADE, db_column='trip_id')


# VOC1
class VOCs_one(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=22, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    process_stage = models.CharField(max_length=30)
    material_id = models.CharField(max_length=30)
    process_add_name = models.CharField(max_length=20, null=True)
    chemical_name = models.CharField(max_length=20, null=True)
    chemical_formula = models.CharField(max_length=20, null=True)
    purchase_volume = models.IntegerField()
    consumption = models.IntegerField()
    purchase_unit = models.CharField(max_length=20)
    CO2 = models.BooleanField(default=False)
    CH4 = models.BooleanField(default=False)
    N2O = models.BooleanField(default=False)
    HFC = models.BooleanField(default=False)
    PFC = models.BooleanField(default=False)
    SF6 = models.BooleanField(default=False)
    NF3 = models.BooleanField(default=False)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# VOC2
class VOCs_two(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=23, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    process_name = models.CharField(max_length=50)
    disposal_volume = models.DecimalField(max_digits=20, decimal_places=4)
    burn = models.CharField(max_length=20)
    concentration_entrance = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    concentration_exit = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    builtIn_rate = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    custom_rate = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    concentration_ch4 = models.FloatField()
    voc_capture_rate = models.FloatField()
    combustion_equipment_rate = models.FloatField()
    radio_VOCs = models.CharField(max_length=20)
    radio_concentration = models.CharField(max_length=20, null=True)
    radio_co2_emission = models.CharField(max_length=20, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 廢棄物
class waste(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=26, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    waste_name = models.CharField(max_length=50)
    waste_weigh = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    waste_date = models.CharField(max_length=20)
    waste_disposal = models.CharField(max_length=20)
    waste_location = models.CharField(max_length=100)
    waste_disposal_vendor = models.CharField(max_length=20)
    transport_type = models.CharField(max_length=50, null=True)
    transport_fuel = models.CharField(max_length=10, null=True)
    transport_distance = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 製程排放自動帶入的化學品表
class chemical_table(models.Model):
    chemical_add = models.CharField(primary_key=True, max_length=50)
    chemical_name = models.CharField(max_length=50)
    chemical_formula = models.CharField(max_length=50)


# 照片
class image(models.Model):
    id = models.AutoField(primary_key=True)
    table_id = models.IntegerField()
    single_id = models.IntegerField()
    stage = models.CharField(max_length=30, null=True)
    image_path = models.FileField(upload_to='images/%Y/%m', validators=[validators.FileExtensionValidator(['jpg', 'png', 'pdf'])], null=True, default=None)


# 納管廢水
class pipe_wastewater(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=27, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    pipe_id = models.CharField(max_length=225)
    address = models.CharField(max_length=225)
    factory = models.CharField(max_length=50)
    january = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    february = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    march = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    april = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    may = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    june = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    july = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    august = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    september = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    october = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    november = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    december = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 採購原物料
class purchase_material(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=28, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    product_id = models.CharField(max_length=50)
    product_name = models.CharField(max_length=50)
    vendor = models.CharField(max_length=50)
    category_name = models.CharField(max_length=100, null=True)
    material_type = models.CharField(max_length=10)
    january = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    february = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    march = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    april = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    may = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    june = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    july = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    august = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    september = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    october = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    november = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    december = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 使用產品間接排放
class product_indirect_emissions(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(section_two, on_delete=models.CASCADE, default=29, db_column='did_id')
    years = models.IntegerField(default=timezone.now().year)
    product_id = models.CharField(max_length=50)
    product_name = models.CharField(max_length=50)
    january = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    february = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    march = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    april = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    may = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    june = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    july = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    august = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    september = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    october = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    november = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    december = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    image_note = models.CharField(max_length=30, null=True)
    message_board = models.CharField(max_length=255, null=True)
    company_id = models.IntegerField()


# 固定、移動係數表表格
class coefficient(models.Model):
    id = models.AutoField(primary_key=True)
    cause = models.CharField(max_length=30)
    gas_name = models.CharField(max_length=50)
    coefficient = models.DecimalField(max_digits=20, decimal_places=10, default=0)
    coefficient_source = models.CharField(max_length=50)
    note = models.CharField(max_length=100, null=True)


# gwp係數表表格
class coefficient_gwp(models.Model):
    id = models.AutoField(primary_key=True)
    gas_name = models.CharField(max_length=30)
    version = models.IntegerField()
    years = models.IntegerField()
    gwp_coefficient = models.DecimalField(max_digits=20, decimal_places=10, default=0)


# 下拉選單
class DropdownOption(models.Model):
    id = models.AutoField(primary_key=True)
    option_group = models.CharField(max_length=100)
    option_value = models.CharField(max_length=100, null=True)
    option_label = models.CharField(max_length=100, null=True)
