# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0011_subdish_shop'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='shop',
            field=models.OneToOneField(default='', to='order_dinner.Shop'),
            preserve_default=False,
        ),
    ]
