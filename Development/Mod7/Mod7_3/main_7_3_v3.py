from get_7_3_v0 import get_names_and_ids
from settings_7_3_v1 import get_fmc_info
import configparser

fmc_info = get_fmc_info()

endpoint = 'policy/accesspolicies'
item_list = get_names_and_ids(fmc_info, endpoint)
for item in item_list:
    print(f'{item["name"]}   {item["id"]}')

endpoint = 'policy/accesspolicies/005056A4-5126-0ed3-0000-042949673459/accessrules'
item_list = get_names_and_ids(fmc_info, endpoint)
for item in item_list:
    print(f'{item["name"]}   {item["id"]}') 

