# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-08-25 08:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0005_auto_20190824_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talks',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '审核通过'), (1, '审核中'), (-1, '审核失败')], default=1, verbose_name='状态'),
        ),
    ]