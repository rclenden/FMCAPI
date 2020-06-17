from get_7_6_v1 import get_names_and_ids
from settings_7_5_v0 import get_fmc_info
from utils_7_5_v0 import print_item_list
import constants_8_1_v1 as constants
from post_8_2_v1 import post
import json
import logging

def main():
    logging.basicConfig(filename='application.log', level=logging.INFO)
    logging.info('Starting the application.')

    logging.info('Retrieving the FMC info.')
    fmc_info = get_fmc_info()
    
    post_data = {
        "name": "TestNetwork7",
        "type": "Network",
        "value": "10.1.2.0/24"
    }

    logging.info('Posting the network object.')
    post(fmc_info, constants.OBJECT_NETWORKS, post_data)
    
    logging.info('Finished execution.')

if __name__ == '__main__':
    main()