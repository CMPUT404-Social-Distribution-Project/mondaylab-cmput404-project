# Generated by Django 4.1.2 on 2022-10-22 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0004_alter_comment_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.CharField(blank=True, default='empty comment', max_length=200, null=True),
        ),
    ]
