# Generated by Django 4.1.2 on 2022-10-22 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0002_alter_author_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='uuid',
            field=models.UUIDField(blank=True, default='fdb8d76a-4b36-45ac-a31d-d054ffd25fde', editable=False, primary_key=True, serialize=False),
        ),
    ]
