'''
total weight, the smallest one wins 
overall weight config
a             1°SS         2
a             1°S          4
b             1°SS         8
b             1°S          16
a             1°           32
b             1°           64
other         1°SS         128
other         1°S          256
other         1°           512
a             SS           1024 1*2**10
a             S            2048 2
b             SS           1024 1
b             S            2048 2
other         SS           8096 3
other         S            16192 4
'''
'''
since we need numpy to speed up, the key may vary a little 
A = 2d array of {0, 1} (0 no contact record, 1 otherwise )
B = 2d array of {0, 1, 2} (0 no alumni, 1 alumni of one school, 2 alumni of two schools)
1. we need * operation to calculate how strong the relationship is,
2. and we separately compare src and dest also need to avoid 1...7
so to avoid 0 we do below
    (A+8)*(B+1) = C
    {8, 9} * {1, 2, 3}
C = 2d array of {8, 16, 24, 9, 18, 27, }

8 means no contact at all, just for matrix padding purpose...

16 S
24 SS
9  1° 
18 1°S
27 1°SS

then I have decided no to get src and dest in the matrix, 
too many special coding and slow...
but (A+8) is still fine


a             7, 1°SS         2
a             6, 1°S          4
a             5, 1° S         4         
a             4, 1°           32
a             3, SS           1024 1*2**10
a             2, S            2048
a             1, S            2048
'''

import bisect

from django.db.models import F

from account.models import Profile, School
from friend.models import PhoneContactRecord
import numpy as np


SRC_WEIGHT_CONFIG = {
        7: 2,
        6: 4,
        5: 4,
        4: 32,
        3: 1024,
        2: 2048,
        1: 2048,
        # below for from matrix
#         27: 2,
#         18: 4,
#         9: 32,
#         24: 1024,
#         16: 2048,
}

'''
                1 1 1
b             7, 1°SS         8
b             6, 1°S          16
b             5, 1° S         16        
b             4, 1°           64
b             3, SS           1024 1*2**10
b             2, S            2048
b             1, S            2048
'''
DEST_WEIGHT_CONFIG = {
        7: 8,
        6: 16,
        5: 16,
        4: 64,
        3: 1024,
        2: 2048,
        1: 2048,
        
        # below for from matrix
#         27: 8,
#         18: 16,
#         9: 64,
#         24: 1024,
#         16: 2048,
}

'''
                1 1 1
other         7, 1°SS         128
other         6, 1°S          256
other         5, 1° S         256
other         4, 1°           512
other         3, SS           8096
other         2, S            16192
other         1,  S           16192 4*(2**10)
'''
OTHER_WEIGHT_CONFIG = {        
        27: 128,
        18: 256,
        9: 512,
        24: 8096,
        16: 16192,
}

def prepare_friend_context(profile, contact_qs):
    '''
        just a tool function to retrieve necessary info from profile
        return 
            contact_profile_id_set, (id only)
            high_school_profile_id_set, (id only)
            college_profile_id_set, (id only)
            id_profile_dict, {id: {id: , high_school_id: , college_id: }} 
            sorted_ids, (sorted array )
    '''
    friend_id_profile_dict = {}
    contact_profile_id_set = set()
    high_school_profile_id_set = set()
    college_profile_id_set = set()
    
    if profile.high_school_id:
        high_school_alumni_qs = Profile.objects.exclude(id=profile.id).filter(
                                        high_school_id=profile.high_school_id).values('id', 
                                        'high_school_id', 'college_id')
    
        for p in high_school_alumni_qs:
            friend_id_profile_dict[ p['id'] ] = p
            high_school_profile_id_set.add( p['id'] )
    if profile.college_id:
        college_alumni_qs = Profile.objects.exclude(id=profile.id).filter(
                                        college_id=profile.college_id).values('id', 
                                        'high_school_id', 'college_id')
    
        for p in college_alumni_qs:
            friend_id_profile_dict[ p['id'] ] = p
            college_profile_id_set.add( p['id'] )

    for p in contact_qs:
        p['id'] = p.pop('profile_id') # to align the naming pattern
        friend_id_profile_dict[ p['id'] ] = p
        contact_profile_id_set.add( p['id'] )

    # move to resolve_4_node_route
    # sorted_ids = friend_id_profile_dict.keys().sort()
    return (contact_profile_id_set, high_school_profile_id_set, 
            college_profile_id_set, friend_id_profile_dict,)

