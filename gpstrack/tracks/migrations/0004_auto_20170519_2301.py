# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-19 23:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('tracks', '0003_auto_20170509_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='velocity',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
