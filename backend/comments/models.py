from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils.timezone import now
from django.utils import dateparse
from django.db.models import (Model, CharField, URLField, TextChoices, TextField,
ForeignKey, CASCADE, IntegerField, DateTimeField,BooleanField
)
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
    type =  CharField(blank=False, null=False, default="comment", max_length=200)
    id = URLField(primary_key=True, blank=True, null=False)
    # when all row in author is deleted, this comment will be too
    author = models.ForeignKey(Author,blank=False, null=False, on_delete=CASCADE)
    contentType = CharField(default=ContentType.markdown, blank=False, null=False, choices=ContentType.choices, max_length=200)
    published = CharField(blank=True, max_length=200)





