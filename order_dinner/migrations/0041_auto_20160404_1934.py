# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0040_auto_20160404_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='latitude',
            field=models.FloatField(default=0.0, verbose_name='\u7eac\u5ea6'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shop',
            name='longitude',
            field=models.FloatField(default=0.0, verbose_name='\u7ecf\u5ea6'),
            preserve_default=True,
        ),
    ]
