# Generated by Django 3.0.7 on 2020-09-17 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0084_auto_20200917_0304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject_types',
            name='initialValue',
            field=models.BooleanField(default=False, verbose_name='Default to On'),
        ),
    ]