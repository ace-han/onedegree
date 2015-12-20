'''
Created on Sep 6, 2015

@author: ace
'''

from django.core.management.base import BaseCommand

from account.models import Profile
from account.utils import format_phonenumber


class Command(BaseCommand):
    help = (
        'Format all the phone numbers in profile table to E164 standard. '
        'e.g.: python manage.py format_phoenumbers --settings onedegree.settings.dev'
    )

    def add_arguments(self, parser):
        pass
        

    def handle(self, *args, **options):
        self.stdout.write('options: %s'% ( options ) )
        err_msgs = []
        err_msg_tpl = 'id: %d, phone_num: %s, error: %s'
        p_qs = Profile.objects.all().only('id', 'phone_num')
        for p in p_qs:
            phone_num = p.phone_num
            try:
                phone_num = format_phonenumber(phone_num)
                p.save()
            except Exception as e:
                err_msgs.append(err_msg_tpl % (p.id, p.phone_num, e))
        
        
        self.stdout.write('total proceeded: %d, failure count: %d'% ( len(p_qs), len(err_msgs) ) )
        if len(err_msgs)>0:
            self.stdout.write('errors: %s\n' % ( '\n'.join(err_msgs) ) )