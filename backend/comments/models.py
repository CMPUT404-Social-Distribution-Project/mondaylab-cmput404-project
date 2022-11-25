from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils.timezone import now
from django.utils import dateparse
from django.db.models import (Model, CharField, URLField, TextChoices, TextField,
ForeignKey, CASCADE, IntegerField, DateTimeField,BooleanField, UUIDField, PositiveIntegerField,
ManyToManyField
)

from uuid import uuid4
# Create your models here.

from author.models import Author # import autuhor table 
class ContentType(TextChoices):
    markdown ="text/markdown", "text/markdown"
    plain = "text/plain", "text/plain"
    base64 = "application/base64", "application/base64"
    png = "image/png;base64", "image/png;base64"
    jpeg = "image/jpeg;base64", "image/jpeg;base64"
class Visibility(TextChoices):
    PUBLIC = 'PUBLIC', 'PUBLIC'
    FRIENDS = 'FRIENDS', 'FRIENDS'

class Comment(Model):
    type = CharField(blank=False, null=False, default="comment", max_length=200)
    id = URLField(blank=True, null=False)
    uuid = UUIDField(primary_key=True, default=uuid4, editable=False)
    # when all row in author is deleted, this comment will be too
    author = models.ForeignKey(Author,blank=False, null=True, on_delete=CASCADE)
    contentType = CharField(default='text/markdown', blank=False, null=False, max_length=200)
    published = CharField(blank=True, max_length=200)
    comment = CharField(blank=True, null=True,  max_length=200, default="empty comment")

class CommentSrc(Model):
    type = CharField(blank=False, null=False, default="comments", max_length=200)
    page = PositiveIntegerField(default=1)
    size = PositiveIntegerField(default=5)
    post = URLField(blank=True, null=False)
    id = URLField(primary_key=True, blank=True, null=False)
    comments = ManyToManyField(Comment, blank=True)





