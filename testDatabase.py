import unittest
import hidden
import app_test

class TestDataBase(unittest.TestCase):

    def test_type_input(self):
        data_dict = app_test.create_dataDict_from_API()
        self.assertTrue(isinstance(data_dict, dict), 'message')

    def test_len_dict_data(self):
        data_dict = app_test.create_dataDict_from_API()
        self.assertTrue(len(data_dict) == 3, 'message')

    def test_dict_data_daily_exist(self):
        data_dict = app_test.create_dataDict_from_API()
        self.assertTrue('data_daily' in data_dict, 'message')

    def test_dict_data_hour_exist(self):
        data_dict = app_test.create_dataDict_from_API()
        self.assertTrue('data_hour' in data_dict, 'message')

    def test_dict_data_info_exist(self):
        data_dict = app_test.create_dataDict_from_API()
        self.assertTrue('data_info' in data_dict, 'message')

    def test_header_daily_columns(self):
        data_dict = app_test.create_dataDict_from_API()
        header_daily = app_test.create_header_daily(data_dict)
        self.assertTrue(len(header_daily) == 14, 'message')

    def test_data_daily_columns(self):
        data_dict = app_test.create_dataDict_from_API()
        data_daily_raw = data_dict['data_daily']
        data_daily = app_test.pull_data_daily_API(data_daily_raw)
        for row in data_daily:
            self.assertTrue(len(tuple(row)) == 14, 'message')

    def test_data_hour_columns(self):
        data_dict = app_test.create_dataDict_from_API()
        data_hour_raw = data_dict['data_hour']
        header_hour = app_test.create_header_hour(data_dict)
        data_hour = app_test.pull_data_hour_API(data_hour_raw,header_hour)
        for row in data_hour:
            self.assertTrue(len(tuple(row)) == 10, 'message')

    def test_strExe_Daily_is_str(self):
        data_dict = app_test.create_dataDict_from_API()
        header_daily = app_test.create_header_daily(data_dict)
        strExe = app_test.create_str_pull_daily_data(header_daily)
        self.assertTrue(isinstance(strExe, str), 'message')

    def test_header_hour_columns(self):
        data_dict = app_test.create_dataDict_from_API()
        header_hour = app_test.create_header_hour(data_dict)
        self.assertTrue(len(header_hour) == 10, 'message')

    def test_strExe_Hour_is_str(self):
        data_dict = app_test.create_dataDict_from_API()
        header_hour = app_test.create_header_hour(data_dict)
        strExe = app_test.create_str_pull_hour_data(header_hour)
        self.assertTrue(isinstance(strExe, str), 'message')

    def test_strExe_info_is_str(self):
        data_dict = app_test.create_dataDict_from_API()
        header_info = app_test.create_header_hour(data_dict)
        strExe = app_test.create_str_pull_info_data(header_info)
        self.assertTrue(isinstance(strExe, str), 'message')

if __name__ == '__main__':
    unittest.main()
