from get_7_6_v1 import get_names_and_ids
from settings_7_5_v0 import get_fmc_info
from utils_8_3_v1 import print_item_list
from utils_8_3_v1 import get_token
import constants_8_1_v1 as constants
from post_8_3_v1 import post
import json
import csv
import logging

def main():
    logging.basicConfig(filename='application.log', level=logging.DEBUG)
    logging.info('Starting the application.')

    logging.info('Retrieving the FMC info.')
    fmc_info = get_fmc_info()
    
    logging.debug('Getting the authentication token.')
    fmc_info['token'] = get_token(fmc_info)

    logging.info('Posting the objects.')

    object_map = {
        'Network': constants.OBJECT_NETWORKS,
        'Range': constants.OBJECT_RANGES,
        'Host': constants.OBJECT_HOSTS
    }

    post_data = {}
    with open('nets1.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[1] == 'Type':
                continue
            else:
                post_data['name'] = row[0]
                post_data['type'] = row[1]
                post_data['value'] = row[2]

                logging.debug('Posting: %s', json.dumps(post_data))
                post(fmc_info, object_map[row[1]], post_data)
    
    logging.info('Finished execution.')

if __name__ == '__main__':
    main()