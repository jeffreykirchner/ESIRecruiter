# Generated by Django 3.0.7 on 2020-07-20 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_auto_20200720_1603'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parameters',
            old_name='timeZone',
            new_name='subjectTimeZone',
        ),
    ]
