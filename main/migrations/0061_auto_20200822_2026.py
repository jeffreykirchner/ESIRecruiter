# Generated by Django 3.0.7 on 2020-08-22 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0060_auto_20200822_1958'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='profile',
        #     name='emailFilters',
        # ),
        migrations.AddField(
            model_name='profile',
            name='emailFilter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.emailFilter', verbose_name='Email Filters'),
        ),
        migrations.AlterField(
            model_name='emailfilter',
            name='domain',
            field=models.CharField(max_length=300, verbose_name='Domain, ex: abc.edu'),
        ),
        migrations.AlterField(
            model_name='emailfilter',
            name='name',
            field=models.CharField(max_length=300, verbose_name='Name'),
        ),
    ]
