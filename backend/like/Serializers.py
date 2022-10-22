from rest_framework import serializers
from .models import Like
class LikeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="Like", read_only=True)

    class Meta:
        model = Like
        fields = ("summary","type","author","object")

