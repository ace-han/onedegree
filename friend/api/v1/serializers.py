from django.contrib.auth import get_user_model
from rest_framework import serializers

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
        if len(tag_objs)>6:
            tag_objs = tag_objs[:6]
        result = []
        for tag in tag_objs:
            result.append(tag.name)
        return result