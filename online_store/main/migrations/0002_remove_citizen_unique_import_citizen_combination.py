# Generated by Django 4.1.7 on 2023-03-04 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='citizen',
            name='unique_import_citizen_combination',
        ),
    ]