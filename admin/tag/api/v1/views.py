
from rest_framework_bulk.generics import BulkModelViewSet

from admin.tag.api.v1.filterset import TreeTagGenericFilterSet
from admin.tag.api.v1.serializers import TreeTagSerializer
from tag.models import TreeTag


class TreeTagViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TreeTag.objects.all()
    serializer_class = TreeTagSerializer
    filter_class = TreeTagGenericFilterSet
    