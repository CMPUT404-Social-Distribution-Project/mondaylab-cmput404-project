
from enum import unique
from django.db.models import (Model, URLField, CharField, ForeignKey, OneToOneField, ManyToManyField, CASCADE)
from author.models import Author
from comments.models import Comment
from post.models import Post
from like.models import Like
from followers.models import FriendRequest

class Inbox(Model):
    """
    items will save all types of posts
    if the type is “post” then add that post to AUTHOR_ID’s inbox
    if the type is “follow” then add that follow is added to AUTHOR_ID’s inbox to approve later
    if the type is “like” then add that like to AUTHOR_ID’s inbox
    if the type is “comment” then add that comment to AUTHOR_ID’s inbox
    """
    type = CharField(max_length=10, default="inbox", editable=False)
    author = OneToOneField(Author, primary_key=True, on_delete=CASCADE, null=False, related_name="inbox_author")
    posts = ManyToManyField(Post, related_name='inbox_posts')
    comments = ManyToManyField(Comment)
    likes = ManyToManyField(Like)
    follow_requests = ManyToManyField(FriendRequest)
    
