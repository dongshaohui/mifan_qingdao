# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0037_auto_20160404_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdish',
            name='dish',
            field=models.ForeignKey(related_name='order_dish', to='order_dinner.Dish'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ordersubdish',
            name='subdish',
            field=models.ForeignKey(to='order_dinner.Subdish'),
            preserve_default=True,
        ),
    ]
