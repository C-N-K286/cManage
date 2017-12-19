# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.AutoField(primary_key=True)
    phone_no = models.CharField(max_length=10)
    typeField = models.CharField(max_length=10)
    
    def __str__(self):
        return str(self.student_id) + ','+str (self.phone_no)+','+str(self.typeField)