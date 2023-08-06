""" Функции для терминала CAS"""
from ws_one_stable import settings as s


def get_parsed_input_data(data):
    data = str(data)
    try:
        data_els = data.split(',')
        kg_date = data_els[3]
        kg_els = kg_date.split(' ')
        kg_els = kg_els[:-1]
        return ''.join(kg_els)
    except:
        return s.fail_parse_code



def check_scale_disconnected(data):
    # Провреят, отправлен ли бит, означающий отключение Терминала
    return 0

