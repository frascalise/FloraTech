# Generated by Django 5.1.2 on 2025-03-17 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('timestamp', models.DateTimeField(primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=50)),
                ('temp_min', models.FloatField()),
                ('temp_max', models.FloatField()),
                ('precipitations', models.CharField(max_length=50)),
                ('precipitations_mm', models.FloatField()),
            ],
        ),
    ]
