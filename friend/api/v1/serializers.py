from collections import OrderedDict

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from account.models import Profile, CITY_CHOICES
from onedegree.api.v1.serializers import DynamicFieldsModelSerializer


class UserSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'display_name', 'selfie_path')
    
    def get_display_name(self, obj):
        return obj.nickname or obj.username

class StringifiedSchoolField(serializers.RelatedField):
    def to_representation(self, value):
        return value.name
    
class FriendProfileSerializer(DynamicFieldsModelSerializer):
    user = UserSerializer()
    city = serializers.SerializerMethodField()
    high_school = StringifiedSchoolField(read_only=True)
    college = StringifiedSchoolField(read_only=True)
    occupations = serializers.StringRelatedField(read_only=True, many=True)
    tags = serializers.SerializerMethodField()
    class Meta:
        model = Profile

    def get_city(self, obj):
        if obj.city is None:
            return None
        for value, label in CITY_CHOICES:
            if value == obj.city:
                return label
        return None
    
    def get_tags(self, obj):
        tag_objs = obj.tags.all()
        query_string = ''
        if 'request' in self.context:
            query_string = self.context['request'].query_params.get('q')
        result = OrderedDict()
        if query_string:
            # ensure target tags for display
            for tag in tag_objs:
                if query_string in tag.name:
                    result[tag.name] = None
        
        for tag in tag_objs:
            if len(result) >= 6:
                break
            result[tag.name] = None

        return list(result.keys())

class SearchProfileSerializer(FriendProfileSerializer):
    is_contact_point = SerializerMethodField()
    
    def get_is_contact_point(self):
        return False