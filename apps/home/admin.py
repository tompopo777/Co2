# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .forms import *
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
    list_filter = ['parent_code']
    # pass


@admin.register(factory)
# admin.site.register(factory, FactoryAdmin)
class FactoryAdmin(admin.ModelAdmin):
    list_display = ('factory_name', )
    list_filter = ['company_id']
    # pass


@admin.register(Profile)
# admin.site.register(Profile, ProfileAdmin)
class ProfileAdmin(admin.ModelAdmin):
    # list_display = ('id', '')
    # list_filter = ['company_id']
    pass


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class MyUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
