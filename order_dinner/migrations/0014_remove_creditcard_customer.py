# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0013_auto_20160401_1344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditcard',
            name='customer',
        ),
    ]
