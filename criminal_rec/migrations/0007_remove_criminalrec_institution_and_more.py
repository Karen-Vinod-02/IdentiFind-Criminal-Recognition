# Generated by Django 5.2 on 2025-04-22 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('criminal_rec', '0006_rename_id_criminalrec_criminal_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='criminalrec',
            name='institution',
        ),
        migrations.RemoveField(
            model_name='criminalrec',
            name='parole_end_date',
        ),
        migrations.AddField(
            model_name='criminalrec',
            name='parole_status',
            field=models.TextField(blank=True, null=True),
        ),
    ]
