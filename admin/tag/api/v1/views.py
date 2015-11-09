
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework_bulk.generics import BulkModelViewSet

from admin.tag.api.v1.serializers import TagSerializer
from admin.tag.api.v1.filtersets import TreeTagGenericFilterSet, \
    TagGenericFilterSet
from admin.tag.api.v1.serializers import TreeTagSerializer, \
    TreeTagMoveNodeSerializer
from tag.models import Tag, TreeTag, TreeTaggedItem


class TreeTagViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TreeTag.objects.all()
    serializer_class = TreeTagSerializer
    filter_class = TreeTagGenericFilterSet
    search_fields = ('name', 'slug', )
    
    def update(self, request, *args, **kwargs):
        # special for rename functionality
        if all([kwargs.get('partial', False),
                'reslugify' in request.data,
                request.data.get('name', False), ]):
            # short term solution
            name = request.data.get('name')
            instance = self.get_object()
            request.data.pop('reslugify')
            request.data.update({'slug': instance.slugify(name)})
        return super(TreeTagViewSet, self).update(request, *args, **kwargs)
    
    @detail_route(methods=['PUT', 'POST', ])
    def move(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TreeTagMoveNodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        target = serializer.validated_data['target']
        position = serializer.validated_data['position']
        instance.move_to(target, position)
        general_serializer = self.get_serializer(instance)
        return Response(general_serializer.data)
    
    @list_route(methods=['GET'])
    def cumulative_count(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = queryset.model._tree_manager.add_related_count(queryset, 
                        TreeTaggedItem, 'tag', 'cumulative_count', cumulative=True) # accumulative affirmative
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class TagViewSet(BulkModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_class = TagGenericFilterSet
    search_fields = ('name', 'slug', )