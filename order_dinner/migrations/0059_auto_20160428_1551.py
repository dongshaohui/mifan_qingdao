# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0058_auto_20160422_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalsetting',
            name='customer_service',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u5ba2\u670d\u7535\u8bdd'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='globalsetting',
            name='policy_link',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u534f\u8bae\u94fe\u63a5\u5730\u5740'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='globalsetting',
            name='working_hours',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u5de5\u4f5c\u65f6\u95f4\u8bbe\u7f6e'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dish',
            name='dish_type',
            field=models.IntegerField(default=0, verbose_name='\u83dc\u54c1\u7c7b\u578b\uff080-\u5355\u54c1\u83dc\uff0c1-\u542b\u914d\u83dc\uff09'),
            preserve_default=True,
        ),
    ]
