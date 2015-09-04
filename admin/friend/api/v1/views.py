
from rest_framework_bulk.generics import BulkModelViewSet

from admin.friend.api.v1.filterset import ContactRecordGenericFilterSet
from admin.friend.api.v1.serializers import ContactRecordSerializer
from friend.models import ContactRecord


class ContactRecordViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ContactRecord.objects.all()
    serializer_class = ContactRecordSerializer
    filter_class = ContactRecordGenericFilterSet
    search_fields = ('to_phone_num', )
    
    
