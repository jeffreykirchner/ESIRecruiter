# Generated by Django 4.0.6 on 2022-08-23 22:47

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0196_consentform_consent_form_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consentform',
            name='consent_form_text',
            field=tinymce.models.HTMLField(default='', verbose_name='Consent Form Text'),
        ),
    ]