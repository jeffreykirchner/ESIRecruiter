# Generated by Django 4.0.7 on 2022-09-20 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0211_alter_profile_public_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiments',
            name='archived',
            field=models.BooleanField(default=False, verbose_name='Archived'),
        ),
    ]
