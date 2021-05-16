import unittest
import hidden
import app_test

class TestRequestAPI(unittest.TestCase):

    def test_url_is_not_None(self):
        #test vars
        vars = app_test.create_home_loc()
        testNone=app_test.create_url_API(vars['lan'],vars['API_KEY'],vars['location'])
        self.assertIsNotNone(testNone)

    def test_url_is_string(self):
        #test vars
        vars = app_test.create_home_loc()
        testStr=app_test.create_url_API(vars['lan'],vars['API_KEY'],vars['location'])
        self.assertTrue(isinstance(testStr, str))

    def test_requests_status(self):
        vars = app_test.create_home_loc()
        url_main = app_test.create_url_API(vars['lan'],vars['API_KEY'],vars['location'])
        response = app_test.get_response_API(url_main)

        self.assertEqual(200, response.status_code)

        



if __name__ == '__main__':
    unittest.main()
