# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0019_customer_delivery_address_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryaddress',
            name='receiver_name',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u6536\u8d27\u4eba\u59d3\u540d'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deliveryaddress',
            name='receiver_phone',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u6536\u8d27\u4eba\u624b\u673a'),
            preserve_default=True,
        ),
    ]
