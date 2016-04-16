# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0049_auto_20160414_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalsetting',
            name='setting_desc',
            field=models.CharField(default=b'\xe5\x8f\x98\xe9\x87\x8f\xe6\x8f\x8f\xe8\xbf\xb0', max_length=255, verbose_name='\u53d8\u91cf\u63cf\u8ff0'),
            preserve_default=True,
        ),
    ]
