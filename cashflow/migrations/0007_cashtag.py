# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0006_planlink_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total', models.FloatField(default=0, verbose_name=b'\xe5\xbd\x93\xe5\x89\x8d\xe9\x87\x91\xe9\xa2\x9d')),
                ('dt', models.DateTimeField(verbose_name=b'dt')),
            ],
            options={
                'ordering': ('-dt',),
            },
        ),
    ]
