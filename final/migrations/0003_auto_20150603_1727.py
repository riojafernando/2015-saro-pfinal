# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0002_ultimafecha'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UltimaFecha',
            new_name='FechaActualizada',
        ),
    ]
