# Generated by Django 3.0.7 on 2020-08-11 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0053_auto_20200811_1854'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiments',
            name='actual_participants_legacy',
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AddField(
            model_name='experiments',
            name='registration_cutoff_legacy',
            field=models.IntegerField(default=1, null=True),
        ),
    ]
