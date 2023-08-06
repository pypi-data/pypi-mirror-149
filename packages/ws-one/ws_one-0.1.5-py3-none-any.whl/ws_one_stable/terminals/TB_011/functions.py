""" Функции для терминала CAS"""
from ws_one_stable import settings as s
import re

def get_parsed_input_data(data):
    data = str(data)
    try:
        #return data.split('=')[1].split('$')[0].strip()
        return re.findall(r'\d+', data)[0]
    except:
        return s.fail_parse_code


def check_scale_disconnected(data):
    # Провреят, отправлен ли бит, означающий отключение Терминала
    return 0

