
from rest_framework_bulk.generics import BulkModelViewSet

from account.models import School, Profile
from admin.account.api.v1.filtersets import SchoolGenericFilterSet, \
    ProfileGenericFilterSet
from admin.account.api.v1.serializers import SchoolSerializer, ProfileSerializer


class SchoolViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    filter_class = SchoolGenericFilterSet
    search_fields = ('name', )
    
class ProfileViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_class = ProfileGenericFilterSet
    search_fields = ('phone_num', )
    
