# Generated by Django 5.2 on 2025-04-22 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('criminal_rec', '0005_alter_criminalrec_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='criminalrec',
            old_name='id',
            new_name='criminal_id',
        ),
    ]
