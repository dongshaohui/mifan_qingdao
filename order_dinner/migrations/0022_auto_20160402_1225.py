# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0021_auto_20160402_1145'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shop',
            old_name='valid',
            new_name='status',
        ),
    ]
