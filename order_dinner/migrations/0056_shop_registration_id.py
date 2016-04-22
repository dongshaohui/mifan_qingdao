# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0055_order_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='registration_id',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u6781\u5149\u63a8\u9001ID'),
            preserve_default=True,
        ),
    ]
