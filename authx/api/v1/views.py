
from django.contrib.auth import get_user_model
from rest_condition import Or
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import (obtain_jwt_token as drf_obtain_jwt_token,
                                      refresh_jwt_token as drf_refresh_jwt_token,
                                      verify_jwt_token as drf_verify_jwt_token)

from authx.api.v1.serializers import UserSerializer
from authx.permissions import IsAdminUser, SelfOnly


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
# just a simple wrapper with extra version parameter

@api_view(['POST'])
def obtain_jwt_token(*args, **kwargs):
    kwargs.pop('version', None)
    return drf_obtain_jwt_token(*args, **kwargs)

@api_view(['POST'])
def refresh_jwt_token(*args, **kwargs):
    kwargs.pop('version', None)
    # need to store the old to an outdated_token table as an invalidated means
    # TODO
    return drf_refresh_jwt_token(*args, **kwargs)

@api_view(['POST'])
def verify_jwt_token(*args, **kwargs):
    kwargs.pop('version', None)
    # this verify only concerns username and integrity of the token
    return drf_verify_jwt_token(*args, **kwargs)

def jwt_response_special_handling(response, user=None):
    # special handling for login(obtain_xxx) and register on successful jwt response
    # just add an extra info for is_necessary_user_info_filled telling the client to nav to profile page
    data = response.data
    if user is None:
        token = response.data.get('token')
        user = __resolve_user(token)
    data['is_necessary_user_info_filled'] = __is_necessary_user_info_filled(user)
    return response

def __is_necessary_user_info_filled(user):
    if user is None:
        return False
    profile = user.profile
    if profile is None:
        return False
    return not any((
        #user.selfie_path == '',
        user.nickname == '',
        profile.phone_num == '',
        # profile.gender == None,
        profile.city == '',
        profile.high_school is None,
        profile.college is None,
        not profile.tags.exists(),
    ))

def __resolve_user(token):
    # a little bit overheaded but just login interface for the time being
    serializer = VerifyJSONWebTokenSerializer(data={'token': token,})
    serializer.is_valid(raise_exception=True)
    return serializer.object.get('user')

@api_view(['POST', ])
def register(request, version=None):
    # need to do some transform on this request.data in order to use UserCreationSerializer
    composed_profile = {
        'phone_num': request.data.get('phone_num'),
        'city': request.data.get('city'),
    }
    request.data['profile'] = composed_profile
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        response_data = jwt_response_payload_handler(token, user, request)
        return jwt_response_special_handling(
                    Response(response_data, status.HTTP_201_CREATED), user=user
                )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', ])
def login(*args, **kwargs):
    kwargs.pop('version', None)
    response = drf_obtain_jwt_token(*args, **kwargs)
    if status.is_success(response.status_code):
        # according to rest_framework_jwt.utils.jwt_response_payload_handler
        # response.data = {'token': xxxx, ...}
        response = jwt_response_special_handling(response)
    return response

class UserRetrieveUpdateViewSet(RetrieveModelMixin,
                                UpdateModelMixin, 
                                GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,
                          Or(IsAdminUser, SelfOnly), )
    
    '''
    # as we are no ModelViewSet, this get_permissions method is not necessary
    def get_permissions(self):
        # based on the answer on stackoverflow, this is the best solution
        # decorator perview on viewset is verified as not working 
        # refer to http://stackoverflow.com/questions/25283797/django-rest-framework-add-additional-permission-in-viewset-update-method#answer-25290284
        if self.action in ('list', 'destroy', ):
            return [IsAdminUser(), ]
        return super().get_permissions()
    '''