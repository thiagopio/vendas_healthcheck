# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthcheck', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='related_project',
            field=models.ManyToManyField(to='healthcheck.Project'),
        ),
        migrations.AlterField(
            model_name='project',
            name='environment',
            field=models.CharField(max_length=10, choices=[(b'DEV', b'DEV'), (b'QA', b'QA'), (b'PROD', b'PROD')]),
        ),
    ]
