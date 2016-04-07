# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0031_auto_20160404_1256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdish',
            name='ordered_subdishes',
        ),
        migrations.AddField(
            model_name='orderdish',
            name='dish_order_number',
            field=models.IntegerField(default=0, verbose_name='\u83dc\u54c1\u70b9\u5355\u6b21\u6570'),
            preserve_default=True,
        ),
    ]
