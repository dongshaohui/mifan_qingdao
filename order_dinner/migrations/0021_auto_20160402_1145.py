# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0020_auto_20160402_1009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='addr',
        ),
        migrations.AddField(
            model_name='shop',
            name='detail_addr',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u5546\u94fa\u8be6\u7ec6\u5730\u5740'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shop',
            name='postcode',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u90ae\u7f16'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shop',
            name='search_addr',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u5546\u94fa\u641c\u7d22\u5730\u5740'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shop',
            name='valid',
            field=models.BooleanField(default=True, verbose_name='\u662f\u5426\u8425\u4e1a'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shop',
            name='remark',
            field=models.TextField(default=b'', max_length=255, verbose_name='\u5907\u6ce8\u4fe1\u606f'),
            preserve_default=True,
        ),
    ]
