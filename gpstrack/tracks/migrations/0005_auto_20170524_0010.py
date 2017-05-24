# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-24 00:10
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('tracks', '0004_auto_20170519_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='track',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='points',
                                    to='tracks.Track'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='time',
            name='local_time',
            field=models.DateTimeField(),
            preserve_default=False,
        ),
    ]
