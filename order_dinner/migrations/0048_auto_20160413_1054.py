# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0047_auto_20160411_1053'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerImg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=255, verbose_name='\u8f6e\u64ad\u56fe\u7247\u540d')),
                ('img', models.ImageField(upload_to=b'imgs/', verbose_name='\u8f6e\u64ad\u56fe\u7247')),
                ('priority', models.IntegerField(default=0, verbose_name='\u83dc\u54c1\u7c7b\u578b')),
            ],
            options={
                'ordering': ['-priority'],
                'verbose_name': '\u8f6e\u64ad\u56fe',
                'verbose_name_plural': '\u8f6e\u64ad\u56fe',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='dish',
            name='shop',
            field=models.ForeignKey(related_name='shop_dish', verbose_name=b'\xe9\x80\x89\xe5\x8f\x96\xe5\xba\x97\xe9\x93\xba', to='order_dinner.Shop'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dish',
            name='subdishes',
            field=models.ManyToManyField(to='order_dinner.Subdish', null=True, verbose_name=b'\xe9\x80\x89\xe5\x8f\x96\xe5\xad\x90\xe8\x8f\x9c\xe5\x93\x81', blank=True),
            preserve_default=True,
        ),
    ]
