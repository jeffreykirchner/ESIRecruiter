# Generated by Django 3.0.7 on 2020-09-16 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0079_experiment_session_day_users_addedbyuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment_session_day_users',
            name='manuallyAdded',
            field=models.BooleanField(default=False),
        ),
    ]
