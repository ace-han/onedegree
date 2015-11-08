from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.models import Profile
from friend.models import are_friends


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def has_friendship(request, version=None):
    profile = get_object_or_404(Profile.objects.filter(id=request.query_params.get('profile_id')))
    self_profile = get_object_or_404(Profile.objects.filter(user=request.user))
    result = {'is_friend': are_friends(self_profile, profile)}
    return Response(result)
