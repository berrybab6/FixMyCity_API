# Generated by Django 4.0.3 on 2022-03-25 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_customuser_phone_number'),
        ('reports', '0008_alter_report_nooflikes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='noOfLikes',
            field=models.ManyToManyField(related_name='report_posts', to='accounts.customuser'),
        ),
    ]
