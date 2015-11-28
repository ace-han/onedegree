from functools import reduce
import operator

from django.db.models.query_utils import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from account.models import Profile, SCHOOL_TYPES
from friend.api.v1.serializers import FriendProfileSerializer
from friend.models import are_friends, PhoneContactRecord
from tag.api.v1.serializers import TagSerializer
from tag.models import TaggedItem, Tag


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def has_friendship(request, version=None):
    profile = get_object_or_404(Profile.objects.filter(user=request.query_params.get('user_id')))
    self_profile = get_object_or_404(Profile.objects.filter(user=request.user))
    result = {'is_friend': are_friends(self_profile, profile)}
    return Response(result)

class FriendTagsListView(ListAPIView):
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
            return Tag.objects.none()
        to_profile_qs = Profile.objects.filter(id__in=pcr_qs)
        extra_filters = {'%s__object_id__in'%(TaggedItem.tag_relname(), ): to_profile_qs}
        tag_qs = TaggedItem.tags_for(Profile, **extra_filters)
        return tag_qs
    
friend_tags = FriendTagsListView.as_view()

class AlumniProfileListView(ListAPIView):
    serializer_class = FriendProfileSerializer
    permission_classes = (IsAuthenticated,)
    search_fields = ('occupations__name', 'tags__name', )
    
    def get_queryset(self):
        user = self.request.user
        profile_qs = Profile.objects.filter(user__isnull=False).exclude(user=user)
        
        # refer to http://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
        # according to doc, filtering against query_params just like this
        valid_school_type_dict = dict(SCHOOL_TYPES)
        user_profile = get_object_or_404(Profile, user=user)
        school_type = self.request.query_params.get('school_type')
        if school_type and school_type not in valid_school_type_dict:
            raise ValidationError('Invalid school_type, valid options are %s' % (''.join(valid_school_type_dict.keys())))
        if school_type:
            school = getattr(user_profile, school_type)
            if school:
                # should be a plain new q_obj
                profile_qs = profile_qs.filter( Q(**{'%s'%school_type: school}) )
            else:
                profile_qs = profile_qs.none()
        else:
            q_objs = []
            for school_type in valid_school_type_dict.keys():
                school = getattr(user_profile, school_type)
                if school is None:
                    continue
                q_objs.append( Q(**{'%s'%school_type: school}) )
            # avoid list all profiles
            if not q_objs:
                #raise ValidationError('No %s set for current user'%school_type)
                return Profile.objects.none()
            q_obj = reduce(operator.or_, q_objs)
            profile_qs = profile_qs.filter(q_obj)
        return profile_qs
alumni = AlumniProfileListView.as_view()                             
            