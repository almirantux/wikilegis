# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-09 17:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20170308_1630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='reporting_member',
        ),
    ]
