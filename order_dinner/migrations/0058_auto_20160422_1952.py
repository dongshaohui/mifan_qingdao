# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0057_auto_20160422_1246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payable_price',
        ),
        migrations.AddField(
            model_name='order',
            name='origin_price',
            field=models.FloatField(default=0, verbose_name='\u83dc\u54c1\u603b\u4ef7\u683c'),
            preserve_default=True,
        ),
    ]
