# Generated by Django 3.1.4 on 2021-01-16 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0135_parameters_testemailaccount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created On'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated On'),
        ),
    ]
