# Generated by Django 4.1.2 on 2022-11-06 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostName', models.URLField()),
                ('authUsername', models.CharField(max_length=200)),
                ('authPassword', models.CharField(max_length=200)),
            ],
        ),
    ]