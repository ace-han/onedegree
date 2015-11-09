from rest_framework import viewsets

from tag.api.v1.serializers import TreeTagSerializer, TagSerializer
from tag.models import Tag, TreeTag


class ReadOnlyTreeTagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TreeTag.objects.all()
    serializer_class = TreeTagSerializer
    
    
class ReadOnlyTagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    search_fields = ('name', 'slug', )