# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-07 17:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Class', '0005_auto_20180103_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='active_class',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
