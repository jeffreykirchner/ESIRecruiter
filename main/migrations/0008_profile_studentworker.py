# Generated by Django 2.2.10 on 2020-06-07 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_profile_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='studentWorker',
            field=models.BooleanField(default=False),
        ),
    ]
