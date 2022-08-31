# Generated by Django 4.0.6 on 2022-08-09 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0192_umbrellaconsentform'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profileconsentform',
            options={'ordering': ['my_profile__user__last_name', 'my_profile__user__first_name'], 'verbose_name': 'Profile Consent Form', 'verbose_name_plural': 'Profile Consent Forms'},
        ),
        migrations.AddField(
            model_name='consentform',
            name='IRB_ID',
            field=models.CharField(default='', max_length=300),
        ),
    ]