# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0059_auto_20160428_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='dish_img',
            field=models.ImageField(upload_to=b'imgs/', null=True, verbose_name='\u83dc\u54c1\u56fe\u7247', blank=True),
            preserve_default=True,
        ),
    ]
