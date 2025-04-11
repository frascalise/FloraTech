# Generated by Django 5.1.2 on 2025-04-11 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_sensor_fk_raspberry_alter_sensor_idsensor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('ONION', 'Onion'), ('TOMATO', 'Tomato'), ('SUGARCANE', 'Sugarcane'), ('COTTON', 'Cotton'), ('MUSTARD', 'Mustard'), ('WHEAT', 'Wheat'), ('BEAN', 'Bean'), ('CITRUS', 'Citrus'), ('MAIZE', 'Maize'), ('MELON', 'Melon'), ('RICE', 'Rice'), ('POTATO', 'Potato'), ('CABBAGE', 'Cabbage'), ('SOYBEAN', 'Soybean'), ('BANANA', 'Banana')], max_length=20)),
            ],
        ),
    ]
