# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashloopplan',
            name='content',
            field=models.TextField(default=b'', verbose_name=b'\xe8\xaf\xa6\xe7\xbb\x86\xe4\xbb\x8b\xe7\xbb\x8d'),
        ),
        migrations.AddField(
            model_name='cashloopplan',
            name='enable',
            field=models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\x90\xaf\xe7\x94\xa8'),
        ),
        migrations.AddField(
            model_name='cashloopplan',
            name='end_date',
            field=models.DateTimeField(default=None, null=True, verbose_name=b'\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AddField(
            model_name='cashloopplan',
            name='name',
            field=models.CharField(default=b'', max_length=100, verbose_name=b'\xe8\xae\xa1\xe5\x88\x92\xe5\x90\x8d\xe7\xa7\xb0'),
        ),
        migrations.AddField(
            model_name='cashloopplan',
            name='start_date',
            field=models.DateTimeField(default=None, verbose_name=b'\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AddField(
            model_name='daikuan',
            name='content',
            field=models.TextField(default=b'', verbose_name=b'\xe8\xaf\xa6\xe7\xbb\x86\xe4\xbb\x8b\xe7\xbb\x8d'),
        ),
        migrations.AddField(
            model_name='daikuan',
            name='enable',
            field=models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\x90\xaf\xe7\x94\xa8'),
        ),
        migrations.AddField(
            model_name='daikuan',
            name='end_date',
            field=models.DateTimeField(default=None, null=True, verbose_name=b'\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AddField(
            model_name='daikuan',
            name='name',
            field=models.CharField(default=b'', max_length=100, verbose_name=b'\xe8\xae\xa1\xe5\x88\x92\xe5\x90\x8d\xe7\xa7\xb0'),
        ),
        migrations.AddField(
            model_name='daikuan',
            name='start_date',
            field=models.DateTimeField(default=None, verbose_name=b'\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4'),
        ),
    ]
