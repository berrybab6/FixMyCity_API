# Generated by Django 4.0.3 on 2022-04-04 10:47

import cloudinary.models
import django.contrib.gis.db.models.fields
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
            name='PhoneOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+9xxxxxxxxxx'. Up to 10 digits allowed.", regex='^\\+?1?\\d{9,14}$')])),
                ('otp', models.CharField(blank=True, max_length=9, null=True)),
                ('count', models.IntegerField(default=0, help_text='Number of otp sent')),
                ('logged', models.BooleanField(default=False, help_text='If otp verification got successful')),
            ],
        ),
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
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('address', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('staff', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('main_sector', models.BooleanField(default=False)),
                ('phone_number', models.CharField(max_length=13, null=True, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('first_name', models.CharField(max_length=255, null=True)),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('ProfileImage', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('roles', models.ForeignKey(db_column='rolesId', null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.role')),
                ('sector', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sector', to='accounts.sector')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
