from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin

from friend.models import PhoneContactRecord


class PhoneContactRecordSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    
    class Meta:
        model = PhoneContactRecord
        list_serializer_class = BulkListSerializer