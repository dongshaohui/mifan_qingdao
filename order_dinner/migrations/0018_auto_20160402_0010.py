# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0017_auto_20160401_1725'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('searched_address', models.CharField(default=b'', max_length=255, verbose_name='\u641c\u7d22\u5f97\u51fa\u5730\u5740')),
                ('longitude', models.FloatField(default=0.0, verbose_name='\u7ecf\u5ea6')),
                ('latitude', models.FloatField(default=0.0, verbose_name='\u7eac\u5ea6')),
                ('detail_address', models.CharField(default=b'', max_length=255, verbose_name='\u8be6\u7ec6\u5730\u5740')),
                ('postcode', models.CharField(default=b'', max_length=255, verbose_name='\u90ae\u7f16')),
                ('customer', models.ForeignKey(related_name='customer_delivery_address', to='order_dinner.Customer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='customer',
            name='user_pay_type_id',
            field=models.IntegerField(default=0, verbose_name='\u652f\u4ed8\u65b9\u5f0fID'),
            preserve_default=True,
        ),
    ]
