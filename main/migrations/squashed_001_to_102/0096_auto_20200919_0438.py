# Generated by Django 3.0.7 on 2020-09-19 04:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0095_auto_20200919_0430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment_session_days',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='experiment_session_days',
            name='date_end',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
