# Generated by Django 4.0.5 on 2022-06-23 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0180_consentform_agreement_required'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_types',
            name='name',
            field=models.CharField(max_length=300, verbose_name='Name'),
        ),
    ]
