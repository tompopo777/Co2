# -*- encoding: utf-8 -*-
from django.contrib import admin
from .forms import CompanyForm
from .models import *


@admin.register(company)
# admin.site.register(company, CompanyAdmin)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'address')
    list_filter = ['parent_code']
    form = CompanyForm


@admin.register(parent)
# admin.site.register(parent, ParentAdmin)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'parent_code')
    # pass


@admin.register(factory)
# admin.site.register(factory, FactoryAdmin)
class FactoryAdmin(admin.ModelAdmin):
    pass
