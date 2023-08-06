from ws_one_stable.main import WeightSplitter


ws = WeightSplitter('0.0.0.0', 2279, port_name='COM2')
ws.get_all_connected_devices()
ws.start()