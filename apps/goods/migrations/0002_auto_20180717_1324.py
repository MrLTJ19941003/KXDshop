# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-17 13:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goodscategorybrand',
            old_name='cagetory',
            new_name='catetory',
        ),
    ]
