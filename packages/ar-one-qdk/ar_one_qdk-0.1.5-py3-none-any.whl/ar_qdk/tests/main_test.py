from ar_qdk.main import ARQDK
import os
import unittest


class MainTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        host = os.environ.get('ar_host')
        port = os.environ.get('ar_port')
        self.qdk = ARQDK(ip=host, port=int(port))
        self.qdk.make_connection()

    def test_get_status(self):
        self.qdk.get_status()
        status = self.qdk.get_data()
        self.assertTrue(status['info'])

    def test_start_car_protocol(self):
        data = {'carnum': 'В060ХА702',
                'comm': 'test',
                'course': 'OUT',
                'car_choose_mode': 'auto'}
        self.qdk.start_car_protocol(data)
        response = self.qdk.get_data()

    def test_catch_window_switch(self):
        self.qdk.catch_window_switch(window_name='TEST')
        response = self.qdk.get_data()
        print("RESPONSE", response)

if __name__ == '__main__':
    unittest.main()
