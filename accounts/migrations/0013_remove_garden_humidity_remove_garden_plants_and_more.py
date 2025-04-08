# Generated by Django 5.1.2 on 2025-04-08 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_remove_garden_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='garden',
            name='humidity',
        ),
        migrations.RemoveField(
            model_name='garden',
            name='plants',
        ),
        migrations.RemoveField(
            model_name='garden',
            name='temperature',
        ),
        migrations.RemoveField(
            model_name='garden',
            name='water',
        ),
        migrations.AddField(
            model_name='garden',
            name='moisture',
            field=models.JSONField(default=1),
            preserve_default=False,
        ),
    ]
