# Generated by Django 3.0.7 on 2020-09-19 04:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0094_auto_20200919_0415'),
    ]

    operations = [
        migrations.RenameField(
            model_name='experiments',
            old_name='recruitmentParamsDefault',
            new_name='recruitment_params_default',
        ),
    ]
