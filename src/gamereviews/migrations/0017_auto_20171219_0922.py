# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-19 04:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamereviews', '0016_auto_20171219_0859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='category',
        ),
        migrations.AddField(
            model_name='news',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
