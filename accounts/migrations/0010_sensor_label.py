# Generated by Django 5.1.2 on 2025-04-08 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_garden_plants'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='label',
            field=models.CharField(default='sensor', max_length=50),
        ),
    ]
