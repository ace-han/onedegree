from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework_jwt.views import (obtain_jwt_token as _obtain_jwt_token,
                                      refresh_jwt_token as _refresh_jwt_token,
                                      verify_jwt_token as _verify_jwt_token,)

from tag.api.v1.serializers import TreeTagSerializer
from tag.models import TreeTag


# just a simple wrapper with extra version parameter
@api_view(['POST'])
def obtain_jwt_token(*args, **kwargs):
    kwargs.pop('version', None)
    return _obtain_jwt_token(*args, **kwargs)

@api_view(['POST'])
def refresh_jwt_token(*args, **kwargs):
    kwargs.pop('version', None)
    return _refresh_jwt_token(*args, **kwargs)

@api_view(['GET', 'POST'])
def verify_jwt_token(*args, **kwargs):
    kwargs.pop('version', None)
    return _verify_jwt_token(*args, **kwargs)

class TreeTagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TreeTag.objects.all()
    serializer_class = TreeTagSerializer