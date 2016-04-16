# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0048_auto_20160413_1054'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('setting_key', models.CharField(default=b'\xe8\xae\xbe\xe7\xbd\xae\xe5\x8f\x98\xe9\x87\x8f\xe5\x90\x8d', max_length=255, verbose_name='\u8bbe\u7f6e\u53d8\u91cf\u540d')),
                ('setting_value', models.FloatField(default=0.0, verbose_name='\u503c')),
            ],
            options={
                'verbose_name': '\u5168\u5c40\u8bbe\u7f6e',
                'verbose_name_plural': '\u5168\u5c40\u8bbe\u7f6e',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShopBusinessStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('desc', models.CharField(max_length=255, verbose_name='\u72b6\u6001\u63cf\u8ff0')),
                ('status_tag', models.IntegerField(default=1, verbose_name='\u662f\u5426\u8425\u4e1a')),
            ],
            options={
                'verbose_name': '\u5546\u94fa\u8425\u4e1a\u72b6\u6001',
                'verbose_name_plural': '\u5546\u94fa\u8425\u4e1a\u72b6\u6001',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['-create_time'], 'verbose_name': '\u7528\u6237', 'verbose_name_plural': '\u7528\u6237'},
        ),
        migrations.AlterModelOptions(
            name='deliveryaddress',
            options={'verbose_name': '\u6536\u8d27\u5730\u5740', 'verbose_name_plural': '\u6536\u8d27\u5730\u5740'},
        ),
        migrations.AlterModelOptions(
            name='dish',
            options={'verbose_name': '\u83dc\u54c1', 'verbose_name_plural': '\u83dc\u54c1'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-create_time'], 'verbose_name': '\u8ba2\u5355', 'verbose_name_plural': '\u8ba2\u5355'},
        ),
        migrations.AlterModelOptions(
            name='shop',
            options={'verbose_name': '\u5546\u5e97', 'verbose_name_plural': '\u5546\u5e97'},
        ),
        migrations.AlterModelOptions(
            name='subdish',
            options={'verbose_name': '\u914d\u83dc', 'verbose_name_plural': '\u914d\u83dc'},
        ),
        migrations.AlterField(
            model_name='bannerimg',
            name='priority',
            field=models.IntegerField(default=0, verbose_name='\u4f18\u5148\u7ea7(\u4f18\u5148\u7ea7\u9ad8\u7684\u4f18\u5148\u663e\u793a)'),
            preserve_default=True,
        ),
    ]
