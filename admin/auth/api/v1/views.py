
from rest_framework_bulk.generics import BulkModelViewSet

from admin.auth.api.v1.filterset import UserGenericFilterSet
from admin.auth.api.v1.serializers import UserSerializer
from authx.models import User


class UserViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = UserGenericFilterSet
    search_fields = ('username', 'nickname', 'email')
    
