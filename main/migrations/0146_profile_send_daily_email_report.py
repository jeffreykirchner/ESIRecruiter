# Generated by Django 3.2 on 2021-09-28 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0145_experiment_sessions_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='send_daily_email_report',
            field=models.BooleanField(default=False, verbose_name='Send Daily Email Report'),
        ),
    ]
