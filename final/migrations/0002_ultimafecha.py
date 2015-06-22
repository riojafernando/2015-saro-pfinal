# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UltimaFecha',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
