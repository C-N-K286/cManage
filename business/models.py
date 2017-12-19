# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Business(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_id = models.AutoField(primary_key=True)
    phone_no = models.CharField(max_length=10)
    business = models.TextField(max_length=20,blank=False,null=False)
    typeField = models.CharField(max_length=10)
    duration = models.DurationField()
    paymentField = models.CharField(max_length=10)
    def __str__(self):
    	return str(self.business_id)


class Instructor(models.Model):
	business_id = models.ForeignKey(Business,on_delete=models.CASCADE)
	instructor_id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	middle_name = models.CharField(max_length=30)
	address = models.CharField(max_length=250)
	ssn = models.IntegerField()
	email = models.EmailField(max_length=70,blank=False, null= False, unique= True)
	telephone = models.IntegerField()