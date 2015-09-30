from rest_framework import viewsets

from account.api.v1.serializers import UserProfileSerializer
from account.models import Profile


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer