from django.db import models
from django.db.models.query_utils import Q


def are_friends(profile1, profile2):
    if profile1.high_school is not None \
        and profile2.high_school is not None \
        and profile1.high_school.id == profile2.high_school.id:
        return True
    
    if profile1.college is not None \
        and profile2.college is not None \
        and profile1.college.id == profile2.college.id:
        return True
    
    cr_qs = ContactRecord.objects.filter(
            Q(from_profile=profile1, to_profile=profile2)|Q(from_profile=profile2, to_profile=profile1)
    )
    if cr_qs.exists():
        return True
    
    return False

class ContactRecord(models.Model):
    from_profile = models.ForeignKey('account.Profile', related_name='from_profile')
    to_profile = models.ForeignKey('account.Profile', related_name='to_profile')
    # reduce table join query, and then a crontab to ensure it's synced with to_profile's phone_num daily
    to_phone_num = models.CharField(max_length=24)
    
    class Meta:
        unique_together = (('from_profile', 'to_profile'),)
