from get_8_4_v1 import get_names_and_ids
from settings_7_5_v0 import get_fmc_info
from utils_8_3_v1 import print_item_list
from utils_8_3_v1 import get_token
import constants_8_1_v1 as constants
from post_8_4_v2 import post
from post_8_4_v2 import post_from_file
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
    elif args.post:
        post_from_file(fmc_info, args.post)
    else:
        print('prob')
        
    logging.info('Finished execution.')

if __name__ == '__main__':
    main()