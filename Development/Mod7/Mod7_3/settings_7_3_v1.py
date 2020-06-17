import configparser

config = configparser.RawConfigParser()
config.read('config_7_3_v1.properties')

def get_fmc_info():
    config.get('FmcInfo', 'fmc.server')
    fmc_info = {
        'server': config.get('FmcInfo', 'fmc.server'),
        'username': config.get('FmcInfo', 'fmc.username'),
        'password': config.get('FmcInfo', 'fmc.password')
    }
    return fmc_info