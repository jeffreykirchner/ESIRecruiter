# Generated by Django 3.1.4 on 2021-01-01 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0124_front_page_notice'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='password_reset_key',
            field=models.UUIDField(blank=True, null=True, verbose_name='Password Reset Key'),
        ),
    ]
