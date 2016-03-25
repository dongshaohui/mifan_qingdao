# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0004_auto_20160325_0259'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='create_time',
            field=models.DateTimeField(default='1990-01-01', verbose_name='\u521b\u5efa\u65f6\u95f4', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='update_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u4fee\u6539\u65f6\u95f4'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dish',
            name='dish_img',
            field=models.ImageField(upload_to=b'imgs/', verbose_name='\u83dc\u54c1\u56fe\u7247'),
            # preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dish',
            name='name',
            field=models.CharField(max_length=255, verbose_name='\u83dc\u540d'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dish',
            name='price',
            field=models.FloatField(default=0.0, verbose_name='\u83dc\u54c1\u4ef7\u683c'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(max_length=255, verbose_name='\u8ba2\u5355\u72b6\u6001'),
            preserve_default=True,
        ),
    ]
