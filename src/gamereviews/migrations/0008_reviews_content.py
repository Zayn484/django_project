# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-14 13:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamereviews', '0007_auto_20171207_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
