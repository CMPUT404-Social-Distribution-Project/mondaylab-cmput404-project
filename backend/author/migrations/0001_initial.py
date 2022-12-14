# Generated by Django 4.1.2 on 2022-11-21 20:59

from django.conf import settings
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('type', models.CharField(default='author', max_length=200)),
                ('uuid', models.UUIDField(blank=True, default=uuid.uuid4, primary_key=True, serialize=False)),
                ('id', models.URLField(blank=True, null=True)),
                ('host', models.URLField(blank=True, null=True)),
                ('displayName', models.CharField(max_length=200, unique=True)),
                ('url', models.URLField(blank=True)),
                ('github', models.URLField(blank=True)),
                ('profileImage', models.URLField(blank=True, default='')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('followers', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
