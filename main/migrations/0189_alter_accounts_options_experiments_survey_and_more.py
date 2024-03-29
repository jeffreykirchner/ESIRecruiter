# Generated by Django 4.0.6 on 2022-07-19 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0188_alter_accounts_options_alter_departments_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accounts',
            options={'ordering': ['department__name', 'number'], 'verbose_name': 'Account', 'verbose_name_plural': 'Accounts'},
        ),
        migrations.AddField(
            model_name='experiments',
            name='survey',
            field=models.BooleanField(default=False, verbose_name='Survey'),
        ),
        migrations.AlterField(
            model_name='accounts',
            name='outside_funding',
            field=models.BooleanField(default=False, verbose_name='Outside Funding'),
        ),
    ]
