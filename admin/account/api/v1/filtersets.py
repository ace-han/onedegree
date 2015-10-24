from django_filters.filters import MultipleChoiceFilter, ModelMultipleChoiceFilter
from django_filters.filterset import FilterSet

from account.models import School, Profile
from tag.models import TreeTag


class SchoolGenericFilterSet(FilterSet):

    id = MultipleChoiceFilter(name='id',
                              # here extra parameter will be passed to field_class 
                              choices=School.objects.values_list('id', 'name'))
    class Meta:
        model = School
        
class ProfileGenericFilterSet(FilterSet):

    id = MultipleChoiceFilter(name='id',
                              choices=Profile.objects.values_list('id', 'phone_num'))
    
    tags = ModelMultipleChoiceFilter(name='tags', queryset=TreeTag.objects.all())
    class Meta:
        model = Profile
