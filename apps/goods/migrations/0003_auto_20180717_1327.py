# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-17 13:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20180717_1324'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goodscategorybrand',
            old_name='catetory',
            new_name='category',
        ),
    ]
