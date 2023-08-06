class UnknownTerminal(Exception):
    # Исключение, возникающее при неизвестном имени терминала
    def __init__(self):
        text = 'Такой терминал не обнаружен! Проверьте правильность набора имени, либо создайте логику для него сами'
        super().__init__(text)


def make_data_aliquot(data, value=10):
    # Сделать вес кратным value
    data = int(data)
    data = data - (data % value)
    return data

print(make_data_aliquot(1580))
