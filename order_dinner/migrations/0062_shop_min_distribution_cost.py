# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0061_auto_20160429_0353'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='min_distribution_cost',
            field=models.FloatField(default=0.0, verbose_name='\u6700\u4f4e\u914d\u9001\u8d39\u7528'),
            preserve_default=True,
        ),
    ]
