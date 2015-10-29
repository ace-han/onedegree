from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from rest_framework import serializers

from account.models import Profile

class UserProfileCreationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Profile
        fields = ('phone_num', 'city')

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileCreationSerializer()
    class Meta:
        model = get_user_model()
    
    @atomic
    def create(self, validated_data):
        ModelClass = self.Meta.model
        profile_data = validated_data.pop('profile')
        # here may going to be an api call to so called auth module
        user = ModelClass.objects.create_user(**validated_data)
        # profile may be in the system already
        profile, newly_created = Profile.objects.get_or_create(phone_num=profile_data.pop('phone_num'),
                            defaults=profile_data)
        profile.user = user
        profile.save()
        return user