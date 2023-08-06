""" Функции для терминала CAS"""
from ws_one_stable import settings as s


def get_parsed_input_data(data):
    data = str(data)
    return data


def check_scale_disconnected(data):
    # Провреят, отправлен ли бит, означающий отключение Терминала
    return False