# Generated by Django 5.1.2 on 2025-04-08 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_garden_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='garden',
            name='name',
        ),
    ]
