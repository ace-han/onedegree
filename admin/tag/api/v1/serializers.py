from rest_framework import serializers
from tag.models import TreeTag


class TreeTagSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)
    class Meta:
        model = TreeTag
        #fields = ('url', 'username', 'email', 'groups')