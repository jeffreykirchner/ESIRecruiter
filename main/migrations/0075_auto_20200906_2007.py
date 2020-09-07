# Generated by Django 3.0.7 on 2020-09-06 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0074_auto_20200903_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='nonresidentAlien',
            field=models.BooleanField(default=False, verbose_name='Nonresident Alien'),
        ),
        migrations.AddField(
            model_name='profile',
            name='w9Collected',
            field=models.BooleanField(default=False, verbose_name='W9 Form Collected'),
        ),
    ]
