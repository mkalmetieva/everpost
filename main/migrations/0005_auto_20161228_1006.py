# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-28 08:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20161227_1929'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postmark',
            name='author',
        ),
        migrations.RemoveField(
            model_name='postmark',
            name='post',
        ),
        migrations.RemoveField(
            model_name='post',
            name='rating',
        ),
        migrations.DeleteModel(
            name='PostMark',
        ),
    ]
