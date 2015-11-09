from rest_framework import serializers

from tag.models import Tag, TreeTag 


class TreeTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeTag
        #fields = ('url', 'username', 'email', 'groups')
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ('slug', )