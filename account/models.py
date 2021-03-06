
from django.conf import settings
from django.db import models
from taggit.managers import TaggableManager
# from tag.fields import TaggableManager

from tag.models import TaggedItem, TreeTaggedItem


SCHOOL_TYPES = (
                ('high_school', 'High School'), 
                ('college', 'College'), 
            )


CITY_CHOICES = (
                ('beijing', '北京'), 
                ('shanghai', '上海'), 
                ('guangzhou', '广州'), 
                ('shenzhen', '深圳'), 
            )

GENDER_TYPES = (
                (None, 'Unknown', ), 
                (0, 'Female', ), 
                (1, 'Male', ), 
            )


class School(models.Model):
    name = models.CharField(max_length=32, unique=True)
    type = models.CharField(max_length=16, choices=SCHOOL_TYPES)
    remark = models.TextField(max_length=255, blank=True)
    
    def __str__(self):
        return '%s: %s' % (self.type, self.name, ) 

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    phone_num = models.CharField(max_length=24, unique=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    gender = models.SmallIntegerField(null=True, choices=GENDER_TYPES)
    city = models.CharField(max_length=16, choices=CITY_CHOICES, blank=True)
    whatsup = models.CharField(max_length=255, blank=True)
    high_school = models.ForeignKey('account.School', related_name='high_school',
                                    null=True, blank=True, on_delete=models.SET_NULL)
    college = models.ForeignKey('account.School', related_name='college',
                                null=True, blank=True, on_delete=models.SET_NULL)
    # for occupation, let's delegate to tree tag for the time being
    occupations = TaggableManager(through=TreeTaggedItem)  # switch back to the original TaggableManager
    
    # for company and other tags, let's delegate to tag... for the time being
    tags = TaggableManager(through=TaggedItem)
    
    def __str__(self):
        return '%s' % (self.user or self.phone_num)