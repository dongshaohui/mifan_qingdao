# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0014_remove_creditcard_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPayType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pay_type', models.IntegerField(default=0, verbose_name='\u652f\u4ed8\u65b9\u5f0f')),
                ('credit_card', models.CharField(max_length=255, verbose_name='\u4fe1\u7528\u5361\u53f7')),
                ('security_code', models.CharField(max_length=255, verbose_name='\u4fe1\u7528\u5b89\u5168\u7801')),
                ('expire_year', models.CharField(max_length=255, verbose_name='\u8fc7\u671f\u5e74\u4efd')),
                ('expire_month', models.CharField(max_length=255, verbose_name='\u8fc7\u671f\u6708\u4efd')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
