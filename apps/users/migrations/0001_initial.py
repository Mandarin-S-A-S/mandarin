# Generated by Django 3.0.5 on 2020-04-07 17:50

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentTypeApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'app',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(error_messages={'unique': 'The email is already registered'}, max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('phone_number', models.CharField(blank=True, max_length=25, null=True)),
                ('extra_fields', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_online', models.DateTimeField(blank=True, null=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('recovery_code', models.CharField(blank=True, default='', max_length=16, null=True)),
                ('recovery_attempts', models.IntegerField(blank=True, default=0, null=True)),
                ('activate_code', models.CharField(blank=True, default='', max_length=16, null=True)),
                ('is_online', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_verificated', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ['first_name'],
            },
        ),
    ]
