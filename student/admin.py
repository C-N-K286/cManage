# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.
from student.models import Student

class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'student'
class UserAdmin(BaseUserAdmin):
    inlines = (StudentInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin) 
admin.site.register(Student)