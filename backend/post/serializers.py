from .models import Post
from rest_framework import serializers
from author.models import Author

# Need a different author serializer that doesn't include the 
# extra fields we have in the other serializer
class PostAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id','uuid','host','displayName','url',
        'github','profileImage', 'type']
        extra_kwargs = {
            'type': {'read_only': True},
            'id': {'read_only': True},
            'uuid': {'read_only': True},
        }

class PostSerializer(serializers.ModelSerializer):
    author = PostAuthorSerializer(many=False, allow_null=True, required=False)  # needed this to get post's author field to become nested json object
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
