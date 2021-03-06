import base64
from functools import reduce
import operator

from django.db.models.query_utils import Q
from django.db.transaction import atomic
from rest_condition import Or
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, list_route
from rest_framework.exceptions import ValidationError, ParseError
from rest_framework.generics import get_object_or_404, ListAPIView, \
    ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from account.models import Profile, SCHOOL_TYPES
from account.utils import format_phonenumber
from authx.permissions import IsAdminUser, SelfOnly
from friend.api.v1.serializers import FriendProfileSerializer
from friend.api.v1.social_routes import calculate_topN_social_routes
from friend.models import are_friends, PhoneContactRecord
from tag.api.v1.serializers import TagSerializer
from tag.models import TaggedItem, Tag


#from friend.api.v1.filtersets import SocialProfileFilterSet
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
    search_fields = ('occupations__name', 'tags__name', 
                     'user__nickname', 'college__name', 'high_school__name', )
    
    def get_queryset(self):
        user = self.request.user
        profile_qs = Profile.objects.filter(user__isnull=False).exclude(user=user)\
                    .select_related('user', 'college', 'high_school') \
                    .prefetch_related('tags')
        # refer to http://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
        # according to doc, filtering against query_params just like this
        valid_school_type_dict = dict(SCHOOL_TYPES)
        user_profile = get_object_or_404(Profile, user=user)
        school_type = self.request.query_params.get('school_type')
        if school_type and school_type not in valid_school_type_dict:
            raise ValidationError('Invalid school_type, valid options are %s' % (','.join(valid_school_type_dict.keys())))
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

class PhoneContactProfileListView(ListCreateAPIView):
    serializer_class = FriendProfileSerializer
    permission_classes = (IsAuthenticated,
                          Or(IsAdminUser, SelfOnly),)
    search_fields = ('occupations__name', 'tags__name', 
                     'user__nickname', 'college__name', 'high_school__name', )
    
    def get_queryset(self):
        to_profile_id_qs = PhoneContactRecord.objects \
            .filter(from_profile__user__id=self.request.user.id) \
            .values_list('to_profile_id', flat=True)

        profile_qs = Profile.objects.filter(id__in=to_profile_id_qs) \
                    .select_related('user', 'college', 'high_school') \
                    .prefetch_related('tags')
        
        return profile_qs
    
    @atomic
    def create(self, request, *args, **kwargs):
        bulk = isinstance(request.data, list)
        data = request.data if bulk else [request.data] 
        # no more serializers that is not necessary for this creation
        # data should be a list of strings
        formatted_phone_nums = []
        for phone_num_str in data:
            formatted_phone_num = format_phonenumber(phone_num_str, quiet=True)
            if not formatted_phone_num:
                continue
            formatted_phone_nums.append(formatted_phone_num)
        
        p_qs = Profile.objects.filter(phone_num__in=formatted_phone_nums).only('id', 'phone_num')
        records = []
        # create for those not in the system
        phone_numm_profile_dict = dict((p.phone_numm, p) for p in p_qs)
        p_qs = list(p_qs)
        for formatted_phone_num in formatted_phone_nums:
            if formatted_phone_num not in phone_numm_profile_dict:
                p = Profile(phone_num=formatted_phone_num)
                p.save()
                p_qs.append(p)
        
        from_profile = get_object_or_404(Profile, user=self.request.user)
        for p in p_qs:
            records.append(
                PhoneContactRecord(from_profile=from_profile, to_profile=p, to_phone_num=p.phone_num)
            )
        PhoneContactRecord.objects.filter(from_profile=from_profile).delete()
        PhoneContactRecord.objects.bulk_create(records)
        return Response(len(records), status=status.HTTP_201_CREATED)
   
phone_contacts = PhoneContactProfileListView.as_view()

class PhoneContactCountView(PhoneContactProfileListView):
    '''
        just for speed up on and reduce the network transmission
    '''
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        #return Response(qs.none().count())
        return Response(qs.count())
   
phone_contact_count = PhoneContactCountView.as_view()


class SocialProfileListView(ReadOnlyModelViewSet):
    serializer_class = FriendProfileSerializer
    permission_classes = (AllowAny, )
    queryset = Profile.objects.filter(user__isnull=False)
    # filter_class = SocialProfileFilterSet
    # user__username is pretty rare
    search_fields =  ('occupations__name', 'tags__name', 
                     'user__nickname', 'college__name', 'high_school__name', )
    
    def _prepare_route_result(self, route, id_profile_dict):
        '''
            route must be a dict
            return {
                total_weight: n, 
                weights: [n...],
                items: [
                    {id: n, display_name: xxx, is_from_mobile_contact: True/False,}, 
                    {...},
                    {...},
                ], 
                route_code: xxx,
                
            }
        '''
        profile_ids = []
        items = []
        for profile_id in route.pop('profile_ids', []):
            profile_ids.append('%s' % profile_id)
            profile = id_profile_dict[profile_id]
            items.append(profile)
            
        route_code = base64.urlsafe_b64encode( ','.join(profile_ids).encode('utf-8') )
        # We need string instead of bytes
        route_code = route_code.decode('utf-8')
        
        
        route['route_code'] = route_code
        route.update({
            'route_code': route_code,
            'items': items,
        })
        return route
        
    def _extract_route_profile_ids(self, route_code):
        try:
            profile_ids = base64.urlsafe_b64decode(route_code.encode('utf-8'))
            profile_ids = profile_ids.decode('utf-8')
            profile_ids = [int(profile_id) for profile_id in profile_ids.split(',')]
        except Exception as e:
            raise ParseError('route_code is malformed')
        
        return profile_ids
        
    @list_route(['GET',],
                  url_path='social-routes'
                  , permission_classes=[IsAuthenticated,]
            )
    def social_routes(self, request, *args, **kwargs):
        '''
            return a list of [
                {profile_id: ''}
            ]
        '''
        target_user_id = request.query_params.get('target_user')
        
        dest_profile = get_object_or_404(Profile, user_id=target_user_id)
        src_profile = get_object_or_404(Profile, user=request.user)
        routes = calculate_topN_social_routes(src_profile, dest_profile, 10)
        profile_id_set = set()
    
        for route in routes:
            profile_id_set.update(route['profile_ids'])

        p_qs = Profile.objects.filter(id__in=profile_id_set).values('id', 
                                        'user__nickname', 'user__username', 'phone_num')
        id_profile_dict = {}
        for p in p_qs:
            nickname = p.pop('user__nickname')
            username = p.pop('user__username')
            p.update({
                'display_name': nickname or username, 
            })
            # if display_name is '' then from user's own mobile
            if p['display_name']:
                p.pop('phone_num')
            id_profile_dict[ p['id'] ] = p
        result = []
        for route in routes:
            result.append( self._prepare_route_result(route, id_profile_dict) )

        return Response(result)
    
    @list_route(['GET',],
                  url_path='social-route-detail'
                  #, permission_classes=[IsAuthenticated,]
            )
    def social_route_detail(self, request, *args, **kwargs):
        route_code = request.query_params.get('route_code')
        profile_ids = self._extract_route_profile_ids(route_code)
        
        queryset = Profile.objects.filter(id__in=profile_ids)
        serializer = self.get_serializer(queryset, many=True)
        
        profile_id_idx_dict = {}
        for idx, profile_id in enumerate(profile_ids):
            profile_id_idx_dict[profile_id] = idx

        result = [0]*len(profile_ids)
        for profile in serializer.data:
            idx = profile_id_idx_dict.get(profile['id'])
            result[idx] = profile
        return Response(result)
    