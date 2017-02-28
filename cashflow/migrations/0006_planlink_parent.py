# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0005_auto_20170227_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='planlink',
            name='parent',
            field=models.ForeignKey(verbose_name=b'\xe7\x88\xb6\xe8\xae\xa1\xe5\x88\x92', to='cashflow.PlanLink', null=True),
        ),
    ]
