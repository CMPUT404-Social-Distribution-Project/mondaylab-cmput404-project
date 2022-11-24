from rest_framework import serializers
from .models import Like
#from post.serializers import PostAuthorSerializer  # reuse this to have nested author obj
from author.serializers import LimitedAuthorSerializer

class LikeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="Like", read_only=True)
    author = LimitedAuthorSerializer(required=False, many=False, allow_null=True)  
    class Meta:
        model = Like
        fields = ("summary","type","author","object")

class LikeAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("summary","type","object")