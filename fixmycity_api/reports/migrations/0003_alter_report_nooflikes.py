# Generated by Django 4.0.3 on 2022-03-20 07:59

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_alter_report_nooflikes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='noOfLikes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=0), blank=True, size=None),
        ),
    ]
