# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('cashflow', '0002_auto_20170227_0644'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plan_id', models.IntegerField(verbose_name=b'plan id')),
                ('content_type', models.ForeignKey(verbose_name=b'content_type', to='contenttypes.ContentType')),
            ],
        ),
        migrations.RemoveField(
            model_name='cashchange',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='cashchange',
            name='plan_id',
        ),
    ]
