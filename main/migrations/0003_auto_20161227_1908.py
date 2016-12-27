# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-27 17:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_niceditimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostMark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('positive', models.BooleanField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(default='', max_length=16392),
        ),
        migrations.AddField(
            model_name='postmark',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Post'),
        ),
    ]