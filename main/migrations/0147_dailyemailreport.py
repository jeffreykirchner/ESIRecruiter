# Generated by Django 3.2 on 2021-09-28 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0146_profile_send_daily_email_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyEmailReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=10000, verbose_name='Text')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Daily Email Report',
                'verbose_name_plural': 'Daily Email Report',
                'ordering': ['timestamp'],
            },
        ),
    ]
