# Generated by Django 5.1.4 on 2024-12-22 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='name',
            new_name='Наименование',
        ),
    ]
