from post.models import Post
from followers.models import FriendRequest
from rest_framework import serializers
from author.serializers import AuthorSerializer

class FriendRequestSerializer(serializers.ModelSerializer):
    # actor = AuthorSerializer(many=False, required=True)
    # object = AuthorSerializer(many=False, required=True)

    class Meta:
        model = FriendRequest
        fields = ("type", "summary", "actor", "object")

        extra_kwargs = {
            'type': {'read_only': True},
        }

    # issue with having two ForeignKey fields. This is the solution.
    # ref: https://stackoverflow.com/questions/26702695/django-rest-framework-object-is-not-iterable
    # answer by Mustaq Mohammad
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['actor'] = AuthorSerializer(instance.actor).data
        rep['object'] = AuthorSerializer(instance.object).data
        return rep