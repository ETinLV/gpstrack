# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-04 23:43
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('tracks', '0002_auto_20170426_1539'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='point',
            options={'ordering': ['time__UTC_time']},
        ),
        migrations.AlterField(
            model_name='message',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location',
                                    to='tracks.Location'),
        ),
        migrations.AlterField(
            model_name='message',
            name='time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time',
                                    to='tracks.Time'),
        ),
        migrations.AlterField(
            model_name='point',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='points',
                                    to='tracks.Location'),
        ),
        migrations.AlterField(
            model_name='point',
            name='time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='points',
                                    to='tracks.Time'),
        ),
        migrations.AlterField(
            model_name='time',
            name='UTC_time',
            field=models.DateTimeField(db_index=True),
        ),
    ]
