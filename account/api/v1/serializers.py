from rest_framework import serializers
from taggit.models import Tag

from account.models import Profile, School
from authx.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'selfie_path', 'email')
        
class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('id', 'name')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    high_school = SchoolSerializer()
    college = SchoolSerializer()
    tags = TagSerializer(many=True)
    class Meta:
        model = Profile