# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-22 09:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_inventory', '0020_auto_20170222_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 2, 22, 17, 51, 33, 60282), verbose_name='Date'),
        ),
    ]
