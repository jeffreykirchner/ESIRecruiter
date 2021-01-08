# Generated by Django 3.1.4 on 2021-01-08 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0129_experiment_session_days_custom_reminder_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameters',
            name='emailVerificationResetText',
            field=models.CharField(default='', max_length=10000),
        ),
        migrations.AddField(
            model_name='parameters',
            name='emailVerificationTextSubject',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
