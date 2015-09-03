from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin

from account.models import School, Profile


class SchoolSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    
    class Meta:
        model = School
        list_serializer_class = BulkListSerializer
        
class ProfileSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        list_serializer_class = BulkListSerializer
        
