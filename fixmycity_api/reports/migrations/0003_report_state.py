# Generated by Django 4.0.4 on 2022-05-02 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_remove_report_state_report_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='state',
            field=models.BooleanField(default=False),
        ),
    ]