# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0004_cashchange_plan_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashchange',
            name='plan_link',
            field=models.ForeignKey(verbose_name=b'plan_link', to='cashflow.PlanLink'),
        ),
        migrations.AlterUniqueTogether(
            name='planlink',
            unique_together=set([('content_type', 'plan_id')]),
        ),
    ]
