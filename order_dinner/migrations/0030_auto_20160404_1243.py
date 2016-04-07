# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0029_auto_20160404_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='dishes',
            field=models.ManyToManyField(to='order_dinner.Dish', null=True, blank=True),
            preserve_default=True,
        ),
    ]
