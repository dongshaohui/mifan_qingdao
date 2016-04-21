# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0052_bannerimg_link'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderdish',
            options={'verbose_name': '\u8ba2\u5355\u4e2d\u7684\u83dc\u54c1', 'verbose_name_plural': '\u8ba2\u5355\u4e2d\u7684\u83dc\u54c1'},
        ),
        migrations.AlterModelOptions(
            name='userpaytype',
            options={'verbose_name': '\u7528\u6237\u652f\u4ed8\u65b9\u5f0f', 'verbose_name_plural': '\u7528\u6237\u652f\u4ed8\u65b9\u5f0f'},
        ),
        migrations.RemoveField(
            model_name='globalsetting',
            name='setting_desc',
        ),
        migrations.RemoveField(
            model_name='globalsetting',
            name='setting_key',
        ),
        migrations.RemoveField(
            model_name='globalsetting',
            name='setting_value',
        ),
        migrations.AddField(
            model_name='globalsetting',
            name='discount_rate',
            field=models.FloatField(default=0.0, verbose_name='\u6298\u6263\u7387'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='globalsetting',
            name='freight_thres',
            field=models.FloatField(default=0.0, verbose_name='\u6ee1X\u5143\u514d\u8fd0\u8d39'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='globalsetting',
            name='tax_rate',
            field=models.FloatField(default=0.08, verbose_name='\u7a0e\u7387'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='payable_price',
            field=models.FloatField(default=0.0, verbose_name='\u8ba2\u5355\u5e94\u4ed8\u4ef7\u683c'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='consume_type',
            field=models.IntegerField(default=0, verbose_name='\u6d88\u8d39\u65b9\u5f0f\uff080-\u914d\u9001\uff0c1-\u5230\u5e97\u6d88\u8d39\uff09'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='create_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u521b\u5efa\u65f6\u95f4'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(related_name='customer_order', verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe6\x89\x8b\xe6\x9c\xba', to='order_dinner.Customer'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_address',
            field=models.ForeignKey(related_name='delivery_address_order', verbose_name=b'\xe9\x80\x81\xe8\xb4\xa7\xe5\x9c\xb0\xe5\x9d\x80', blank=True, to='order_dinner.DeliveryAddress', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='order_dishes',
            field=models.ManyToManyField(to='order_dinner.OrderDish', null=True, verbose_name=b'\xe8\xae\xa2\xe5\x8d\x95\xe5\x8c\x85\xe5\x90\xab\xe8\x8f\x9c\xe5\x93\x81', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='pay_type',
            field=models.ForeignKey(verbose_name='\u652f\u4ed8\u65b9\u5f0f', blank=True, to='order_dinner.UserPayType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='shop',
            field=models.ForeignKey(related_name='shop_order', verbose_name=b'\xe5\xba\x97\xe9\x93\xba', to='order_dinner.Shop'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='tip_type',
            field=models.IntegerField(default=0, verbose_name='\u5c0f\u8d39\u65b9\u5f0f\uff080-\u5c0f\u8d39\u6bd4\u7387\uff0c1-\u73b0\u91d1\u5c0f\u8d39\uff09'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='update_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u4fee\u6539\u65f6\u95f4', auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shop',
            name='commission',
            field=models.FloatField(default=0.1, verbose_name='\u4f63\u91d1\u767e\u5206\u6bd4'),
            preserve_default=True,
        ),
    ]
