import json
import sys
import requests
import logging
 
def post(fmc_info, endpoint, post_data):

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
    
    headers['X-auth-access-token']=auth_token
    
    api_path_base = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/"
    url = server + api_path_base + endpoint
    if (url[-1] == '/'):
        url = url[:-1]
    
    json_resp = None
    try:
        r = requests.post(url, data=json.dumps(post_data), headers=headers, verify=False)
        status_code = r.status_code
        resp = r.text
        logging.info("Status code is: %s", str(status_code))
        if status_code == 201 or status_code == 202:
            logging.info("Post was successful...")
            json_resp = json.loads(resp)
            logging.debug(json.dumps(json_resp,sort_keys=True,indent=4, separators=(',', ': ')))
        else :
            r.raise_for_status()
            logging.error("Error occurred in POST: %s", resp)
    except requests.exceptions.HTTPError as err:
        logging.error("Error in connection: %s", str(err))
    finally:
        if r: r.close()
                
    return json_resp
 
