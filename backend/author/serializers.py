from .models import Author
from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id','uuid','host','displayName','url',
        'github','profileImage','is_active','is_superuser', 'type']
        extra_kwargs = {
            'type': {'read_only': True},
            'id': {'read_only': True},
            'uuid': {'read_only': True},
            'is_superuser': {'read_only': True},
        }