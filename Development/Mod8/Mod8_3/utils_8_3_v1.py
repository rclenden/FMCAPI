#A file for useful functions
import json
import sys
import requests
import logging

def print_item_list(item_list):
    for item in item_list:
        print(f'{item["name"]}   {item["id"]}')


def get_token(fmc_info):
    server = fmc_info['server']
    username = fmc_info['username']
    password = fmc_info['password']
                
    r = None
    headers = {'Content-Type': 'application/json'}
    api_auth_path = "/api/fmc_platform/v1/auth/generatetoken"
    auth_url = server + api_auth_path
    try:
        r = requests.post(auth_url, headers=headers, auth=requests.auth.HTTPBasicAuth(username,password), verify=False)
        auth_headers = r.headers
        auth_token = auth_headers.get('X-auth-access-token', default=None)
        if auth_token == None:
            logging.error("auth_token not found. Exiting...")
            sys.exit()
    except Exception as err:
        logging.error("Error in generating auth token: %s", str(err))
        sys.exit()
    
    return auth_token