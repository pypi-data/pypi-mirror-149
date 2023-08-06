from pds_one.main import PortDataSplitter
from ws_one_stable import support_functions as sup_func
from traceback import format_exc
import ws_one_stable.settings as s


class WeightSplitter(PortDataSplitter):
    def __init__(self, ip, port, port_name='/dev/ttyUSB0', terminal_name='CAS',
                 debug=False, scale_protocol=None):
        super().__init__(ip, port, port_name, device_name=terminal_name,
                         debug=debug, scale_protocol=scale_protocol)
        self.terminal_name = terminal_name
        self.terminal_funcs = sup_func.extract_terminal_func(
            self.terminal_name)
        self.start_weight = 0

    def set_stable_wight(self, start_weight):
        self.start_weight = start_weight

    def upd_stable_weight(self, new_weight):
        self.start_weight += new_weight
        self.start_weight = self.make_data_aliquot(self.start_weight)

    def make_data_aliquot(self, data, value=10):
        # Сделать вес кратным value
        try:
           data = int(data)
           data = data - (data % value)
        except:
            self.show_print(format_exc())
        return data

    def stable_weight(self, data):
        try:
            data = int(data)
            data -= self.start_weight
            return data
        except:
            print(format_exc())
            return data

    def check_data(self, data):
        # Проверить данные, вызывал функцию этого терминала
        if self.terminal_funcs.check_scale_disconnected(data):
            data = s.scale_disconnected_code
        else:
            data = self.terminal_funcs.get_parsed_input_data(data)
            data = self.stable_weight(data)
        return data

    def send_data(self, data, **kwargs):
        # Отправить данные
        data = str(data)
        try:
            data = bytes(data, encoding='utf-8')
            self.show_print('Sending:', data, debug=True)
            super().send_data(data, **kwargs)
        except TypeError:
            self.show_print("Reconnecting...", debug=True)
            self.reconnect_logic()
