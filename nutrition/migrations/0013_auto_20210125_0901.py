# Generated by Django 3.1.2 on 2021-01-25 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0012_auto_20210125_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='meal',
            field=models.CharField(choices=[('breakfast', 'breakfast'), ('launch', 'launch'), ('dinner', 'dinner')], default='launch', max_length=16),
        ),
    ]