def prepare_src_friend_context(profile):
    pcr_qs = PhoneContactRecord.objects.filter(from_profile=profile)\
        .annotate(high_school_id=F('to_profile__high_school_id'), 
                  college_id=F('to_profile__college_id'),
                  # profile_id to avoid django db id confusion 
                  profile_id=F('to_profile_id')).values('profile_id', 'high_school_id', 'college_id')
    
    return prepare_friend_context(profile, pcr_qs)
    
def prepare_dest_friend_context(profile):
    pcr_qs = PhoneContactRecord.objects.filter(to_profile=profile)\
        .annotate(high_school_id=F('from_profile__high_school_id'), 
                  college_id=F('from_profile__college_id'),
                  # profile_id to avoid django db id confusion 
                  profile_id=F('from_profile_id')).values('profile_id', 'high_school_id', 'college_id')

    return prepare_friend_context(profile, pcr_qs) 
    
def __init_route():
    return {
        'total_weight': 0,
        'weights': [],
        'profile_ids': [],
    }

def __add_route_node(route, node, weight, closed=False):
    '''
        when closed==True, calculate the total_weight
    '''
    route['weights'].append(weight)
    route['profile_ids'].append(node)
    if closed:
        route['total_weight'] = sum(route['weights'])

def resolve_target_relevant_weight(node, friend_context, weight_config):
    '''
        return None means no relationship
        
        let's do some bit operation
        7 = 1 1 1
            1°S S
            4 2 1
        
    '''
    (contact_profile_id_set, high_school_profile_id_set, 
            college_profile_id_set, _,) = friend_context
    relationship = 0
    if node in contact_profile_id_set:
        relationship |= 4
    if node in high_school_profile_id_set:
        relationship |= 2
    if node in college_profile_id_set:
        relationship |= 1
    
    return weight_config.get(relationship, None)


def resolve_src_relevant_weight(node, src_friend_context):
    '''
        return None means no connection
    '''
    return resolve_target_relevant_weight(node, src_friend_context, SRC_WEIGHT_CONFIG)

def resolve_dest_relevant_weight(node, dest_friend_context):
    
    return resolve_target_relevant_weight(node, dest_friend_context, DEST_WEIGHT_CONFIG)

def resolve_middle_relevant_weight(relationship):
    return OTHER_WEIGHT_CONFIG.get(relationship, 0)

def resolve_2_node_routes(src, dest, src_friend_context, dest_friend_context):
    '''
        handle src->dest situation 
            weight is based on src not dest
    '''
    weight = resolve_src_relevant_weight(dest, src_friend_context)
    result = []
    if weight is None:
        return result
    
    route = __init_route()
    __add_route_node(route, dest.id, weight, closed=True)
    result.append(route)
    return result

def resolve_3_node_routes(src, dest, src_friend_context, dest_friend_context):
    _, _, _, src_friend_id_profile_dict = src_friend_context
    _, _, _, dest_friend_id_profile_dict = dest_friend_context
    src_friend_ids = src_friend_id_profile_dict.keys()
    dest_friend_ids = dest_friend_id_profile_dict.keys()
    middle_node_profile_ids = np.intersect1d(src_friend_ids, dest_friend_ids)
    result = []
    for node in middle_node_profile_ids:
        route = __init_route()
        weight = resolve_src_relevant_weight(node, src_friend_context)
        __add_route_node(route, node, weight, closed=False)
        weight = resolve_dest_relevant_weight(node, dest_friend_context)
        __add_route_node(route, node, weight, closed=True)
    
    return result


