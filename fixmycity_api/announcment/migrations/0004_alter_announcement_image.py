# Generated by Django 4.0.3 on 2022-03-21 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcment', '0003_announcement_sectoradmin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='image',
            field=models.URLField(null=True),
        ),
    ]
