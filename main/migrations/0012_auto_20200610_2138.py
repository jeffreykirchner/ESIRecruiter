# Generated by Django 2.2.10 on 2020-06-10 21:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20200608_1746'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accounts',
            options={'verbose_name': 'Account', 'verbose_name_plural': 'Accounts'},
        ),
        migrations.AlterModelOptions(
            name='accounttypes',
            options={'verbose_name': 'Account Type', 'verbose_name_plural': 'Account Types'},
        ),
        migrations.AlterModelOptions(
            name='departments',
            options={'verbose_name': 'Department', 'verbose_name_plural': 'Departments'},
        ),
        migrations.AlterModelOptions(
            name='experience_levels',
            options={'verbose_name': 'Experience Levels', 'verbose_name_plural': 'Experience Levels'},
        ),
        migrations.AlterModelOptions(
            name='experiment_session_day_users',
            options={'verbose_name': 'Experiment Session Day Users', 'verbose_name_plural': 'Experiment Session Day Users'},
        ),
        migrations.AlterModelOptions(
            name='experiment_session_days',
            options={'verbose_name': 'Experiment Session Days', 'verbose_name_plural': 'Experiment Session Days'},
        ),
        migrations.AlterModelOptions(
            name='experiment_sessions',
            options={'verbose_name': 'Experiment Sessions', 'verbose_name_plural': 'Experiment Sessions'},
        ),
        migrations.AlterModelOptions(
            name='experiments',
            options={'verbose_name': 'Experiment', 'verbose_name_plural': 'Experiments'},
        ),
        migrations.AlterModelOptions(
            name='genders',
            options={'verbose_name': 'Gender', 'verbose_name_plural': 'Genders'},
        ),
        migrations.AlterModelOptions(
            name='institutions',
            options={'verbose_name': 'Institution', 'verbose_name_plural': 'Institutions'},
        ),
        migrations.AlterModelOptions(
            name='locations',
            options={'verbose_name': 'Location', 'verbose_name_plural': 'Locations'},
        ),
        migrations.AlterModelOptions(
            name='majors',
            options={'verbose_name': 'Major', 'verbose_name_plural': 'Majors'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Profile', 'verbose_name_plural': 'Profiles'},
        ),
        migrations.AlterModelOptions(
            name='schools',
            options={'verbose_name': 'School', 'verbose_name_plural': 'Schools'},
        ),
        migrations.AlterModelOptions(
            name='subject_types',
            options={'verbose_name': 'Subject Type', 'verbose_name_plural': 'Subject Types'},
        ),
        migrations.AlterField(
            model_name='experiment_session_day_users',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ESDU', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(default='', max_length=100),
        ),
    ]
