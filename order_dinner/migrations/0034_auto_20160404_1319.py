# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0033_orderdish_ordered_subdishes'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderSubDish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subdish_order_number', models.IntegerField(default=0, verbose_name='\u5b50\u83dc\u54c1\u70b9\u5355\u6b21\u6570')),
                ('subdish', models.OneToOneField(to='order_dinner.Subdish')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='orderdish',
            name='dish',
            field=models.OneToOneField(related_name='order_dish', to='order_dinner.Dish'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderdish',
            name='ordered_subdishes',
            field=models.ManyToManyField(to='order_dinner.OrderSubDish', null=True, blank=True),
            preserve_default=True,
        ),
    ]
