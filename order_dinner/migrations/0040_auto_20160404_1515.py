# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0039_order_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='consume_type',
            field=models.IntegerField(default=0, verbose_name='\u6d88\u8d39\u65b9\u5f0f'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_address',
            field=models.ForeignKey(related_name='delivery_address_order', blank=True, to='order_dinner.DeliveryAddress', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='pay_type',
            field=models.ForeignKey(related_name='user_pay_type_order', blank=True, to='order_dinner.UserPayType', null=True),
            preserve_default=True,
        ),
    ]
