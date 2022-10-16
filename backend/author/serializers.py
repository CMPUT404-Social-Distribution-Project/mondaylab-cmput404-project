from .models import Author
from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        extra_kwargs = {
            'type': {'read_only': True},
            'id': {'read_only': True},
            'published': {'read_only': True}
        }