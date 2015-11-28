'''
Created on Sep 6, 2015

@author: ace
'''
from _functools import reduce
from argparse import ArgumentTypeError
from gettext import gettext as _
import operator
import re

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models.query_utils import Q

from account.models import Profile


RANGE_REGEX = re.compile('range\(([^)]+)\)')

class Range(object):
    '''
        convert range(n,m,step) to a list
    '''
    
    def __call__(self, string):
        m = RANGE_REGEX.match(string)
        if not m:
            message = _('range string: %s is not parsable')
            raise ArgumentTypeError(message % (string))

        try:
            range_args = [int(part) for part in m.group(1).split(',')]
            return range(*range_args)
        except (ValueError, TypeError) as e:
            message = _('range string: %s is not parsable: %s')
            raise ArgumentTypeError(message % (string, e))

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, repr(range))

class Command(BaseCommand):
    help = (
        'Patching a generated user to a specified profile with test_user? prefix and the same password as username'
        'e.g.: python manage.py patch_test_user --settings onedegree.settings.dev -r "range(1,9,2)" "range(2,8)"'
    )
    
    user_prefix = 'test_user'
    user_model = get_user_model()
    def add_arguments(self, parser):
        parser.add_argument('-f', '--force', action='store_true',
                            help='Force to overwrite existing associated user')
        parser.add_argument('-r', '--ranges', nargs='*', type=Range(),
                            help='A list of profile ids in the format of range(n,m,step), step is optional')

    def handle(self, *args, **options):
        self.stdout.write('options: %s'% ( options ) )
        
        profile_qs = Profile.objects.all()
        if options['ranges']:
            q_objs = [Q(id__in=r) for r in options['ranges'] ]
            profile_qs = profile_qs.filter( reduce(operator.or_, q_objs) )
        newly_created_count = 0  
        if options['force']:
            for profile in profile_qs:
                if self._prepare_consistent_user_profile(profile):
                    newly_created_count += 1
        else:
            for profile in profile_qs:
                if self._prepare_user_profile_if_necessary(profile):
                    newly_created_count += 1
        
        self.stdout.write('total profile: %d, newly created: %d'% ( profile_qs.count(), newly_created_count ) )
        
    def _prepare_consistent_user_profile(self, profile):
        username = '%s%s' % (self.user_prefix, profile.id)
        user, created = self.user_model.objects.get_or_create(username=username)
        user.set_password(username)
        user.save()
        profile.user = user
        profile.save()
        return created
            
    def _prepare_user_profile_if_necessary(self, profile):
        if profile.user_id:
            return
        return self._prepare_consistent_user_profile(profile)