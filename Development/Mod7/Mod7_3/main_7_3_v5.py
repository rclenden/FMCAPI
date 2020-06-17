from get_7_3_v0 import get_names_and_ids
from settings_7_3_v1 import get_fmc_info
from utils_7_3_v1 import print_item_list
import configparser

fmc_info = get_fmc_info()

endpoint = 'policy/accesspolicies'
print_item_list(get_names_and_ids(fmc_info, endpoint))

endpoint = 'policy/accesspolicies/005056A4-5126-0ed3-0000-042949673459/accessrules'
print_item_list(get_names_and_ids(fmc_info, endpoint))
