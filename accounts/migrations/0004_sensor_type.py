# Generated by Django 5.1.2 on 2025-04-02 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_sensor_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='type',
            field=models.CharField(default='sensor', max_length=50),
        ),
    ]
