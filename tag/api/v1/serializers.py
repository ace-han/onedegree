from rest_framework import serializers
from taggit.models import Tag

from tag.models import TreeTag


class TreeTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeTag
        #fields = ('url', 'username', 'email', 'groups')
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ('slug', )