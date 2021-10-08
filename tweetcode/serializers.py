from django.conf import settings
from rest_framework import serializers

from .models import Posts

MAX_POST_LENGTH = settings.MAX_POST_LENGTH

TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS



class PostActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)


    def validate_action(self,value):
        value = value.lower().strip()
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for posts")

        return value 



class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id','content',]

    def validate_content(self,value):
        if len(value)> MAX_POST_LENGTH:
            raise serializers.ValidationError("This Post is too long")
        return value


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id','content']
