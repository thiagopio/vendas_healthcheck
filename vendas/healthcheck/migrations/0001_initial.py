# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('url', models.URLField(max_length=100)),
                ('environment', models.CharField(max_length=10, choices=[(0, b'DEV'), (1, b'QA'), (2, b'PROD')])),
            ],
        ),
    ]
