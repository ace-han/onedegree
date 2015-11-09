from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin
from tag.models import Tag, TreeTag

from account.models import School, Profile
from admin.account.api.v1.fields import TaggedItemRelatedField


class SchoolSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    
    class Meta:
        model = School
        list_serializer_class = BulkListSerializer
        
class ProfileSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    
#     tags = serializers.PrimaryKeyRelatedField(many=True, read_only=False)
    occupations = TaggedItemRelatedField(many=True, read_only=False, queryset=TreeTag.objects.all())
    tags = TaggedItemRelatedField(many=True, read_only=False, queryset=Tag.objects.all())
    class Meta:
        model = Profile
        list_serializer_class = BulkListSerializer
#         fields = ('id', 'user', 'phone_num', 'gender', 'city', 
#                     'high_school', 'college', 'tags', 'description')
    
    def create(self, validated_data):
        occupations = validated_data.pop('occupations', None)
        tags = validated_data.pop('tags', None)
        # only taking care of tags since other many2many relations will have extra through table to setup
        instance = super(ProfileSerializer, self).create(validated_data)
        if occupations:
            instance.occupations.add(*occupations)
        if tags:
            # this add will create those tag records not yet in the system
            # refer to taggit.managers.py#tags_to_create 
            instance.tags.add(*tags)
            # since tags.add already done commit stuff
            # instance.save()
        return instance
    
    def update(self, instance, validated_data):
        occupations = validated_data.pop('occupations', None)
        tags = validated_data.pop('tags', None)
        # only taking care of tags since other many2many relations will have extra through table to setup
        instance = super(ProfileSerializer, self).update(instance, validated_data)
        if occupations != None:
            instance.occupations.set(*occupations)
        if tags != None:
            # since tags may set to empty []
            # since tags.add already done the set intersection
            instance.tags.set(*tags)
            # since add just cater for appending situation not the removing situation
            # instance.tags.add(*tags)
            # since tags.add already done commit stuff
            # instance.save()
        return instance
            
            
