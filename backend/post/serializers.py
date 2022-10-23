from .models import Post
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):

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