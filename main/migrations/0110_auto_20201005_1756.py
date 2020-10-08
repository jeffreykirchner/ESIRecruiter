# Generated by Django 3.1.2 on 2020-10-05 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0109_help_docs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='help_docs',
            name='name',
        ),
        migrations.AddField(
            model_name='help_docs',
            name='title',
            field=models.CharField(default='', max_length=300, verbose_name='Title'),
        ),
    ]