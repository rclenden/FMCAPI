import json
import sys
import requests
import logging

def get_object(fmc_info, endpoint=None, url=None):
    if url == None:
        server = fmc_info['server']
        path_base = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/"
        url = server + path_base + endpoint
        if (url[-1] == '/'):
            url = url[:-1]    
    
    headers = {'Content-Type': 'application/json'}
    headers['X-auth-access-token'] = fmc_info['token']
    
    json_resp = None
    try:
        r = requests.get(url, headers=headers, verify=False)
        status_code = r.status_code
        resp = r.text
        if (status_code == 200):
            logging.info("GET successful.")
            json_resp = json.loads(resp)
        else:
            r.raise_for_status()
            logging.error("Error occurred in GET: %s", resp)
    except requests.exceptions.HTTPError as err:
        logging.error("Error in connection: %s", str(err)) 
    finally:
        if r : r.close()
    return json_resp

def get_names_and_ids(fmc_info, endpoint):
    is_next = True
    url = None
    item_list = []
    while is_next:
        if url:
            full_response = get_object(fmc_info, url=url)
        else:
            full_response = get_object(fmc_info, endpoint=endpoint)
        items = full_response['items']
        for item in items:
            item_list.append({'name': item['name'], 'id': item['id'], 'type': item['type']})
        paging = full_response['paging']
        try:
            url = paging['next'][0]
        except KeyError:
            is_next = False
    return item_list
    






