# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0009_auto_20160325_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='commission',
            field=models.FloatField(default=0.0, verbose_name='\u4f63\u91d1\u767e\u5206\u6bd4'),
            preserve_default=True,
        ),
    ]
