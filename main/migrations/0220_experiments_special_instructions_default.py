# Generated by Django 4.1.7 on 2023-03-22 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0219_remove_experiment_sessions_allowed_list_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiments',
            name='special_instructions_default',
            field=models.CharField(default='', max_length=300),
        ),
    ]
