# Generated by Django 4.0.4 on 2022-06-03 17:38

import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0174_alter_consentform_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileconsentform',
            name='singnature_points',
            field=models.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True),
        ),
    ]
