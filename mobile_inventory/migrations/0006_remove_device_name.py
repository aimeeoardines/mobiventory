# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-14 17:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_inventory', '0005_auto_20170209_1835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='name',
        ),
    ]
