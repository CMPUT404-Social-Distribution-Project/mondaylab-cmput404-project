# Generated by Django 4.1.2 on 2022-11-10 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='visibility',
            field=models.CharField(choices=[('PUBLIC', 'PUBLIC'), ('FRIENDS', 'FRIENDS'), ('PRIVATE', 'PRIVATE')], default='PUBLIC', max_length=200),
        ),
    ]