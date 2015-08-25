from rest_framework import viewsets

from admin.tag.api.v1.serializers import TreeTagSerializer
from tag.models import TreeTag


class TreeTagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TreeTag.objects.all()
    serializer_class = TreeTagSerializer