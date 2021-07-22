import unittest

from clico.utils import validate_url


class TestUtils(unittest.TestCase):
    def test_validate_url(self):
        self.assertTrue(validate_url(s='https://google.com'))
        self.assertTrue(validate_url(s='http://8.8.8.8'))

        with self.assertRaises(ValueError) as ctx:
            validate_url(s='_invalid_url_')

        self.assertTrue(str(ctx.exception) == 'Invalid value `_invalid_url_`')
