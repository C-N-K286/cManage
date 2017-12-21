# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-11 16:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('business', '0001_initial'),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('class_id', models.AutoField(primary_key=True, serialize=False)),
                ('class_name', models.CharField(max_length=100, unique=True)),
                ('corse_duration', models.DurationField()),
                ('duration', models.DurationField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('class_location', models.CharField(max_length=250)),
                ('allocated_room', models.CharField(max_length=10)),
                ('instructor', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('business_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.Business')),
                ('student', models.ManyToManyField(to='student.Student')),
            ],
        ),
    ]
