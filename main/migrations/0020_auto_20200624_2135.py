# Generated by Django 3.0.7 on 2020-06-24 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20200624_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment_sessions',
            name='experience_max',
            field=models.IntegerField(default=1000),
        ),
        migrations.AddField(
            model_name='experiment_sessions',
            name='experience_min',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='experiments',
            name='experience_max_defualt',
            field=models.IntegerField(default=1000),
        ),
        migrations.AddField(
            model_name='experiments',
            name='experience_min_defualt',
            field=models.IntegerField(default=0),
        ),
    ]
