# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0060_auto_20160428_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='dish_order_checkout_thres',
            field=models.FloatField(default=0.0, verbose_name='\u83dc\u54c1\u6210\u83dc\u4ef7\u683c\u4e0b\u9650\uff08\u53ea\u5bf9\u542b\u914d\u83dc\u6709\u6548\uff09'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dish',
            name='dish_img',
            field=models.ImageField(default='', upload_to=b'imgs/', verbose_name='\u83dc\u54c1\u56fe\u7247'),
            preserve_default=False,
        ),
    ]
