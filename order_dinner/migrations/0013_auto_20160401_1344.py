# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0012_dish_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u7528\u6237\u540d'),
            preserve_default=True,
        ),
    ]
