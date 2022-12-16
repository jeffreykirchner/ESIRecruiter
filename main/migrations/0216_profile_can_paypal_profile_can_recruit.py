# Generated by Django 4.1.4 on 2022-12-15 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0215_parameters_international_tax_rate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='can_paypal',
            field=models.BooleanField(default=False, verbose_name='User can send PayPal payments'),
        ),
        migrations.AddField(
            model_name='profile',
            name='can_recruit',
            field=models.BooleanField(default=False, verbose_name='User can recruit subjects to sessions'),
        ),
    ]