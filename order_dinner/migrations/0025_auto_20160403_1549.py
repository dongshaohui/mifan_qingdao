# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0024_dish_dish_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subdish',
            name='shop',
            field=models.ForeignKey(to='order_dinner.Shop'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpaytype',
            name='customer',
            field=models.ForeignKey(related_name='customer_userpaytype', to='order_dinner.Customer'),
            preserve_default=True,
        ),
    ]
