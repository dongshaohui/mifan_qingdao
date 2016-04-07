# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0041_auto_20160404_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='shop_feature',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u5546\u5e97\u7279\u8272'),
            preserve_default=True,
        ),
    ]
