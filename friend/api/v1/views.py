from django.http.response import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from account.models import Profile
from friend.models import are_friends, PhoneContactRecord
from tag.api.v1.serializers import TagSerializer
from tag.models import TaggedItem


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def has_friendship(request, version=None):
    profile = get_object_or_404(Profile.objects.filter(id=request.query_params.get('profile_id')))
    self_profile = get_object_or_404(Profile.objects.filter(user=request.user))
    result = {'is_friend': are_friends(self_profile, profile)}
    return Response(result)

class FriendTagsApiView(ListAPIView):
    #permission_classes = (AllowAny, )
    # queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # I will pass the filterset on this scenario and follow the easy implementation as the drf suggests
    # refer to http://www.django-rest-framework.org/api-guide/filtering/
    def get_queryset(self):
        # we might migrate it back to user module?
        pcr_qs = PhoneContactRecord.objects.filter(
                    from_profile__user_id=self.kwargs['user_id']
                ).values_list('to_profile_id', flat=True)
        if not pcr_qs.exists():
            raise Http404
        to_profile_qs = Profile.objects.filter(id__in=pcr_qs)
        extra_filters = {'%s__object_id__in'%(TaggedItem.tag_relname(), ): to_profile_qs}
        tag_qs = TaggedItem.tags_for(Profile, **extra_filters)
        return tag_qs
    
friend_tags = FriendTagsApiView.as_view()