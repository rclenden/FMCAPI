import json
import sys
import requests
import csv
import constants_8_4_v1 as constants
from get_8_4_v1 import get_names_and_ids
import logging

def post(fmc_info, endpoint, post_data):

    server = fmc_info['server']
    headers = {'Content-Type': 'application/json'}
    headers['X-auth-access-token'] = fmc_info['token']
    
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
 
def post_from_file(fmc_info, file_name):
    third_header = ''
    file_rows = []
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        third_header = next(reader)[2]
        for row in reader:
            file_rows.append(row)
    THIRD_HEADER_MAP[third_header](fmc_info, file_rows)

def post_network_objects(fmc_info, data):
    for row in data:
        post_data = {}
        post_data['name'] = row[0]
        post_data['type'] = row[1]
        post_data['value'] = row[2]
        logging.debug('Posting: %s', json.dumps(post_data))
        post(fmc_info, constants.OBJECT_TYPE_MAP[row[1]], post_data)

def create_literal_list(literals):
    literal_list = []
    literals = literals.strip('"')
    literal_list_raw = literals.split(',')
    for literal in literal_list_raw:
        literal_dictionary = {}
        if '/' in literal:
            literal_dictionary['type'] = 'Network'
        else:
            literal_dictionary['type'] = 'Host'
        literal_dictionary['value'] = literal
        literal_list.append(literal_dictionary)
    return literal_list

def create_object_list(objects, fmc_object_list):
    object_list = []
    objects = objects.strip('"')
    object_name_list = objects.split(',')
    for object_name in object_name_list:
        id = ''
        type = ''
        for object in fmc_object_list:
            if object_name == object['name']:
                id = object['id']
                type = object['type']
                break
        if id == '':
            logging.error('Network object or group not found in FMC: %s', object_name)
            sys.exit('Network object or group not found in FMC')
        object_list.append({'id': id, 'type': type})
    return object_list

def post_network_groups(fmc_info, data):
    #Creating one list of FMC objects and groups for lookups of id and type from name
    fmc_object_list = get_names_and_ids(fmc_info, constants.OBJECT_NETWORK_ADDRESSES)
    fmc_object_list.extend(get_names_and_ids(fmc_info, constants.OBJECT_NETWORK_GROUPS))

    for row in data:
        post_data = {}
        object_name_list = []
        post_data['name'] = row[0]
        post_data['type'] = row[1]
        literals = row[2]
        objects = row[3]
        post_data['literals'] = create_literal_list(literals)
        post_data['objects'] = create_object_list(objects, fmc_object_list)
        logging.debug('Posting: %s', json.dumps(post_data))
        post(fmc_info, constants.OBJECT_NETWORK_GROUPS, post_data)

def post_protocolport_objects(fmc_info, data):
    pass

def post_port_groups(fmc_info, data):
    pass

# The third header in the file determines the type of file and what is being posted
THIRD_HEADER_MAP = {
        'Value': post_network_objects,
        'Literals': post_network_groups,
        'Port': post_protocolport_objects,
        'Objects': post_port_groups
}
