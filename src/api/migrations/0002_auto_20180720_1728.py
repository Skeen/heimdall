# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-07-20 17:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='password',
            name='signature',
            field=models.CharField(default='', max_length=2000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='password',
            name='signing_key',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, related_name='signatures', to='api.PublicKey'),
            preserve_default=False,
        ),
    ]