# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0045_order_reject_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='name_en',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u5546\u94fa\u82f1\u6587\u540d'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shop',
            name='remark_en',
            field=models.TextField(default=b'', max_length=255, verbose_name='\u5907\u6ce8\u82f1\u6587\u4fe1\u606f'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shop',
            name='shop_feature_en',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u5546\u5e97\u7279\u8272\u82f1\u6587'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shop',
            name='name',
            field=models.CharField(max_length=255, verbose_name='\u5546\u94fa\u4e2d\u6587\u540d'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shop',
            name='remark',
            field=models.TextField(default=b'', max_length=255, verbose_name='\u5907\u6ce8\u4e2d\u6587\u4fe1\u606f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shop',
            name='shop_feature',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u5546\u5e97\u7279\u8272\u4e2d\u6587'),
            preserve_default=True,
        ),
    ]
