import get_7_1_v1 as get

fmc_info = {
    'server': 'https://10.81.127.36',
    'username': 'api',
    'password': 'superpass'
}

endpoint = 'policy/accesspolicies'

print (get.get_object(fmc_info, endpoint))
    