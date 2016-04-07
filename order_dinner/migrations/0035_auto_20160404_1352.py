# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0034_auto_20160404_1319'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='feight',
            new_name='freight',
        ),
    ]
