# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0044_auto_20160407_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='reject_reason',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u8ba2\u5355\u53d6\u6d88\u539f\u56e0'),
            preserve_default=True,
        ),
    ]
