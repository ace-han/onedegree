from rest_framework import serializers

from tag.models import TreeTag
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin

class TreeTagSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)
    class Meta:
        model = TreeTag
        list_serializer_class = BulkListSerializer