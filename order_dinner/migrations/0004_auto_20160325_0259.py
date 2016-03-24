# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0003_auto_20160325_0255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subdish',
            name='name',
            field=models.CharField(max_length=255, verbose_name='\u914d\u83dc\u540d'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subdish',
            name='price',
            field=models.FloatField(default=0.0, verbose_name='\u914d\u83dc\u5355\u4ef7'),
            preserve_default=True,
        ),
    ]
