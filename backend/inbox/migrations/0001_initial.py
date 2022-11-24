# Generated by Django 4.1.2 on 2022-11-23 22:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('like', '0001_initial'),
        ('post', '0001_initial'),
        ('comments', '0001_initial'),
        ('author', '0001_initial'),
        ('followers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('type', models.CharField(default='inbox', editable=False, max_length=10)),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='inbox_author', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('comments', models.ManyToManyField(to='comments.comment')),
                ('follow_requests', models.ManyToManyField(to='followers.friendrequest')),
                ('likes', models.ManyToManyField(to='like.like')),
                ('posts', models.ManyToManyField(related_name='inbox_posts', to='post.post')),
            ],
        ),
    ]
