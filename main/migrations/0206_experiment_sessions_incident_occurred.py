# Generated by Django 4.0.6 on 2022-09-09 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0205_remove_consentform_irb_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment_sessions',
            name='incident_occurred',
            field=models.BooleanField(default=False),
        ),
    ]
