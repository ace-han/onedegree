
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework_bulk.generics import BulkModelViewSet

from admin.tag.api.v1.filterset import TreeTagGenericFilterSet
from admin.tag.api.v1.serializers import TreeTagSerializer, \
    TreeTagMoveNodeSerializer
from tag.models import TreeTag


class TreeTagViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TreeTag.objects.all()
    serializer_class = TreeTagSerializer
    filter_class = TreeTagGenericFilterSet
    
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