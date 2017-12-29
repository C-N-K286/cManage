# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.
from business.models import Business,Instructor

class BusinessInline(admin.StackedInline):
    model = Business
    can_delete = False
    verbose_name_plural = 'business'
class UserAdmin(BaseUserAdmin):
    inlines = (BusinessInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Instructor)
admin.site.register(Business)