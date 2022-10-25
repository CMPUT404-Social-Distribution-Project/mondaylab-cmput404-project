from django.utils.timezone import now
from django.utils import dateparse
from django.db.models import (Model, CharField, URLField, TextChoices, TextField,
ForeignKey, CASCADE, IntegerField, DateTimeField,BooleanField,UUIDField
)
from author.models import Author
from uuid import uuid4

# class ContentType(TextChoices):
#     markdown ="text/markdown", "text/markdown"
#     plain = "text/plain", "text/plain"
#     base64 = "application/base64", "application/base64"
#     png = "image/png;base64", "image/png;base64"
#     jpeg = "image/jpeg;base64", "image/jpeg;base64"

# class Visibility(TextChoices):
#     PUBLIC = 'PUBLIC', 'PUBLIC'
#     FRIENDS = 'FRIENDS', 'FRIENDS'


class Post(Model):
    class ContentType(TextChoices):
        markdown ="text/markdown", "text/markdown"
        plain = "text/plain", "text/plain"
        base64 = "application/base64", "application/base64"
        png = "image/png;base64", "image/png;base64"
        jpeg = "image/jpeg;base64", "image/jpeg;base64"
    class Visibility(TextChoices):
        PUBLIC = 'PUBLIC', 'PUBLIC'
        FRIENDS = 'FRIENDS', 'FRIENDS'

    type =CharField(blank=False, null=False, default="post", max_length=200)
    title = CharField(max_length=50, blank=True)
    id = URLField(blank=False, null=False)
    uuid = UUIDField(primary_key=True, default=uuid4, editable=False)
    source = URLField(blank=True)
    origin = URLField(blank=True)
    description = CharField( blank=True, null=True, max_length=300)
    contentType = CharField(default=ContentType.plain, blank=False, null=False, choices=ContentType.choices, max_length=200)
    content = TextField(blank=True, null=True)
    author = ForeignKey(Author, blank=False, null=True, on_delete=CASCADE)
    categories = TextField(null=True)
    #see this to send categories
    #https://stackoverflow.com/a/7151813 
    count = IntegerField(default=0)
    comments = URLField(blank=True)
    #commentsSrc = ForeignKey(CommentsSrc, blank=True, null=True)
    published = DateTimeField(auto_now_add=True, editable=False)
    visibility = CharField(default=Visibility.PUBLIC, choices=Visibility.choices, max_length=200)
    unlisted = BooleanField(default=False, blank=False, null=False)

