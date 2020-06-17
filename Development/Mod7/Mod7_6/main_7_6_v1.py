from get_7_6_v1 import get_names_and_ids
from settings_7_5_v0 import get_fmc_info
from utils_7_5_v0 import print_item_list
import constants_7_5_v1 as constants
import logging

logging.basicConfig(filename='application.log',level=logging.INFO)

def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logging.info('Starting the application.')

    logging.info('Retrieving the FMC info.')
    fmc_info = get_fmc_info()
    logging.info('Retrieving and printing the access policies.')
    print_item_list(get_names_and_ids(fmc_info, constants.ACCESS_POLICIES))
    
    logging.info('Finished execution.')

if __name__ == '__main__':
    main()