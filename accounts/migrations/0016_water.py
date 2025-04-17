# Generated by Django 5.2 on 2025-04-11 13:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_garden_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Water',
            fields=[
                ('timestamp', models.DateTimeField(primary_key=True, serialize=False)),
                ('waterQuantity', models.FloatField()),
                ('fk_garden', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.garden')),
            ],
        ),
    ]
