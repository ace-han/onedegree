'''
Created on Sep 5, 2015

@author: ace
'''
from django.db.models.fields import Field
from django.utils.translation import ugettext_lazy as _

from taggit.managers import _TaggableManager, TaggableRel, TaggableManager as TaggableField
from taggit.models import TaggedItem

'''
    though not using it afterwards since sub-serializer class for TaggedItem 
    always goes with a TaggedItemRelatedField
    this field for those Model Class just only for display purpose (read_only=True)
    take it as a default behavior like the 
        early account.Profile.tags = TaggableManager 
        and a default ProfileSerializer without any field definition
'''
class TaggableManager(TaggableField):
    # Field flags
    many_to_many = True
    many_to_one = False
    one_to_many = False
    one_to_one = False

    _related_name_counter = 0

    def __init__(self, verbose_name=_("Tags"),
                 help_text=_("A comma-separated list of tags."),
                 through=None, blank=False, related_name=None, to=None,
                 manager=_TaggableManager):
        '''
            copy from taggit.managers.py 
            taggit version: 0.17.0 
            just because the original one doesnot support serializable by default
        '''
        self.through = through or TaggedItem
        self.swappable = False
        self.manager = manager

        rel = TaggableRel(self, related_name, self.through, to=to)

        Field.__init__(
            self,
            verbose_name=verbose_name,
            help_text=help_text,
            blank=blank,
            null=True,
            serialize=True, # make it serialize-able 
            rel=rel,
        )
        # NOTE: `to` is ignored, only used via `deconstruct`.
    
    '''
        those method with __xxx__ should copy along, too
    '''
        
    def __get__(self, instance, model):
        if instance is not None and instance.pk is None:
            raise ValueError("%s objects need to have a primary key value "
                             "before you can access their tags." % model.__name__)
        manager = self.manager(
            through=self.through,
            model=model,
            instance=instance,
            prefetch_cache_name=self.name
        )
        return manager
    
    def __lt__(self, other):
        """
        Required contribute_to_class as Django uses bisect
        for ordered class contribution and bisect requires
        a orderable type in py3.
        """
        return False