# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0027_auto_20160404_1050'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerificationCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mobile', models.CharField(max_length=255, verbose_name='\u624b\u673a')),
                ('verification_code', models.CharField(default=b'', max_length=255, verbose_name='\u624b\u673a\u9a8c\u8bc1\u7801')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='customer',
            name='verification_code',
        ),
    ]
