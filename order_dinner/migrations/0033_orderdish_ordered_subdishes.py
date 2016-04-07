# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0032_auto_20160404_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdish',
            name='ordered_subdishes',
            field=models.ManyToManyField(to='order_dinner.Subdish', null=True, blank=True),
            preserve_default=True,
        ),
    ]
