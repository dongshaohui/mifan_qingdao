# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0062_shop_min_distribution_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalsetting',
            name='short_message_mobile',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u63a5\u53d7\u65b0\u5355\u77ed\u4fe1\u7535\u8bdd'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shopmanager',
            name='shop',
            field=models.OneToOneField(null=True, blank=True, to='order_dinner.Shop'),
            preserve_default=True,
        ),
    ]
