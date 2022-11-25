from django.db.models import (Model, URLField, CharField, ForeignKey, UUIDField, CASCADE)
from author.models import Author
from uuid import uuid4



class FriendRequest(Model):
    type = CharField(max_length=6, default="Follow")
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    summary = CharField(max_length=200)
    actor = ForeignKey(Author, related_name='sent_friend_request', on_delete = CASCADE, blank=True, null=True)
    object = ForeignKey(Author, related_name='recieve_friend_request', on_delete = CASCADE, blank=True, null=True)

    def __str__(self):
        return self.summary