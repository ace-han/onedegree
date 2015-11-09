# from common.filters.list import ListFilter
'''
    for future filtering in rest api
        1. Almost one FilterSet on one ViewSet(View/ View Function)
        2. in order to support bulk delete/id query, id field(int-typed) could be using MultipleChoiceFilter as below
        3. MultipleChoiceFilter has already taken care of whether the parameter is single or plural form by lookup='in'
        4. for string query, please see to search functionality in rest_framework.filters.SearchFilter
        5. (Deprecated.Affirmative) comma-separated list filter is a little bit weird and no in a consistent pattern 
                        when doing form submission 
        6. Don't do ModelMultipleChoiceFilter on an id(pk) field unless it's a ForeignKey
'''

from django_filters.filters import MultipleChoiceFilter  # , ModelMultipleChoiceFilter
from django_filters.filterset import FilterSet

from tag.models import Tag, TreeTag


class TreeTagGenericFilterSet(FilterSet):
    #id = ListFilter(name='id')
    #id = ModelMultipleChoiceFilter(name='id')    # don't do M  

    id = MultipleChoiceFilter(name='id',
                              # here extra parameter will be passed to field_class 
                              choices=TreeTag.objects.values_list('id', 'slug'))
    class Meta:
        model = TreeTag

class TagGenericFilterSet(FilterSet):
    #id = ListFilter(name='id')
    #id = ModelMultipleChoiceFilter(name='id')    # don't do M  

    id = MultipleChoiceFilter(name='id',
                              # here extra parameter will be passed to field_class 
                              choices=Tag.objects.values_list('id', 'slug'))
    class Meta:
        model = Tag