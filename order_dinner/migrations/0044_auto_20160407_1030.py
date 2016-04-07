# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_dinner', '0043_shop_business_hour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='shop_img',
            field=models.ImageField(upload_to=b'imgs/', verbose_name='\u5546\u94fa\u56fe\u7247'),
            preserve_default=True,
        ),
    ]
