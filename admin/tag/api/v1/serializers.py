from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin

from tag.models import Tag, TreeTag


class TreeTagSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    slug = serializers.SlugField(required=False, allow_null=True)
    cumulative_count = serializers.IntegerField(required=False, allow_null=True)
    class Meta:
        model = TreeTag
        list_serializer_class = BulkListSerializer
        

class TreeTagPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def display_value(self, instance):
        return 'ID: %s, Name: %s' % (instance.id, instance.name)

class TreeTagMoveNodeSerializer(serializers.Serializer):
    target = TreeTagPrimaryKeyRelatedField( queryset=TreeTag.objects.all() )
    position = serializers.ChoiceField(choices=(
                                                ('first-child', 'Parent: target, position: first child',),
                                                ('last-child', 'Parent: target, position: last child',),
                                                ('left', 'Parent: target\'s parent, position: before target',),
                                                ('right', 'Parent: target\'s parent, position: after target',), 
                                                ))
    
class TagSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    slug = serializers.SlugField(required=False, allow_null=True)
    class Meta:
        model = Tag
        list_serializer_class = BulkListSerializer