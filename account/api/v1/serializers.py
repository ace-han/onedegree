from rest_framework import serializers

from account.models import Profile, School
from authx.models import User
from onedegree.api.v1.serializers import DynamicFieldsModelSerializer
from tag.models import Tag, TreeTag


class UserSerializer(serializers.ModelSerializer):
    # may need to refactor to another db
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'selfie_path', 'email')
        
class SchoolSerializer(serializers.ModelSerializer):
    #id = serializers.AutoF
    class Meta:
        model = School
        fields = ('id', 'name')
        # this read_only is for nested Serializer getting id as a writable field
        # see/debug to below src code for more detail
        #  rest_framework.serializers.py#to_internal_value
        #  rest_framework.serializers.py#_writable_fields(self):
        extra_kwargs = {'id': {'read_only': False,}, } 

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')
        extra_kwargs = {'id': {'read_only': False,}, } 

class TreeTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeTag
        fields = ('id', 'name')

class UserProfileSerializer(DynamicFieldsModelSerializer):
    user = UserSerializer()
    high_school = SchoolSerializer()
    college = SchoolSerializer()
    occupations = TreeTagSerializer(many=True)
    tags = TagSerializer(many=True)
    class Meta:
        model = Profile
        
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr in ('high_school', 'college'):
                # a little hack here for the value(school) is {'id':0,'name':'x',}
                value = School.objects.get(id=value.get('id'))
            elif attr == 'tags':
                tags = []
                for tag_data in value:
                    if 'id' in tag_data:
                        tag = Tag(**tag_data)
                    else:
                        tag = tag_data.get('name')
                    tags.append(tag)
                instance.tags.set(*tags)
                continue    # don't set the tags to the attrs   
            setattr(instance, attr, value)
            
        instance.save()

        return instance