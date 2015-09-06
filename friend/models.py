from django.db import models


class ContactRecord(models.Model):
    from_profile = models.ForeignKey('account.Profile', related_name='from_profile')
    to_profile = models.ForeignKey('account.Profile', related_name='to_profile')
    # reduce table join query, and then a crontab to ensure it's synced with to_profile's phone_num daily
    to_phone_num = models.CharField(max_length=24)
    
    class Meta:
        unique_together = (('from_profile', 'to_profile'),)
