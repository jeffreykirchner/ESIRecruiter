# Generated by Django 4.0.6 on 2022-08-03 23:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0191_consentform_archived'),
    ]

    operations = [
        migrations.CreateModel(
            name='UmbrellaConsentForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(default='', max_length=100, unique=True, verbose_name='Displayed name to subjects')),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('consent_form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='umbrella_consent_forms', to='main.consentform')),
            ],
            options={
                'verbose_name': 'Umbrella Consent Form',
                'verbose_name_plural': 'Umbrella Consent Forms',
            },
        ),
    ]
