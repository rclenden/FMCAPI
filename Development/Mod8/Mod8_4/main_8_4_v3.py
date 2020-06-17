from get_8_4_v1 import get_names_and_ids
from settings_7_5_v0 import get_fmc_info
from utils_8_3_v1 import print_item_list
from utils_8_3_v1 import get_token
import constants_8_1_v1 as constants
from post_8_4_v3 import post
from post_8_4_v3 import post_from_file
import argparse
import json
import csv
import sys
import logging

def get_fmc_information():
    logging.info('Retrieving the FMC info.')
    fmc_info = get_fmc_info()
    logging.debug('Getting the authentication token.')
    fmc_info['token'] = get_token(fmc_info)
    return fmc_info


def get_arguments():
    arguments = {}
    parser = argparse.ArgumentParser(description='Perform FMC API operations.')
    parser.add_argument('-g', '--get', help='GET objects: Networks, Hosts, etc.')
    parser.add_argument('-p', '--post', help='POST objects from a CSV')
    args = parser.parse_args()
    if args.get:
        arguments['get'] = args.get
    if args.post:
        arguments['post'] = args.post
    if not arguments:
        logging.error('Command line missing --get or --post')
        parser.print_help(sys.stderr)
        sys.exit(1)
    return arguments

def main():
    logging.basicConfig(filename='application.log', level=logging.DEBUG)
    logging.info('Starting the application.')

    fmc_info = get_fmc_information()
    arguments = get_arguments()
    if 'get' in arguments:
        fmc_endpoint = constants.OBJECT_MAP[arguments['get']]
        print_item_list(get_names_and_ids(fmc_info, endpoint=fmc_endpoint))
    if 'post' in arguments:
        post_from_file(fmc_info, arguments['post'])
        
    logging.info('Finished execution.')

if __name__ == '__main__':
    main()