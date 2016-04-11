# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0046_auto_20160411_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='name_en',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u82f1\u6587\u83dc\u540d'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='subdish',
            name='name_en',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u914d\u83dc\u82f1\u6587\u540d'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dish',
            name='name',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u4e2d\u6587\u83dc\u540d'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subdish',
            name='name',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u914d\u83dc\u4e2d\u6587\u540d'),
            preserve_default=True,
        ),
    ]
