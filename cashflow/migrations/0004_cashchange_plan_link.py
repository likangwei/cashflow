# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0003_auto_20170227_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashchange',
            name='plan_link',
            field=models.ForeignKey(default=None, verbose_name=b'plan', to='cashflow.PlanLink'),
            preserve_default=False,
        ),
    ]
