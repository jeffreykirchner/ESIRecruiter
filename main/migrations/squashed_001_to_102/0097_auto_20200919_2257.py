# Generated by Django 3.0.7 on 2020-09-19 22:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0096_auto_20200919_0438'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='subjectType',
            new_name='subject_type',
        ),
    ]
