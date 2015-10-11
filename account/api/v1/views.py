from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from account.api.v1.serializers import UserProfileSerializer
from account.models import Profile, CITY_CHOICES


@api_view(['GET'])
def city_list(request, version=None):
    result = [ {'code': city_tuple[0], 'label': city_tuple[1], } for city_tuple in CITY_CHOICES ]
    return Response(result)

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)