# Generated by Django 2.2.10 on 2020-06-08 17:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20200607_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment_sessions',
            name='experience_level',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='main.experience_levels'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(default='', max_length=100, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
