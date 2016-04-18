# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0050_globalsetting_setting_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpaytype',
            name='customer',
            field=models.ForeignKey(related_name='customer_userpaytype', blank=True, to='order_dinner.Customer', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpaytype',
            name='pay_type',
            field=models.IntegerField(default=0, verbose_name='\u652f\u4ed8\u65b9\u5f0f\uff080-\u4fe1\u7528\u5361\uff0c1-\u8d27\u5230\u4ed8\u6b3e\uff09'),
            preserve_default=True,
        ),
    ]
