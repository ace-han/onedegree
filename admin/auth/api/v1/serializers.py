from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin

from authx.models import User


class UserSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    password = serializers.CharField(
                    style={'input_type': 'password'}
                )
    
    class Meta:
        model = User
        list_serializer_class = BulkListSerializer
        
