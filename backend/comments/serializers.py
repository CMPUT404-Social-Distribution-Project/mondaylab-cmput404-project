from post.models import Post
from .models import Comment
from rest_framework import serializers
from author.serializers import LimitedAuthorSerializer

class CommentsSerializer(serializers.ModelSerializer):
    author = LimitedAuthorSerializer(required=False, many=False, allow_null=True)
    class Meta:
        model = Comment
        fields = '__all__'

        extra_kwargs = {
            'type': {'read_only': True},
            'id': {'read_only': True},
            'published': {'read_only': True},
        }

class CommentSrcSerializer(serializers.ModelSerializer):
    comments = CommentsSerializer(required=False, many=True, allow_null=True)
    class Meta:
        model = Comment
        fields = '__all__'
