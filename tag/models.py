
from __future__ import unicode_literals
from functools import partial
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from taggit.models import TagBase, ItemBase, GenericTaggedItemBase


# from django.db import models
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def slugify(instance):
    return partial(do_slugify, instance)

def do_slugify(instance, tagName, adjust=None):
    
    '''
        instance must be descendant instance of TagBase
    '''
    
    if not is_ascii(tagName):
        # it's very rare invocation
        from unihandecode import Unihandecoder
        # I decide to use zh only first
        # it seems zh could also do ja
        # s = '明天明天的风吹明日は明日の風が吹く'
        # zh_d = Unihandecoder(lang='zh')
        # zh_d.decode(s)
        # 'Ming Tian Ming Tian De Feng Chui Ming Ri haMing Ri noFeng gaChui ku'
        # ja_d = Unihandecoder(lang='ja')
        # ja_d.decode(s)
        # 'Mei Tenmei Ten Teki Sui Ashita ha Ashita no Kaze ga Fuku'
        d = Unihandecoder(lang='zh') 
        tag = d.decode( tagName )
    # In this way, Tag object take curry bind self to this function
    return TagBase.slugify(instance, tagName, adjust)

# Please note that if you are using multi-inheritance, 
# MPTTModel should usually be the first class to be inherited from
class TreeTag(MPTTModel, TagBase):
    # The preferred way to do model registration in django-mptt is by subclassing MPTTModel.
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    
    # background_color = models.CharField(_(''), max_length=16)
    
    def slugify(self, tag, i=None):
        return do_slugify(self, tag, i)
    
    def __str__(self):
        return self.name


'''
    below copy from taggit.models
'''
class TaggedItemBase(ItemBase):
    tag = models.ForeignKey('tag.TreeTag', related_name="%(app_label)s_%(class)s_items")

    class Meta:
        abstract = True

    @classmethod
    def tags_for(cls, model, instance=None, **extra_filters):
        kwargs = extra_filters or {}
        if instance is not None:
            kwargs.update({
                '%s__content_object' % cls.tag_relname(): instance
            })
            return cls.tag_model().objects.filter(**kwargs)
        kwargs.update({
            '%s__content_object__isnull' % cls.tag_relname(): False
        })
        return cls.tag_model().objects.filter(**kwargs).distinct()


class TaggedItem(GenericTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = _("Tagged Item")
        verbose_name_plural = _("Tagged Items")