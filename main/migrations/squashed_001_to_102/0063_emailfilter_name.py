# Generated by Django 3.0.7 on 2020-08-22 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0062_remove_emailfilter_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailfilter',
            name='name',
            field=models.CharField(default='Chapman', max_length=300, verbose_name='Name'),
            preserve_default=False,
        ),
    ]
