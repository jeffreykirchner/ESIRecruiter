# Generated by Django 4.0.7 on 2022-10-07 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0214_remove_profile_nonresidentalien_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameters',
            name='international_tax_rate',
            field=models.DecimalField(decimal_places=2, default=0.3, max_digits=5),
        ),
        migrations.AlterField(
            model_name='profile',
            name='international_student',
            field=models.BooleanField(default=False, verbose_name='International Student'),
        ),
    ]
