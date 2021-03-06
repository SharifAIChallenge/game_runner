# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-06 22:47
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DockerFile',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='dockerfiles')),
                ('version', models.IntegerField(blank=True, editable=False)),
                ('memorylimit', models.IntegerField(help_text='maximum memory usage allowed in KBs')),
                ('cpushare', models.IntegerField(help_text='CPU shares (relative weight)')),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='sourcefiles')),
                ('dockerfile',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docker_registry.DockerFile')),
            ],
        ),
    ]
