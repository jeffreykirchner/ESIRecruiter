# Generated by Django 3.1.2 on 2020-10-02 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0107_auto_20201002_1709'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faq',
            options={'ordering': ['order'], 'verbose_name': 'FAQ', 'verbose_name_plural': 'FAQs'},
        ),
        migrations.AlterField(
            model_name='faq',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Show Question'),
        ),
        migrations.AlterField(
            model_name='faq',
            name='answer',
            field=models.CharField(max_length=10000, verbose_name='Answer'),
        ),
        migrations.AlterField(
            model_name='faq',
            name='order',
            field=models.IntegerField(default=1, verbose_name='Display Order'),
        ),
        migrations.AlterField(
            model_name='faq',
            name='question',
            field=models.CharField(max_length=300, verbose_name='Question'),
        ),
    ]