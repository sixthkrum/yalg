import configparser

# name of the config file
config_file_name = 'config.ini'

# make a new config, overwrites current config
def MakeNewConfig():
    config = configparser.ConfigParser()

    config['GENERAL'] = {
        '# General settings that effect all other things': '',
        'DEVICE': '/dev/input/event4'
    }

    config['GESTURE_SWIPE_THREE_FINGER'] = {
        '# These are the minimum values that dy or/and dx must reach for an action to be executed': '',
        'DY_THRESHOLD': '0',
        'DX_THRESHOLD': '0'
    }

    config['GESTURE_SWIPE_FOUR_FINGER'] = {
        '# These are the minimum values that dy or/and dx must reach for an action to be executed': '',
        'DY_THRESHOLD': '0',
        'DX_THRESHOLD': '0'
    }
    
    with open(config_file_name, 'w') as config_file:
        config.write(config_file)


config = configparser.ConfigParser()
config.read(config_file_name)