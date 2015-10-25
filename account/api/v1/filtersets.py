from django_filters.filters import CharFilter
from django_filters.filterset import FilterSet

from account.models import Profile, School


class UserProfileFilterSet(FilterSet):

    username = CharFilter(name='user__username')
    
    class Meta:
        model = Profile
        # if we don't specify the `fields` it will be `model.filelds+filterset.declare_fields`
        # fields = ['username'] 

'''
# this kind of  expose the structure of object definition
# good for internal projects not for external ones
from url_filter.filtersets import ModelFilterSet

class UserProfileFilterSet(ModelFilterSet):
    
    class Meta:
        model = Profile
'''
        
class SchoolFilterSet(FilterSet):
    class Meta:
        model = School