# Generated by Django 3.1.4 on 2021-01-30 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0136_auto_20210116_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment_session_days',
            name='reminder_email_sent_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]