# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-03-29 18:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpage_tour', '0003_auto_20190329_1847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='holidaytour',
            name='holiday',
        ),
        migrations.DeleteModel(
            name='HolidayTour',
        ),
    ]
