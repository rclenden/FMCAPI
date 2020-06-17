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

    post_data = {}
    # The third header determines the type of file and what is being posted
    map = {
        'Value': post_network_objects,
        'Literals': post_network_groups,
        'Port': post_protocolport_objects,
        'Objects': post_port_groups
    }
    third_header_row = ''
    file_rows = []
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        third_header_row = next(reader)[2]
        for row in reader:
            file_rows.append(row)
    map[third_header_row](fmc_info, file_rows)
    sys.exit()
    # logging.info('Posting the objects.')

def post_network_objects(fmc_info, data):

    for row in data:
        post_data = {}
        post_data['name'] = row[0]
        post_data['type'] = row[1]
        post_data['value'] = row[2]
        logging.debug('Posting: %s', json.dumps(post_data))
        post(fmc_info, constants.OBJECT_TYPE_MAP[row[1]], post_data)

def post_network_groups(fmc_info, data):
    
    #I know in advance that when I post a group that contains objects,
    #I will need to get the id and type of each object, from its name.
    #So before I start a loop, I will create a list of objects and object groups from the FMC.
    #Each object or object group will be a dictionary with name, id, and type.
    #The get_names_and_ids method will do this.
    #Since a member of a group can be a group, both objects and groups will be in one dictionary.
    fmc_object_list = get_names_and_ids(fmc_info, constants.OBJECT_NETWORK_ADDRESSES)
    fmc_object_list.extend(get_names_and_ids(fmc_info, constants.OBJECT_NETWORK_GROUPS))

    for row in data:
        post_data = {}
        literal_list_raw = []
        literal_list = []
        object_name_list = []
        object_list = []
        post_data['name'] = row[0]
        post_data['type'] = row[1]
        literals = row[2]
        objects = row[3]

        #The literals field provides a list: "10.2.3.4,10.3.4.0/24,10.3.5.7,10.4.6.0/24"
        #Or just one value: 10.2.3.4
        #Literals can be either host (10.1.1.1) or network (10.1.1.0/24)
        #Each literal must become a dictionary with type and value
        #As in {'type': 'Network', 'value': '10.2.3.0/24'}
        #First, we strip the double quotes from the ends (if any)
        literals = literals.strip('"')
        #Next, split the items into a raw list
        literal_list_raw = literals.split(',')
        # Now create a dictionary for each literal as we iterate
        for literal in literal_list_raw:
            literal_dictionary = {}
            if '/' in literal:
                literal_dictionary['type'] = 'Network'
            else:
                literal_dictionary['type'] = 'Host'
            literal_dictionary['value'] = literal
            literal_list.append(literal_dictionary)

        #The objects field provides a list of the names of the objects.
        #If multiple objects: "objectName1,objectName2"
        #Or if one object: objectName1
        #Each object name must become a dictionary with type and id
        #First, we strip the double quotes from the ends (if any)
        objects = objects.strip('"')
        #Next, split the items into a raw list
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

        post_data['literals'] = literal_list
        post_data['objects'] = object_list

        logging.debug('Posting: %s', json.dumps(post_data))
        post(fmc_info, constants.OBJECT_NETWORK_GROUPS, post_data)

def post_protocolport_objects(fmc_info, data):
    
    post_data = {}

def post_port_groups(fmc_info, data):
    
    post_data = {}