def __get_index(sorted_list, value):
    return bisect.bisect_left(sorted_list, value)

def prepare_contact_2d_relationship_array(
                        src_friend_id_profile_dict, dest_friend_id_profile_dict,
                        src_sorted_profile_ids, dest_sorted_profile_ids):
    '''
        return numpy.array composed by {0, 1}
        0 no contact connection, 1 otherwise
    '''    
    pcr_qs = PhoneContactRecord.objects.filter(from_profile_id__in=src_sorted_profile_ids,
            to_profile_id__in=dest_sorted_profile_ids).values_list('from_profile_id', 'to_profile_id')
    
    
    relationship_array = np.zeros((len(src_sorted_profile_ids), 
                                   len(dest_sorted_profile_ids)), dtype=np.uint8)
    for from_profile_id, to_profile_id in pcr_qs:

        relationship_array[__get_index(src_sorted_profile_ids, from_profile_id), 
                           __get_index(dest_sorted_profile_ids, to_profile_id)] = 1
    
    
    return relationship_array
    
def __setup_school_relationship_array(school_relationship_array, 
                                      sorted_profile_ids, 
                                      school_ids,
                                      friend_id_profile_dict):
    for idx, profile_id in enumerate(sorted_profile_ids):
        profile_info = friend_id_profile_dict[profile_id]
        if profile_info['high_school_id']:
            # maybe None
            school_relationship_array[idx, __get_index(school_ids, profile_info['high_school_id'])] = 1
        if profile_info['college_id']:
            school_relationship_array[idx, __get_index(school_ids, profile_info['college_id'])] = 1



def prepare_alumni_2d_relationship_array(
                        src_friend_id_profile_dict, dest_friend_id_profile_dict,
                        src_sorted_profile_ids, dest_sorted_profile_ids):
    '''
        return numpy.array composed by {0, 1, 2}
        0 no school connection, 1 sharing one school, 2 for two
    '''
    school_ids = School.objects.values_list('id', flat=True).order_by('id')
    school_ids = list(school_ids)
    src_school_relationship_array = np.zeros( (len(src_sorted_profile_ids), len(school_ids) ), 
                                              dtype=np.uint8)
    
    
    dest_school_relationship_array = np.zeros( (len(dest_sorted_profile_ids), len(school_ids)), 
                                               dtype=np.uint8)
    
    __setup_school_relationship_array(src_school_relationship_array,
                                      src_sorted_profile_ids, school_ids,
                                      src_friend_id_profile_dict)

    __setup_school_relationship_array(dest_school_relationship_array,
                                      dest_sorted_profile_ids, school_ids,
                                      dest_friend_id_profile_dict )
    
    #np.dot({ {a's friends} school}  { {b's friends} school}.T)
    alumni_2d_relationship_array = np.dot( src_school_relationship_array, dest_school_relationship_array.T )
    return alumni_2d_relationship_array
    
