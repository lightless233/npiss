# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-01 12:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine_app', '0002_pissimages_local_filename'),
    ]

    operations = [
        migrations.AddField(
            model_name='pissimages',
            name='qiniu_filename',
            field=models.CharField(default=None, max_length=64, unique=True),
        ),
    ]
