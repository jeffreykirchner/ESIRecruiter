# Generated by Django 3.0.7 on 2020-09-19 23:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0098_auto_20200919_2306'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='emailFilter',
            new_name='email_filter',
        ),
        migrations.RenameField(
            model_name='schools',
            old_name='emailFilter',
            new_name='email_filter',
        ),
    ]
