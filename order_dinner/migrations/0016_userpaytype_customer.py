# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0015_userpaytype'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpaytype',
            name='customer',
            field=models.ForeignKey(related_name='customer_userpaytype', default='', to='order_dinner.Customer'),
            preserve_default=False,
        ),
    ]
