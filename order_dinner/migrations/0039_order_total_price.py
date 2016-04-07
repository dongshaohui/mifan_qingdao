# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0038_auto_20160404_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.FloatField(default=0.0, verbose_name='\u8ba2\u5355\u603b\u4ef7\u683c'),
            preserve_default=True,
        ),
    ]
