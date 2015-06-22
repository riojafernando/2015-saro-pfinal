# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0003_auto_20150603_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='fecha',
            field=models.DateField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actividad',
            name='fecha_usuario',
            field=models.DateField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actividad',
            name='hora',
            field=models.TimeField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actividad',
            name='larga_dur',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actividad',
            name='precio',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actividad',
            name='tipo',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actividad',
            name='titulo',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actividad',
            name='url',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuario',
            name='actividades',
            field=models.ManyToManyField(to='final.Actividad', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuario',
            name='titulo_usuario',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
