# Generated by Django 5.2.1 on 2025-05-14 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='deleted_at',
        ),
    ]
