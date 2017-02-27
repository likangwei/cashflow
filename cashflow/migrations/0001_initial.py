# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plan_id', models.IntegerField(verbose_name=b'plan id')),
                ('changed_money', models.FloatField(verbose_name=b'\xe6\x94\xaf\xe5\x87\xba\xe6\x88\x96\xe6\x94\xb6\xe5\x85\xa5')),
                ('dt', models.DateTimeField(verbose_name=b'\xe6\x97\xb6\xe9\x97\xb4')),
                ('remark', models.CharField(max_length=255, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8')),
                ('content_type', models.ForeignKey(verbose_name=b'content_type', to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['dt'],
            },
        ),
        migrations.CreateModel(
            name='CashLoopPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cron', models.CharField(default=b'0 0 1 * *', max_length=100, verbose_name=b'cron')),
                ('cash_per_time', models.FloatField(verbose_name=b'\xe5\x8d\x95\xe6\xac\xa1\xe6\x94\xb6\xe6\x94\xaf')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DaiKuan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cron', models.CharField(default=b'0 0 1 * *', max_length=100, verbose_name=b'cron')),
                ('daikuan_total', models.FloatField(verbose_name=b'\xe8\xb4\xb7\xe6\xac\xbe\xe6\x9c\xac\xe9\x87\x91')),
                ('daikuan_yihuan', models.TextField(verbose_name=b'\xe8\xb4\xb7\xe6\xac\xbe\xe5\xb7\xb2\xe8\xbf\x98')),
                ('daikuan_shoufu', models.FloatField(verbose_name=b'\xe8\xb4\xb7\xe6\xac\xbe\xe9\xa6\x96\xe4\xbb\x98')),
                ('daikuan_nianlilv', models.FloatField(verbose_name=b'\xe8\xb4\xb7\xe6\xac\xbe\xe5\xb9\xb4\xe5\x88\xa9\xe7\x8e\x87')),
                ('daikuan_years', models.IntegerField(default=0, verbose_name=b'\xe8\xb4\xb7\xe6\xac\xbe\xe5\xb9\xb4\xe9\x99\x90')),
                ('daikuan_months', models.IntegerField(default=0, verbose_name=b'\xe8\xb4\xb7\xe6\xac\xbe\xe6\x9c\x88\xe6\x95\xb0')),
                ('daikuan_type', models.CharField(default=b'debj', max_length=100, verbose_name=b'\xe8\xb4\xb7\xe6\xac\xbe\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'debj', b'\xe7\xad\x89\xe9\xa2\x9d\xe6\x9c\xac\xe9\x87\x91'), (b'debx', b'\xe7\xad\x89\xe9\xa2\x9d\xe6\x9c\xac\xe6\x81\xaf')])),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
