from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin

from friend.models import ContactRecord


class ContactRecordSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    
    class Meta:
        model = ContactRecord
        list_serializer_class = BulkListSerializer