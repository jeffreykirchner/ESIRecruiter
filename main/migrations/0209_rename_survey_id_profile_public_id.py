# Generated by Django 4.0.7 on 2022-09-15 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0208_profile_survey_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='survey_id',
            new_name='public_id',
        ),
    ]
