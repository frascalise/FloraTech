# Generated by Django 5.1.2 on 2025-04-08 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_garden_plants_alter_garden_moisture'),
    ]

    operations = [
        migrations.AddField(
            model_name='garden',
            name='status',
            field=models.CharField(default='working', max_length=50),
        ),
    ]
