# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-15 07:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamereviews', '0012_reviews_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='imgs',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
