# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0023_auto_20160402_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='dish_type',
            field=models.IntegerField(default=0, verbose_name='\u83dc\u54c1\u7c7b\u578b'),
            preserve_default=True,
        ),
    ]
