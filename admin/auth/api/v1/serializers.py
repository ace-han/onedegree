from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin

from authx.models import User


class UserSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    password = serializers.CharField(
                    style={'input_type': 'password'},
                    write_only=True # password not showing for the time being
                )
    
    class Meta:
        model = User
        list_serializer_class = BulkListSerializer
        
    def create(self, validated_data):
        raw_password = validated_data.get('password', None)
        validated_data['password'] = make_password(raw_password)
        return super(UserSerializer, self).create(validated_data)
        
    def update(self, instance, validated_data):
        raw_password = validated_data.get('password', None)
        validated_data['password'] = make_password(raw_password)
        return super(UserSerializer, self).update(instance, validated_data)
        