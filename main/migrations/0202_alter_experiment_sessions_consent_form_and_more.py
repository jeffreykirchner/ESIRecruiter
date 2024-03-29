# Generated by Django 4.0.6 on 2022-09-02 20:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0201_alter_consentform_irb_study_alter_irbstudy_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment_sessions',
            name='consent_form',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ES_c', to='main.consentform'),
        ),
        migrations.AlterField(
            model_name='experiment_sessions',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ES_d', to=settings.AUTH_USER_MODEL),
        ),
    ]
