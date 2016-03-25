# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0006_auto_20160325_0324'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cardno', models.CharField(max_length=255, verbose_name='\u4fe1\u7528\u5361\u53f7')),
                ('expire_month', models.CharField(max_length=255, verbose_name='\u8fc7\u671f\u6708\u4efd')),
                ('expire_year', models.CharField(max_length=255, verbose_name='\u8fc7\u671f\u5e74\u4efd')),
                ('security_code', models.CharField(max_length=255, verbose_name='\u4fe1\u7528\u5b89\u5168\u7801')),
                ('customer', models.OneToOneField(to='order_dinner.Customer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        
    ]
