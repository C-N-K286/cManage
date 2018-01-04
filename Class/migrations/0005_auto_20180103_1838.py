# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-03 13:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Class', '0004_auto_20171221_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='allocated_room_variable',
            field=models.CharField(default='Room', max_length=100),
        ),
        migrations.AlterField(
            model_name='class',
            name='class_location_variable',
            field=models.CharField(default='Location', max_length=100),
        ),
        migrations.AlterField(
            model_name='class',
            name='class_name_variable',
            field=models.CharField(default='Class', max_length=250),
        ),
        migrations.AlterField(
            model_name='class',
            name='description_variable',
            field=models.CharField(default='Description', max_length=100),
        ),
        migrations.AlterField(
            model_name='class',
            name='end_date_variable',
            field=models.CharField(default='End Date', max_length=100),
        ),
        migrations.AlterField(
            model_name='class',
            name='instructor_variable',
            field=models.CharField(default='Instructor', max_length=100),
        ),
        migrations.AlterField(
            model_name='class',
            name='start_date_variable',
            field=models.CharField(default='Start Date', max_length=100),
        ),
    ]