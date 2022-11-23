from .models import Post
from rest_framework import serializers
from author.models import Author
from comments.serializers import CommentSrcSerializer
from author.serializers import LimitedAuthorSerializer


class PostSerializer(serializers.ModelSerializer):
    # author = LimitedAuthorSerializer(many=False, allow_null=True, required=False)  # needed this to get post's author field to become nested json object
    # commentSrc = CommentSrcSerializer(many=True, required=False)
    uuid = serializers.UUIDField(format='hex', required=False)
    class Meta:
        model = Post
        fields = '__all__'

        extra_kwargs = {
            'type': {'read_only': True},
            'id': {'read_only': True},
            'published': {'read_only': True},
            'author': {'read_only': True},
            'comments': {'read_only': True},
        }

    # issue with having two ForeignKey fields. This is the solution.
    # ref: https://stackoverflow.com/questions/26702695/django-rest-framework-object-is-not-iterable
    # answer by Mustaq Mohammad
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['author'] = LimitedAuthorSerializer(instance.author).data
        rep['commentSrc'] = CommentSrcSerializer(instance.commentSrc).data
        return rep
