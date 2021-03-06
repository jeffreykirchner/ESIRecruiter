# Generated by Django 3.0.7 on 2020-08-12 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0054_auto_20200811_1905'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiment_sessions',
            name='actual_participants',
        ),
        migrations.RemoveField(
            model_name='experiment_sessions',
            name='allow_multiple_participations',
        ),
        migrations.RemoveField(
            model_name='experiment_sessions',
            name='experience_constraint',
        ),
        migrations.RemoveField(
            model_name='experiment_sessions',
            name='experience_max',
        ),
        migrations.RemoveField(
            model_name='experiment_sessions',
            name='experience_min',
        ),
        migrations.RemoveField(
            model_name='experiment_sessions',
            name='experiments_exclude',
        ),
        migrations.RemoveField(
            model_name='experiment_sessions',
            name='experiments_exclude_all',
        ),
        migrations.RemoveField(
            model_name='experiment_sessions',
            name='experiments_include',
        ),
        migrations.RemoveField(
            model_name='experiment_sessions',
            name='experiments_include_all',
        ),
        migrations.RemoveField(
            model_name='experiment_sessions',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='experiment_sessions',
            name='institutions_exclude',
        ),
        migrations.RemoveField(
            model_name='experiment_sessions',
            name='institutions_exclude_all',
        ),
        migrations.RemoveField(
            model_name='experiment_sessions',
            name='institutions_include',
        ),
        migrations.RemoveField(
            model_name='experiment_sessions',
            name='institutions_include_all',
        ),
        migrations.RemoveField(
            model_name='experiment_sessions',
            name='registration_cutoff',
        ),
        migrations.RemoveField(
            model_name='experiment_sessions',
            name='subject_type',
        ),
        migrations.AddField(
            model_name='experiment_sessions',
            name='recruitmentParamsDefault',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.recruitmentParameters'),
        ),
    ]
