from account.models import Profile
from friend.models import PhoneContactRecord


def __prepare_route(route):
    return {
        'total_weight': len(route),
        'weights': [],
        'profile_ids': route,
    }
    
def calculate_social_routes(src, dest):
    '''
        return all (profile_id_set all relevant profile_id, routes between src and dest)
        profile_id_set = set(), routes = [
            {
                total_weight: n, 
                weights: [n...],
                profile_ids: [
                    profile_id1, 
                    profile_id2, 
                    profile_id3
                ]
            },
            {...},
            {...},
        ]
    '''
    dest = Profile.objects.get(user_id=4)
    
    to_profile_ids = PhoneContactRecord.objects.filter(from_profile=dest).values_list('to_profile_id', flat=True)
    p_qs = Profile.objects.filter(id__in=to_profile_ids).values_list('id', flat=True)

    result = []
    result.append( __prepare_route(p_qs[:2]) ) 
    result.append( __prepare_route(p_qs[2:5]) )
    result.append( __prepare_route(p_qs[5:9]) )
    result.append( __prepare_route(p_qs[9:15]) )
    return p_qs, result
