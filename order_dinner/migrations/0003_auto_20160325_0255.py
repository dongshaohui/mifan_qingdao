# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0002_auto_20160325_0251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='create_time',
            field=models.DateTimeField(auto_now=True, verbose_name='\u521b\u5efa\u65f6\u95f4'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='mobile',
            field=models.CharField(max_length=255, verbose_name='\u7528\u6237\u624b\u673a'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=255, verbose_name='\u7528\u6237\u540d'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='password',
            field=models.CharField(max_length=255, verbose_name='\u7528\u6237\u5bc6\u7801'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='update_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u4fee\u6539\u65f6\u95f4'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='valid',
            field=models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u7528'),
            preserve_default=True,
        ),
    ]
