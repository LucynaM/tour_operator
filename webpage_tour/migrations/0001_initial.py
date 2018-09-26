# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-26 10:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('webpage_offer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=15)),
                ('last_name', models.CharField(max_length=30)),
                ('phone', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('offer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tours', to='webpage_offer.Offer')),
            ],
        ),
        migrations.CreateModel(
            name='TourParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('reserved', 'reserved'), ('confirmed', 'confirmed'), ('cancelled', 'cancelled')], default='reserved', max_length=20)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='webpage_tour.Participant')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tours', to='webpage_tour.Tour')),
            ],
        ),
    ]
