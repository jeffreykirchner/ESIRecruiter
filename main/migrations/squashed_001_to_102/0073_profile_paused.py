# Generated by Django 3.0.7 on 2020-08-28 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0072_auto_20200828_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='paused',
            field=models.BooleanField(default=False, verbose_name='Paused'),
        ),
    ]
