
from rest_framework_bulk.generics import BulkModelViewSet

from admin.friend.api.v1.filtersets import PhoneContactRecordGenericFilterSet
from admin.friend.api.v1.serializers import PhoneContactRecordSerializer
from friend.models import PhoneContactRecord


class PhoneContactRecordViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = PhoneContactRecord.objects.all()
    serializer_class = PhoneContactRecordSerializer
    filter_class = PhoneContactRecordGenericFilterSet
    search_fields = ('to_phone_num', )
    
    
