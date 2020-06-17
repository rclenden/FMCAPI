from get_8_4_v1 import get_names_and_ids
from settings_7_5_v0 import get_fmc_info
from utils_8_3_v1 import print_item_list
from utils_8_3_v1 import get_token
import constants_8_1_v1 as constants
from post_8_4_v0 import post
import argparse
import json
import csv
import sys
import logging

def main():
    logging.basicConfig(filename='application.log', level=logging.DEBUG)
    logging.info('Starting the application.')

    logging.info('Retrieving the FMC info.')
    fmc_info = get_fmc_info()
    
    logging.debug('Getting the authentication token.')
    fmc_info['token'] = get_token(fmc_info)

    parser = argparse.ArgumentParser(description='Perform FMC API operations.')
    parser.add_argument('-g', '--get', help='get objects')
    parser.add_argument('-p', '--post', help='post objects')
    args = parser.parse_args()
    if args.get:
        print_item_list(get_names_and_ids(fmc_info, endpoint=constants.OBJECT_MAP[args.get]))
    else:
        sys.exit()
        
    logging.info('Posting the objects.')

    # post_data = {}
    # with open('nets1.csv') as csvfile:
    #     reader = csv.reader(csvfile)
    #     for row in reader:
    #         if row[1] == 'Type':
    #             continue
    #         else:
    #             post_data['name'] = row[0]
    #             post_data['type'] = row[1]
    #             post_data['value'] = row[2]

    #             logging.debug('Posting: %s', json.dumps(post_data))
    #             post(fmc_info, object_map[row[1]], post_data)
    
    #I know in advance that when I post a group that contains objects,
    #I will need to get the id and type of each object, from its name.
    #So before I start a loop, I will create a list of objects and object groups from the FMC.
    #Each object or object group will be a dictionary with name, id, and type.
    #The get_names_and_ids method will do this.
    #Since a member of a group can be a group, both objects and groups will be in one dictionary.
    fmc_object_list = get_names_and_ids(fmc_info, constants.OBJECT_NETWORK_ADDRESSES)
    fmc_object_list.extend(get_names_and_ids(fmc_info, constants.OBJECT_NETWORK_GROUPS))

    with open('NetworkGroups1.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            post_data = {}
            literal_list_raw = []
            literal_list = []
            object_name_list = []
            object_list = []
            if row[1] == 'Type':
                continue
            else:
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

    logging.info('Finished execution.')

if __name__ == '__main__':
    main()