# Generated by Django 4.0.6 on 2022-09-01 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0197_alter_consentform_consent_form_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consentform',
            name='pdf_file',
            field=models.FileField(upload_to=''),
        ),
    ]
