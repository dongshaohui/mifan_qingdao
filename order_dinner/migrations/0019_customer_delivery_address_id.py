# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0018_auto_20160402_0010'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='delivery_address_id',
            field=models.IntegerField(default=0, verbose_name='\u6536\u8d27\u5730\u5740ID'),
            preserve_default=True,
        ),
    ]
