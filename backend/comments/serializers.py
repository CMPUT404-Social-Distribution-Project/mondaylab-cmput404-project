from post.models import Post
from .models import Comment
from rest_framework import serializers
from post.serializers import PostAuthorSerializer

class CommentsSerializer(serializers.ModelSerializer):
    author = PostAuthorSerializer(required=False, many=False, allow_null=True)
    class Meta:
        model = Comment
        fields = '__all__'

        extra_kwargs = {
            'type': {'read_only': True},
            'id': {'read_only': True},
            'published': {'read_only': True},
        }