# Generated by Django 3.0.7 on 2020-09-07 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0075_auto_20200906_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameters',
            name='maxAnnualEarnings',
            field=models.IntegerField(default=600),
        ),
    ]
