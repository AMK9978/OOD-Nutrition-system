# Generated by Django 3.1.2 on 2020-12-09 11:49

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0003_auto_20201117_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodreserve',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 9, 11, 49, 34, 975378)),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('6598e5ba-83fb-4cb0-92df-c9474659fe1c'), editable=False, primary_key=True, serialize=False),
        ),
    ]
