# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-19 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamereviews', '0034_auto_20171219_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='topgames',
            name='content',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topgames',
            name='release_date',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='topgames',
            name='title',
            field=models.CharField(max_length=20),
        ),
    ]
