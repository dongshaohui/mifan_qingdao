# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0026_auto_20160403_1659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='dish',
        ),
        migrations.AddField(
            model_name='customer',
            name='verification_code',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u624b\u673a\u9a8c\u8bc1\u7801'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='distance',
            field=models.FloatField(default=0.0, verbose_name='\u8ba2\u5355\u8ddd\u79bb'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='feight',
            field=models.FloatField(default=0.0, verbose_name='\u8ba2\u5355\u8fd0\u8d39'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='remark',
            field=models.CharField(default='', max_length=255, verbose_name='\u8ba2\u5355\u5907\u6ce8'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='tax',
            field=models.FloatField(default=0.0, verbose_name='\u8ba2\u5355\u7a0e\u8d39'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='tip',
            field=models.FloatField(default=0.0, verbose_name='\u8ba2\u5355\u5c0f\u8d39'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='tip_type',
            field=models.IntegerField(default=0, verbose_name='\u5c0f\u8d39\u65b9\u5f0f'),
            preserve_default=True,
        ),
    ]
