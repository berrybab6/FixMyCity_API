# Generated by Django 4.0.3 on 2022-05-25 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0006_remove_report_nooflikes_report_nooflikes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='tag',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
