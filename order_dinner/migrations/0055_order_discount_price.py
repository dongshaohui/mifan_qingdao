# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0054_order_commission_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount_price',
            field=models.FloatField(default=0.0, verbose_name='\u6298\u6263\u91d1\u989d'),
            preserve_default=True,
        ),
    ]
