from rest_framework import viewsets

from tag.api.v1.serializers import TreeTagSerializer
from tag.models import TreeTag


class SchoolViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TreeTag.objects.all()
    serializer_class = TreeTagSerializer
    
class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TreeTag.objects.all()
    serializer_class = TreeTagSerializer