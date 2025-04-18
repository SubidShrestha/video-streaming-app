# Generated by Django 5.2 on 2025-04-13 17:17

import authentication.managers
import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('last_deactivated_at', models.DateTimeField(blank=True, null=True, verbose_name='last deactivated at')),
                ('last_reactivated_at', models.DateTimeField(blank=True, null=True, verbose_name='last reactivated at')),
                ('username', models.CharField(error_messages={'unique': 'The username is already taken.'}, help_text='Required. 26 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=26, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='profile image')),
                ('email', models.EmailField(error_messages={'unique': 'A user with this email address already exists.'}, max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'users',
                'indexes': [models.Index(fields=['username'], name='idx_username'), models.Index(fields=['email'], name='idx_email')],
            },
            managers=[
                ('objects', authentication.managers.AuthUserManager()),
            ],
        ),
    ]
