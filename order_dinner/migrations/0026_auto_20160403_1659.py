# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0025_auto_20160403_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='status',
            field=models.IntegerField(default=True, verbose_name='\u662f\u5426\u8425\u4e1a'),
            preserve_default=True,
        ),
    ]
