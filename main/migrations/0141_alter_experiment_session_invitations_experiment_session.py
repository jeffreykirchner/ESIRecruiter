# Generated by Django 3.2 on 2021-09-23 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0140_auto_20210422_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment_session_invitations',
            name='experiment_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiment_session_invitations', to='main.experiment_sessions'),
        ),
    ]
