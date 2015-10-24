from django_filters.filters import MultipleChoiceFilter  # , ModelMultipleChoiceFilter
from django_filters.filterset import FilterSet

from authx.models import User


class UserGenericFilterSet(FilterSet):

    id = MultipleChoiceFilter(name='id',
                              # here extra parameter will be passed to field_class 
                              choices=User.objects.values_list('id', 'username'))
    class Meta:
        model = User
