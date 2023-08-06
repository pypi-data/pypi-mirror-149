from ws_one_stable import settings as s
from traceback import format_exc
import re

def get_parsed_input_data(data):
    data = str(data)
    print('working with data', data)
    try:
        #data_els = data.split(' ')
        #kg_el = data_els[0]
        data = data.replace("b'", "")
        data = data.replace("$'", "")
        data = data.replace("%'", "")
        data = data.replace("=", "")
        #element = data[0]
        data = re.findall(r"\d+", data)[0]
        print('data after parse', data)
        if data.isdigit():
            return data
        else:
            print("EL", data)
    except:
        print(format_exc())
        return s.fail_parse_code



def check_scale_disconnected(data):
    return False
    # Провреят, отправлен ли бит, означающий отключение Терминала
    #return 0
