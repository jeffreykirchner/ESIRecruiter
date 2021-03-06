# Generated by Django 2.2.10 on 2020-06-04 23:47

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid

# def initGenders(apps, schema_editor):

#     MyModel = apps.get_model('main', 'genders')

#     gender=MyModel()
#     gender.name="Female"
#     gender.save()

#     gender=MyModel()
#     gender.name="Male"
#     gender.save()

#     gender=MyModel()
#     gender.name="Transgender"
#     gender.save()

#     gender=MyModel()
#     gender.name="Other"
#     gender.save()

#     gender=MyModel()
#     gender.name="Prefer not to say"
#     gender.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='accounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=300)),
                ('number', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='accountTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='departments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('charge_account', models.CharField(max_length=100)),
                ('petty_cash', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='experience_levels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='experiments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('experiment_manager', models.CharField(max_length=300)),
                ('registration_cutoff_default', models.IntegerField()),
                ('actual_participants_default', models.IntegerField()),
                ('length_default', models.IntegerField()),
                ('notes', models.TextField(null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('account_default', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.accounts')),
                ('experience_level_default', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.experience_levels')),
                ('experiments_exclude_default', models.ManyToManyField(blank=True, related_name='_experiments_experiments_exclude_default_+', to='main.experiments')),
                ('experiments_include_default', models.ManyToManyField(blank=True, related_name='_experiments_experiments_include_default_+', to='main.experiments')),
            ],
        ),
        migrations.CreateModel(
            name='genders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        
        #migrations.RunPython(initGenders),

        migrations.CreateModel(
            name='institutions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='locations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('address', models.TextField(null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='majors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='schools',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='subject_types',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapmanID', models.CharField(default='00000000', max_length=100)),
                ('emailConfirmed', models.CharField(default='no', max_length=100)),
                ('blackballed', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('gender', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.genders')),
                ('major', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.majors')),
                ('school', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.schools')),
                ('type', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='main.accountTypes')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='experiments_institutions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.experiments')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.institutions')),
            ],
        ),
        migrations.AddField(
            model_name='experiments',
            name='gender_default',
            field=models.ManyToManyField(to='main.genders'),
        ),
        migrations.AddField(
            model_name='experiments',
            name='institution',
            field=models.ManyToManyField(through='main.experiments_institutions', to='main.institutions'),
        ),
        migrations.AddField(
            model_name='experiments',
            name='institutions_exclude_default',
            field=models.ManyToManyField(blank=True, related_name='experiments_institutions_exclude_default', to='main.institutions'),
        ),
        migrations.AddField(
            model_name='experiments',
            name='institutions_include_default',
            field=models.ManyToManyField(blank=True, related_name='experiments_institutions_include_default', to='main.institutions'),
        ),
        migrations.AddField(
            model_name='experiments',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.schools'),
        ),
        migrations.AddField(
            model_name='experiments',
            name='subject_type_default',
            field=models.ManyToManyField(to='main.subject_types'),
        ),
        migrations.CreateModel(
            name='experiment_sessions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('experience_level', models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to='main.experience_levels')),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.experiments')),
                ('experiments_exclude', models.ManyToManyField(blank=True, related_name='experiment_sessions_experiments_exclude', to='main.experiments')),
                ('experiments_include', models.ManyToManyField(blank=True, related_name='experiment_sessions_experiments_include', to='main.experiments')),
                ('gender', models.ManyToManyField(to='main.genders')),
                ('institutions_exclude', models.ManyToManyField(blank=True, related_name='experiment_sessions_institutions_exclude', to='main.institutions')),
                ('institutions_include', models.ManyToManyField(blank=True, related_name='experiment_sessions_institutions_include', to='main.institutions')),
                ('subject_type', models.ManyToManyField(to='main.subject_types')),
            ],
        ),
        migrations.CreateModel(
            name='experiment_session_days',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_cutoff', models.IntegerField(default=1)),
                ('actual_participants', models.IntegerField(default=1)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('length', models.IntegerField(default=60)),
                ('auto_reminder', models.SmallIntegerField(default=1)),
                ('canceled', models.SmallIntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.accounts')),
                ('experiment_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.experiment_sessions')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.locations')),
            ],
        ),
        migrations.CreateModel(
            name='experiment_session_day_users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attended', models.BooleanField(default=False)),
                ('bumped', models.BooleanField(default=False)),
                ('confirmed', models.BooleanField(default=False)),
                ('confirmationHash', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('show_up_fee', models.DecimalField(decimal_places=6, max_digits=10)),
                ('earnings', models.DecimalField(decimal_places=6, max_digits=10)),
                ('multi_day_legacy', models.BooleanField(default=False, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('experiment_session_day', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.experiment_session_days')),
                ('experiment_session_legacy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.experiment_sessions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='accounts',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.departments'),
        ),
    ]
