# Generated by Django 3.0.7 on 2020-08-12 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0055_auto_20200812_1658'),
    ]

    operations = [
        migrations.RenameField(
            model_name='experiment_sessions',
            old_name='recruitmentParamsDefault',
            new_name='recruitmentParams',
        ),
    ]