
from __future__ import unicode_literals

# from django.db import models
from mptt.models import MPTTModel
from taggit.models import TagBase
from mptt.fields import TreeForeignKey


def is_ascii(s):
    return all(ord(c) < 128 for c in s)

# Please note that if you are using multi-inheritance, 
# MPTTModel should usually be the first class to be inherited from
class TreeTag(MPTTModel, TagBase):
    # The preferred way to do model registration in django-mptt is by subclassing MPTTModel.
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    
    # background_color = models.CharField(_(''), max_length=16)
    
    def slugify(self, tag, i=None):
        if not is_ascii(tag):
            # it's very rare invocation
            from unihandecode import Unihandecoder
            d = Unihandecoder(lang='zh') # I decide to use zh only first
            tag = d.decode( tag )
        return super(TreeTag, self).slugify(tag, i) 