# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0063_auto_20160504_2216'),
    ]

    operations = [
        migrations.CreateModel(
            name='DishCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=255, verbose_name='\u7c7b\u522b\u540d\u79f0')),
                ('shop', models.ForeignKey(verbose_name=b'\xe9\x80\x89\xe5\x8f\x96\xe5\xba\x97\xe9\x93\xba', to='order_dinner.Shop')),
            ],
            options={
                'verbose_name': '\u83dc\u54c1\u7c7b\u578b',
                'verbose_name_plural': '\u83dc\u54c1\u7c7b\u578b',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='globalsetting',
            name='short_message_username',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u63a5\u53d7\u65b0\u5355\u77ed\u4fe1\u7528\u6237\u540d'),
            preserve_default=True,
        ),
    ]
