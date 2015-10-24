from rest_condition import Or
from rest_framework import viewsets
from rest_framework.decorators import api_view, detail_route
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.api.v1.filtersets import UserProfileFilterSet
from account.api.v1.serializers import UserProfileSerializer
from account.models import Profile, CITY_CHOICES
from authx.permissions import IsAdminUser, SelfOnly


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
                          Or(IsAdminUser, SelfOnly), )
    filter_class = UserProfileFilterSet
    
    def get_permissions(self):
        # based on the answer on stackoverflow, this is the best solution
        # decorator perview on viewset is verified as not working 
        # refer to http://stackoverflow.com/questions/25283797/django-rest-framework-add-additional-permission-in-viewset-update-method#answer-25290284
        if self.action in ('list', 'destroy', ):
            return [IsAdminUser(), ]
        return super().get_permissions()
    
    @detail_route()
    def userwise(self, request, pk=None, version=None):
        '''
            retrieve profile via user id only
        '''
        # retrieving a profile via query_param user_id only(for security concern)
        # may need to move the logic to other app/db
        user_id = request.query_params.get('user_id')
        if not user_id:
            raise ValidationError('Query parameter `user_id` is required')
        instance = get_object_or_404(self.get_queryset(), user=user_id)
        self.check_object_permissions(self.request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
        