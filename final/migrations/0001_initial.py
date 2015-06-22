# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.TextField()),
                ('tipo', models.TextField()),
                ('precio', models.TextField()),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('larga_dur', models.TextField()),
                ('url', models.TextField()),
                ('fecha_usuario', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=32)),
                ('titulo_usuario', models.TextField()),
                ('actividades', models.ManyToManyField(to='final.Actividad')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
