# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0028_auto_20160404_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='dishes',
            field=models.ManyToManyField(to='order_dinner.Dish'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='shop',
            field=models.OneToOneField(default='', to='order_dinner.Shop'),
            preserve_default=False,
        ),
    ]
