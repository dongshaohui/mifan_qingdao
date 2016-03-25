# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0010_shop_commission'),
    ]

    operations = [
        migrations.AddField(
            model_name='subdish',
            name='shop',
            field=models.OneToOneField(default=10, to='order_dinner.Shop'),
            preserve_default=False,
        ),
    ]
