# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0005_auto_20160325_0312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='mobile',
            field=models.CharField(max_length=255, verbose_name='\u624b\u673a'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dish',
            name='subdishes',
            field=models.ManyToManyField(to='order_dinner.Subdish', null=True, blank=True),
            preserve_default=True,
        ),
    ]
