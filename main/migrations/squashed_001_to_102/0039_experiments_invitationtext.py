# Generated by Django 3.0.7 on 2020-07-21 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0038_auto_20200721_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiments',
            name='invitationText',
            field=models.CharField(default='', max_length=10000),
        ),
    ]
