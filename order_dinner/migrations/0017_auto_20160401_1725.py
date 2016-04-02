# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0016_userpaytype_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpaytype',
            name='customer',
            field=models.ForeignKey(related_name='customer_user_pay_types', to='order_dinner.Customer'),
            preserve_default=True,
        ),
    ]
