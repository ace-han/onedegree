from rest_framework.permissions import IsAuthenticated

from friend.models import are_friends


class IsFriend(IsAuthenticated):
    '''
        is current login user's profile friend to target obj(profile)
    '''
    def has_object_permission(self, request, view, obj):
        return are_friends(request.user.profile, obj)