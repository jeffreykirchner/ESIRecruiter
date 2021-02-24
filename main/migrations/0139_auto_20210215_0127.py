# Generated by Django 3.1.4 on 2021-02-15 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0138_experiment_session_days_paypal_api'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameters',
            name='paypal_email_body',
            field=models.CharField(default='thanks for your participation!', max_length=200),
        ),
        migrations.AddField(
            model_name='parameters',
            name='paypal_email_subject',
            field=models.CharField(default='You have a payment from <your_org>.', max_length=200),
        ),
    ]