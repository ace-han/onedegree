from django_filters.filters import MultipleChoiceFilter  # , ModelMultipleChoiceFilter
from django_filters.filterset import FilterSet

from friend.models import PhoneContactRecord


class PhoneContactRecordGenericFilterSet(FilterSet):

    id = MultipleChoiceFilter(name='id',
                              # here extra parameter will be passed to field_class 
                              choices=PhoneContactRecord.objects.values_list('id', 'to_phone_num'))
    class Meta:
        model = PhoneContactRecord