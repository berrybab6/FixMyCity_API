# Generated by Django 4.0.3 on 2022-03-22 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_alter_report_userid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='sectorId',
            new_name='sector',
        ),
        migrations.RenameField(
            model_name='report',
            old_name='userId',
            new_name='user',
        ),
    ]
