# Generated by Django 5.2 on 2025-04-11 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_water_id_alter_water_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='water',
            name='id',
        ),
        migrations.AlterField(
            model_name='water',
            name='timestamp',
            field=models.DateTimeField(primary_key=True, serialize=False),
        ),
    ]
