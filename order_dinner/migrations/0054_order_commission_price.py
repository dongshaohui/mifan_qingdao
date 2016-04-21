# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0053_auto_20160421_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='commission_price',
            field=models.FloatField(default=0.0, verbose_name='\u4f63\u91d1'),
            preserve_default=True,
        ),
    ]
