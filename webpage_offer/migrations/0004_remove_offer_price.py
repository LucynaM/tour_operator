# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-02 18:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpage_offer', '0003_news'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='price',
        ),
    ]
