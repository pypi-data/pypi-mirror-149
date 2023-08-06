""" Функции для терминала CAS"""
from ws_one_stable import settings as s


def get_parsed_input_data(data):
    data = str(data)
    try:
        data_els = data.split(' ')
        kg_el = data_els[0]
        element = kg_el.replace('ww', '')
        element = element.replace("b'", "")
        if element.startswith('-'):
            element = element.replace('-', '')
        if element.isdigit():
            return str(int(element))
        else:
            print('Returning None', element)
    except:
        return s.fail_parse_code



def check_scale_disconnected(data):
    # Провреят, отправлен ли бит, означающий отключение Терминала
    return 0

