# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0022_auto_20160402_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='shop_img',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u5546\u94fa\u56fe\u7247'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dish',
            name='shop',
            field=models.ForeignKey(related_name='shop_dish', to='order_dinner.Shop'),
            preserve_default=True,
        ),
    ]
