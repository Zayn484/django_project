# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-07 12:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamereviews', '0004_reviews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='img',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='info',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
