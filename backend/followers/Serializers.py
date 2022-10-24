from post.models import Post
from followers.models import FriendRequest
from rest_framework import serializers
from author.serializers import AuthorSerializer

class FriendRequestSerializer(serializers.ModelSerializer):
    actor = AuthorSerializer(many=False, required=True)
    object = AuthorSerializer(many=False, required=True)

    class Meta:
        model = FriendRequest
        fields = ("type", "summary", "actor", "object")

        extra_kwargs = {
            'type': {'read_only': True},
        }