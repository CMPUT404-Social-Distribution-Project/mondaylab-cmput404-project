from rest_framework import serializers
from .models import Like
#from post.serializers import PostAuthorSerializer  # reuse this to have nested author obj
from author.serializers import LimitedAuthorSerializer

class LikePostSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="Like", read_only=True)
    author = LimitedAuthorSerializer(required=False, many=False, allow_null=True)  
    class Meta:
        model = Like
        fields = ("summary","type","author","object")

class LikeAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("summary","type","object")

class LikeCommentSerializer(serializers.ModelSerializer):
    # fields declare here will ovveride the default field in meta()
    type = serializers.CharField(default="Like", read_only=True)  
    # for nesting author obj within like object
    author = LimitedAuthorSerializer(required=False, many=False, allow_null=True)  
    class Meta:
        model = Like
        fields = ("summary","type","author","object")