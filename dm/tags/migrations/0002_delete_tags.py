# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-06 19:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tags',
        ),
    ]
