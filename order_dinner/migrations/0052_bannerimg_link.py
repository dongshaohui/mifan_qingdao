# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0051_auto_20160418_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='bannerimg',
            name='link',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u8d85\u94fe\u63a5'),
            preserve_default=True,
        ),
    ]
