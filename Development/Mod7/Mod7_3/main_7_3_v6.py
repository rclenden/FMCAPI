from get_7_3_v0 import get_names_and_ids
from settings_7_3_v1 import get_fmc_info
from utils_7_3_v1 import print_item_list
import constants_7_3_v1 as constants

fmc_info = get_fmc_info()
print_item_list(get_names_and_ids(fmc_info, constants.ACCESS_POLICIES))
