# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0008_shop_shopmanager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='remark',
            field=models.TextField(max_length=255, verbose_name='\u5907\u6ce8\u4fe1\u606f'),
            preserve_default=True,
        ),
    ]
