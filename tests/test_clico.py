from unittest import mock, TestCase

from clico import Clico
from clico.models import Domain, Link, Error, Result, Integration


class TestClico(TestCase):
    def setUp(self):
        self.clico = Clico(api_key='api_key')
        self.valid_link = {
            'domain': Domain.CLI_CO,
            'target_url': 'https://google.com',
            'callback_url': 'https://my-api.com/callback',
            'is_deep': False,
            'id_campaign': 'my-campaign',
            'utm_phone': 'XXXXXXXXXXX',
        }
        self.valid_integration = {
            'callback_uri': 'https://my-api.com/callback',
            'redirect_uri': 'https://google.com',
            'user_data': {
                'key': 'value'
            }
        }

    def test_empty_api_key(self):
        with self.assertRaises(ValueError) as ctx:
            Clico()
        self.assertTrue(str(ctx.exception) == 'API key is required')

    def test_single_link_assertion_failed(self):
        with self.assertRaises(AssertionError) as ctx:
            self.clico.single_link('')
        self.assertEqual(str(ctx.exception), 'Type `str` is not an instance of `Link` object')

    @mock.patch("clico.clico.requests.post")
    def test_single_link_success(self, mock_post):
        fake_short_url = 'https://cli.co/GHk7c'
        mock_response = mock.Mock(status_code=200)
        mock_response.json.return_value = {
            "result": fake_short_url
        }
        mock_post.return_value = mock_response

        single_link = self.clico.single_link(Link(**self.valid_link))
        self.assertIsInstance(single_link, Link)
        self.assertEqual(single_link.short_link, fake_short_url)

    @mock.patch("clico.clico.requests.post")
    def test_single_link_failed(self, mock_post):
        mock_response = mock.Mock(status_code=400)
        mock_response.json.return_value = {
            "status": 400
        }
        mock_post.return_value = mock_response

        single_link = self.clico.single_link(Link(**self.valid_link))
        self.assertIsInstance(single_link, Error)

    def test_multiple_links_assertion_failed(self):
        with self.assertRaises(AssertionError) as ctx:
            self.clico.multiple_links('')
        self.assertEqual(str(ctx.exception), 'Type `str` is not an instance of `list` object')

    @mock.patch("clico.clico.requests.post")
    def test_multiple_links_success(self, mock_post):
        fake_result = Result(result=['https://cli.co/GHk7c', 'https://vk.in/GHk7c'])

        mock_response = mock.Mock(status_code=200)
        mock_response.json.return_value = fake_result.dict()
        mock_post.return_value = mock_response

        multiple_links = self.clico.multiple_links([
            Link(**self.valid_link),
            Link(**self.valid_link)
        ])
        self.assertIsInstance(multiple_links, list)
        self.assertEqual(len(multiple_links), 2)
        self.assertIsInstance(multiple_links[0], Link)
        self.assertEqual(multiple_links[0].short_link, 'https://cli.co/GHk7c')
        self.assertNotEqual(multiple_links[1].short_link, 'https://cli.co/GHk7c')

    @mock.patch("clico.clico.requests.post")
    def test_multiple_links_failed(self, mock_post):
        mock_response = mock.Mock(status_code=400)
        mock_response.json.return_value = {
            "status": 400
        }
        mock_post.return_value = mock_response

        multiple_links = self.clico.multiple_links([
            Link(**self.valid_link),
            Link(**self.valid_link)
        ])
        self.assertIsInstance(multiple_links, Error)

    def test_integration_assertion_failed(self):
        with self.assertRaises(AssertionError) as ctx:
            self.clico.integration('')
        self.assertEqual(str(ctx.exception), 'Type `str` is not an instance of `Integration` object')

    @mock.patch("clico.clico.requests.post")
    def test_integration_success(self, mock_post):
        token = 'https://my.cli.com/?token=c2c31eca-b7e0-4a73-85a4-6e0975b81d76'
        fake_result = Result(result=token)

        mock_response = mock.Mock(status_code=200)
        mock_response.json.return_value = fake_result.dict()
        mock_post.return_value = mock_response

        integration = self.clico.integration(Integration(**self.valid_integration))
        self.assertEqual(integration.token, token)

    @mock.patch("clico.clico.requests.post")
    def test_integration_failed(self, mock_post):
        mock_response = mock.Mock(status_code=400)
        mock_response.json.return_value = {
            "status": 400
        }
        mock_post.return_value = mock_response

        multiple_links = self.clico.integration(Integration(**self.valid_integration))
        self.assertIsInstance(multiple_links, Error)
