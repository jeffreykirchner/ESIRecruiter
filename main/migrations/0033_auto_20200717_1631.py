# Generated by Django 3.0.7 on 2020-07-17 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_experiment_sessions_showupfee_legacy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiments',
            name='showUpFee',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=10),
        ),
    ]
