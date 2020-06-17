#A file for useful constants

#Endpoints
ACCESS_POLICIES = 'policy/accesspolicies'
OBJECT_NETWORKS = 'object/networks'
OBJECT_HOSTS = 'object/hosts'
OBJECT_RANGES = 'object/ranges'
OBJECT_NETWORK_ADDRESSES = 'object/networkaddresses'
OBJECT_NETWORK_GROUPS = 'object/networkgroups'

OBJECT_MAP = {
    'Networks': OBJECT_NETWORKS,
    'Ranges': OBJECT_RANGES,
    'Hosts': OBJECT_HOSTS,
    'NetworkAddresses': OBJECT_NETWORK_ADDRESSES,
    'NetworkGroups': OBJECT_NETWORK_GROUPS
}

OBJECT_TYPE_MAP = {
    'Network': OBJECT_NETWORKS,
    'Range': OBJECT_RANGES,
    'Host': OBJECT_HOSTS,
    'NetworkAddress': OBJECT_NETWORK_ADDRESSES,
    'NetworkGroup': OBJECT_NETWORK_GROUPS
}