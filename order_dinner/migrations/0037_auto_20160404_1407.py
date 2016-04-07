# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0036_auto_20160404_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shop',
            field=models.ForeignKey(related_name='shop_order', to='order_dinner.Shop'),
            preserve_default=True,
        ),
    ]