def resolve_4_node_routes(src, dest, src_friend_context, dest_friend_context):
    _, _, _, src_friend_id_profile_dict = src_friend_context
    _, _, _, dest_friend_id_profile_dict = dest_friend_context
    
    src_sorted_profile_ids = sorted( src_friend_id_profile_dict.keys() )
    dest_sorted_profile_ids = sorted( dest_friend_id_profile_dict.keys() )
    
    # naming array to avoid confusion in numpy
    contact_array = prepare_contact_2d_relationship_array(
                        src_friend_id_profile_dict, dest_friend_id_profile_dict,
                        src_sorted_profile_ids, dest_sorted_profile_ids)
    
    alumni_array = prepare_alumni_2d_relationship_array(
                        src_friend_id_profile_dict, dest_friend_id_profile_dict,
                        src_sorted_profile_ids, dest_sorted_profile_ids)
   
    # (A+8)*(B+1) = C
    relationship_array = (contact_array+8)*(alumni_array+1)
    #     >>> x = np.eye(3)
    #     >>> x
    #     array([[ 1.,  0.,  0.],
    #            [ 0.,  1.,  0.],
    #            [ 0.,  0.,  1.]])
    #     >>> np.nonzero(x)
    #     (array([0, 1, 2]), array([0, 1, 2]))
    #     
    #     >>> x[np.nonzero(x)]
    #     array([ 1.,  1.,  1.])
    #     >>> np.transpose(np.nonzero(x))
    #     array([[0, 0],
    #            [1, 1],
    #            [2, 2]])
    index_array = np.transpose(np.nonzero(relationship_array>8))
    # a->node2->node3->b
    dest_id = dest.id
    result = []
    for row in index_array:
        node2 = src_sorted_profile_ids[ row[0] ]
        node3 = dest_sorted_profile_ids[ row[1] ]
        
        route = __init_route()
        weight = resolve_src_relevant_weight(node2, src_friend_context)
        __add_route_node(route, node2, weight, closed=False)
        
        if node2 != node3:
            relationship = relationship_array[row[0], row[1]]
            weight = resolve_middle_relevant_weight(relationship)
            __add_route_node(route, node3, weight, closed=False)
        
        weight = resolve_dest_relevant_weight(node3, dest_friend_context)
        __add_route_node(route, dest_id, weight, closed=True)
        result.append(route)

    return result    

def calculate_social_routes_by_user_id(src_id, dest_id):
    # for test only
    return calculate_social_routes(Profile.objects.get(user_id=src_id), 
                                   Profile.objects.get(user_id=dest_id))

def calculate_social_routes_by_profile_id(src_id, dest_id):
    # for test only
    return calculate_social_routes(Profile.objects.get(id=src_id), 
                                   Profile.objects.get(id=dest_id))

def calculate_social_routes(src, dest, src_included=False):
    '''
        return all routes between src and dest
        routes = [
            {
                total_weight: n, 
                weights: [edge1_weight, edge2_weight, ...],
                profile_ids: [
                    profile_id1(node1), 
                    profile_id2(node2), 
                    profile_id3(node3),
                ]
            },
            {...},
            {...},
        ]
        
        We only handle below situations:
        1. src->dest
        2. src->?->dest
        3. src->?->?->dest
        
        
        define
            -> as edge
            src, ?, dest as node
            
        
    '''
    candidate_routes = []
    src_friend_context = prepare_src_friend_context(src)
    dest_friend_context = prepare_dest_friend_context(dest)
    
    if len(src_friend_context[-1])==0 or len(dest_friend_context[-1])==0:
        # start points or end points has no friends at all...
        return []

    # I just did (A+3)*(B+1)
    # A: mobile contact relationship Matrix
    # B: school relationship matrix
    
    # since we need numpy to speed up, the key may vary a little 
    # A = 2d array of {0, 1} (0 no contact record, 1 otherwise )
    # B = 2d array of {0, 1, 2} (0 no alumni, 1 alumni of one school, 2 alumni of two schools)
    # we need * operation to calculate how strong the relationship is, 
    # so to avoid 0 we do below
    #     (A+8)*(B+1) = C
    # src->dest has direct connection?
    two_node_routes = resolve_2_node_routes(src, dest, src_friend_context, dest_friend_context)
    candidate_routes.extend(two_node_routes)
    
    # src -> ? ->dest
    three_node_routes = resolve_3_node_routes(src, dest, src_friend_context, dest_friend_context)
    candidate_routes.extend(three_node_routes)
    
    #  src -> ? -> ? ->dest
    four_node_routes = resolve_4_node_routes(src, dest, src_friend_context, dest_friend_context)
    candidate_routes.extend(four_node_routes)
    
    candidate_routes.sort(key=lambda x: x['total_weight'])

    return candidate_routes

def calculate_topN_social_routes(src, dest, n):
    
    sorted_routes = calculate_social_routes(src, dest)
    
    sorted_routes = sorted_routes[:n]
    
    return sorted_routes