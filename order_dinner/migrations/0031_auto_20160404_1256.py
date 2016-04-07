# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0030_auto_20160404_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dish', models.ForeignKey(related_name='order_dish', to='order_dinner.Dish')),
                ('ordered_subdishes', models.ManyToManyField(to='order_dinner.Subdish', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='order',
            name='dishes',
        ),
        migrations.AddField(
            model_name='order',
            name='order_dishes',
            field=models.ManyToManyField(to='order_dinner.OrderDish', null=True, blank=True),
            preserve_default=True,
        ),
    ]
