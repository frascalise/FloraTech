# Generated by Django 5.1.3 on 2025-01-14 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telematry', '0002_rename_telematry_data_telematrydata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telematrydata',
            name='received_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
