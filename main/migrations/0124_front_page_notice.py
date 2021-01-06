# Generated by Django 3.1.4 on 2020-12-31 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0123_auto_20201224_2058'),
    ]

    operations = [
        migrations.CreateModel(
            name='Front_page_notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_text', models.CharField(default='', max_length=1000, verbose_name='Subject Text')),
                ('body_text', models.CharField(default='', max_length=10000, verbose_name='Body Text')),
                ('enabled', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Front Page Notice',
                'verbose_name_plural': 'Front Page Notices',
            },
        ),
    ]