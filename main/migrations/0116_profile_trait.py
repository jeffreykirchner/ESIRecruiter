# Generated by Django 3.1.2 on 2020-11-29 22:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0115_traits'),
    ]

    operations = [
        migrations.CreateModel(
            name='profile_trait',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('my_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.profile')),
                ('trait', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.traits')),
            ],
            options={
                'verbose_name': 'Profile Trait',
                'verbose_name_plural': 'Profile Traits',
            },
        ),
    ]
