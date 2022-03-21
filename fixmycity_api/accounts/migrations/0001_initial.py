# Generated by Django 4.0.3 on 2022-03-19 06:01

import accounts.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.PositiveSmallIntegerField(choices=[(1, 'super_admin'), (3, 'custom_user'), (2, 'sector_admin')], primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district_name', models.CharField(max_length=150, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(max_length=150, unique=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255, null=True)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=accounts.models.upload_to)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('staff', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('roles', models.ForeignKey(db_column='rolesId', on_delete=django.db.models.deletion.CASCADE, to='accounts.role')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SectorAdmin',
            fields=[
                ('sector_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('email', models.EmailField(max_length=100)),
                ('main_sector', models.BooleanField(default=False)),
                ('sector', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sector', to='accounts.sector')),
            ],
            options={
                'abstract': False,
            },
            bases=('accounts.user',),
        ),
    ]
