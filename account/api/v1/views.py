from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from account.api.v1.filtersets import UserProfileFilterSet
from account.api.v1.serializers import UserProfileSerializer
from account.models import Profile, CITY_CHOICES
from authx.permissions import IsOwnerOrReadOnly
from rest_condition import Or


@api_view(['GET'])
def city_list(request, version=None):
    result = [ {'code': city_tuple[0], 'label': city_tuple[1], } for city_tuple in CITY_CHOICES ]
    return Response(result)

'''
from rest_framework.filters import SearchFilter, OrderingFilter
from url_filter.integrations.drf import DjangoFilterBackend
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_class = UserProfileFilterSet
    filter_backends = (
        DjangoFilterBackend, # this backend expose the structure of object definition
                            # good for internal projects not for external ones
        SearchFilter,
        OrderingFilter,
    )
'''

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,
                          Or(IsAdminUser, IsOwnerOrReadOnly), )
    filter_class = UserProfileFilterSet
    
    def get_permissions(self):
        # based on the answer on stackoverflow, this is the best solution
        # decorator perview on viewset is verified as not working 
        # refer to http://stackoverflow.com/questions/25283797/django-rest-framework-add-additional-permission-in-viewset-update-method#answer-25290284
        if self.action == 'list':
            return [IsAdminUser(), ]
        return super().get_permissions()