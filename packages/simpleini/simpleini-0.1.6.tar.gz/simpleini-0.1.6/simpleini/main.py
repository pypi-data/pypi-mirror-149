import configparser
import os
import sys
from datetime import datetime


def logging(text):
    with open(f'{os.getcwd() + os.sep}log.txt', 'a', encoding='utf8') as log_file:
        for log_text in text.split('\n'):
            text_to_write = f'{datetime.now()} :   {log_text}\n'
            log_file.write(text_to_write)
            print(text_to_write)


class SETTINGS(object):

    def __init__(self, all_settings: str, required_fields: str):
        config_file = configparser.ConfigParser()
        path_to_settings = f'{os.getcwd() + os.sep}settings.ini'

        if not os.path.exists(path_to_settings):

            for name_setting in [i.strip() for i in all_settings.split(',')]:
                config_file['DEFAULT'][name_setting] = ''

            with open(path_to_settings, 'w', encoding='utf8') as configfile:
                config_file.write(configfile)

            logging('Settings.ini created. Please fill it and restart program.')
            sys.exit()

        else:
            result = dict()
            config_file.read(path_to_settings, encoding='utf8')
            all_keys = list(config_file['DEFAULT'].keys())
            for setting in all_settings.split(','):
                name_setting = setting.strip()
                if not name_setting in all_keys:
                    raise KeyError(f'Key [{name_setting}] not find on settings.ini')
                result[name_setting] = config_file['DEFAULT'][name_setting]

            if required_fields == 'all':
                fields_to_check = result.keys()
            else:
                fields_to_check = [i.strip() for i in required_fields.split(',')]

            for field_check in fields_to_check:
                if field_check in result and result[field_check] == '':
                    logging(f'Field [{field_check}] on settings.ini must be filled in. Please fill it and restart '
                            f'program.')
                    sys.exit()

            for key, value in result.items():
                self.__dict__[key] = value

    def __getattr__(self, name):
        return self.__dict__[name]