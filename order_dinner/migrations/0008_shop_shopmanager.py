# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('order_dinner', '0007_creditcard_shop'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u5546\u94fa\u540d')),
                ('addr', models.CharField(max_length=255, verbose_name='\u5546\u94fa\u5730\u5740')),
                ('mobile', models.CharField(max_length=255, verbose_name='\u8054\u7cfb\u4eba\u7535\u8bdd')),
                ('remark', models.CharField(max_length=255, verbose_name='\u5907\u6ce8\u4fe1\u606f')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShopManager',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('shop', models.OneToOneField(to='order_dinner.Shop')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
        ),
    ]
