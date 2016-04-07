# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0042_shop_shop_feature'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='business_hour',
            field=models.CharField(default='', max_length=255, verbose_name='\u8425\u4e1a\u65f6\u95f4'),
            preserve_default=False,
        ),
    ]
