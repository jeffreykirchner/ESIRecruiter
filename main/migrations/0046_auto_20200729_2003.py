# Generated by Django 3.0.7 on 2020-07-29 20:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0045_auto_20200729_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment_session_messages',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='experiment_session_messages',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
