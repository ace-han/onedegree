
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
            tag = d.decode( tag )
        return super(TreeTag, self).slugify(tag, i) 