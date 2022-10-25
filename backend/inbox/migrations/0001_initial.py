# Generated by Django 4.1.2 on 2022-10-25 20:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0001_initial'),
        ('followers', '0001_initial'),
        ('author', '0001_initial'),
        ('like', '0001_initial'),
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('type', models.CharField(default='inbox', editable=False, max_length=10)),
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('comments', models.ManyToManyField(to='comments.comment')),
                ('follow_request', models.ManyToManyField(to='followers.friendrequest')),
                ('likes', models.ManyToManyField(to='like.like')),
                ('posts', models.ManyToManyField(related_name='inbox_posts', to='post.post')),
            ],
        ),
    ]
