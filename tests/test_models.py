import json
import unittest
from enum import EnumMeta

from pydantic import ValidationError

from clico import Clico
from clico.models import Result, Error, Domain, Integration, Link


class TestModels(unittest.TestCase):
    def setUp(self):
        self.clico = Clico(api_key='api_key')

    def test_result_model(self):
        properties = json.loads(Result.schema_json()).get('properties')

        self.assertEqual(len(properties), 1)
        self.assertIn('result', properties)
        self.assertIn('anyOf', properties.get('result'))
        self.assertTupleEqual(('string', 'array'), tuple(x.get('type') for x in properties.get('result').get('anyOf')))

    def test_error_model(self):
        properties = json.loads(Error.schema_json()).get('properties')

        self.assertEqual(len(properties), 5)
        self.assertIn('status', properties)
        self.assertIn('timestamp', properties)
        self.assertIn('error', properties)
        self.assertIn('message', properties)
        self.assertIn('path', properties)
        self.assertEqual(properties.get('status').get('type'), 'integer')
        self.assertEqual(properties.get('timestamp').get('type'), 'string')
        self.assertEqual(properties.get('timestamp').get('format'), 'date-time')
        self.assertEqual(properties.get('error').get('type'), 'string')
        self.assertEqual(properties.get('message').get('type'), 'string')
        self.assertEqual(properties.get('path').get('type'), 'string')
        self.assertTupleEqual(('status',), tuple(json.loads(Error.schema_json()).get('required')))
        self.assertIn('timestamp', Error.__validators__)

    def test_domain_model(self):
        self.assertIsInstance(Domain, EnumMeta)
        self.assertEqual(len(tuple(map(str, Domain))), 30)
        self.assertEqual(Domain.CLI_CO, 'cli.co')

    def test_integration_model(self):
        properties = json.loads(Integration.schema_json()).get('properties')

        self.assertEqual(len(properties), 4)
        self.assertIn('callback_uri', properties)
        self.assertIn('redirect_uri', properties)
        self.assertIn('user_data', properties)
        self.assertIn('token', properties)
        self.assertEqual(properties.get('callback_uri').get('type'), 'string')
        self.assertEqual(properties.get('redirect_uri').get('type'), 'string')
        self.assertEqual(properties.get('user_data').get('type'), 'object')
        self.assertEqual(properties.get('token').get('type'), 'string')

    def test_link_model(self):
        properties = json.loads(Link.schema_json()).get('properties')

        self.assertEqual(len(properties), 13)
        self.assertTupleEqual(('*', 'callback_url', 'target_url'),
                              tuple(sorted([k for k, v in Link.__validators__.items()])))
        self.assertIn('target_url', properties)
        self.assertIn('domain', properties)
        self.assertIn('is_deep', properties)
        self.assertIn('id_campaign', properties)
        self.assertIn('right_side', properties)
        self.assertIn('utm_phone', properties)
        self.assertIn('utm_source', properties)
        self.assertIn('utm_medium', properties)
        self.assertIn('utm_campaign', properties)
        self.assertIn('utm_content', properties)
        self.assertIn('utm_term', properties)
        self.assertIn('callback_url', properties)
        self.assertIn('short_link', properties)

        with self.assertRaises(ValidationError) as ctx:
            Link(**{})

        self.assertIsInstance(ctx.exception, ValidationError)
        self.assertTupleEqual(ctx.exception.errors()[0].get('loc'), ('target_url',))
