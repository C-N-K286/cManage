# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from business.models import Business,Instructor
from student.models import Student
import datetime
# Create your models here.
class Class(models.Model):
    business_id = models.ForeignKey(Business,to_field='business_id',on_delete=models.CASCADE)
    class_id = models.AutoField(primary_key=True)

    active_class = models.BooleanField()   
    class_name = models.CharField(max_length=100,blank=False,null=False,unique=True)
    class_name_variable = models.CharField(max_length=250,default='Class')

    corse_duration = models.DurationField()
    duration = models.DurationField()

    start_date = models.DateField()
    start_date_variable = models.CharField(max_length=100,default='Start Date')

    end_date = models.DateField()
    end_date_variable = models.CharField(max_length=100,default='End Date')

    class_location = models.CharField(max_length=250)
    class_location_variable = models.CharField(max_length=100,default = 'Location')

    allocated_room = models.CharField(max_length=10)
    allocated_room_variable = models.CharField(max_length=100,default='Room')
    #instructor = models.CharField(max_length=200)
    instructor = models.ManyToManyField(Instructor)
    instructor_variable = models.CharField(max_length=100,default='Instructor')

    description = models.TextField()
    description_variable = models.CharField(max_length=100,default='Description')

	
    student = models.ManyToManyField(Student)
    def __str__(self):
        return self.class_name
    def get_date(self):
        return str(self.class_name)+","+str(self.start_date)+"," + str(self.end_date)