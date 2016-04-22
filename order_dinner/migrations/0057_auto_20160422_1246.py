# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0056_shop_registration_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerimg',
            name='link',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name='\u8d85\u94fe\u63a5', blank=True),
            preserve_default=True,
        ),
    ]
