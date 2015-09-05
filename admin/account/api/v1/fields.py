from rest_framework import serializers
from rest_framework.relations import RelatedField


class TaggedItemRelatedField(serializers.PrimaryKeyRelatedField):
    """
    A custom field to use for the `tagged_object` generic relationship.
    """
    def __init__(self, **kwargs):
        self.pk_field = kwargs.pop('pk_field', None)
        kwargs.pop('many', None)
        kwargs.pop('allow_empty', None)
        self.queryset = kwargs.pop('queryset', self.queryset)
        super(RelatedField, self).__init__(**kwargs)
        
    def to_internal_value(self, data):
        value = serializers.PrimaryKeyRelatedField.to_internal_value(self, data)
#         self.root.instance => Profile instance
#         relationship = get_attribute(instance, self.source_attrs)
#         relationship.set(*value)
        return value
#     def to_representation(self, value):
#         """
#         Serialize tagged objects to a simple textual representation.
#         """
#         raise Exception('Unexpected type of tagged object')