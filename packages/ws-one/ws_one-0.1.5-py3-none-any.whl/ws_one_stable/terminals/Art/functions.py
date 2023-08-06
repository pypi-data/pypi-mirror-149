""" Функции для терминала CAS"""
from ws_one_stable import settings as s


def get_parsed_input_data(data):
    data = str(data)
    try:
        data = data[1:-2].replace('\\r', '')
        data = data.replace("'", "")
        return data
    except:
        return s.fail_parse_code


def check_scale_disconnected(data):
    # Провреят, отправлен ли бит, означающий отключение Терминала
    return 0
