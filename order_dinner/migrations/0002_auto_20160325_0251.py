# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='create_time',
            field=models.DateTimeField(default='1990-01-01', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='update_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
