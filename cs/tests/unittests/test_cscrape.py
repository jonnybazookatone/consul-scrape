"""
Unit tests placeholder
"""
from cs.consul_scrape import ConsulScrape
from moto import mock_s3
from unittest import TestCase

import mock
import boto3


class TestConsulScrape(TestCase):
    """
    Unit tests for all of the main scrape methods
    """

    def setUp(self):
        """
        Generic setup of the tests
        """

        self.service = 'adsws'
        self.environment = 'staging'
        self.stub_service_payload = {
            'config/{}/{}/DEBUG'.format(self.service, self.environment): False,
            'config/{}/{}/CLIENT'.format(self.service, self.environment): {
                'TOKEN': 'we will provide an api key token for this application'
            }
        }

    def test_functional_blueprint(self):
        """
        List of entire steps need to be carried out by the consul-scraper
        """

        # Scraper pulls all the key/values from consul

        # Scraper dumps each of the key/values to S3 storage

    @mock.patch('cs.consul_scrape.consulate.Consul')
    def test_get_consul_keys_in_memory(self, mocked_class):
        """
        Tests that we can obtain the consul keys
        """

        # Mock the consulate session class
        session = mocked_class.return_value
        session.kv.find.return_value = self.stub_service_payload

        cs = ConsulScrape(service=self.service, port=8500)
        cs.get_config()

        self.assertEqual(
            cs.config[self.service].keys(),
            self.stub_service_payload.keys(),
            msg='Configuration keys do not match expected {} != {}'.format(
                cs.config,
                self.stub_service_payload
            )
        )
        self.assertAlmostEqual(
            cs.config[self.service].items(),
            self.stub_service_payload.items(),
            msg='Configuration items do not match expected {} != {}'.format(
                cs.config,
                self.stub_service_payload
            )
        )

    @mock.patch('cs.consul_scrape.consulate.Consul')
    @mock_s3
    def test_upload_consul_keys_to_s3(self, mocked_class):
        """
        Test that the key/values obtained are uploaded to s3 storage
        """

        # Mock the consulate session class
        session = mocked_class.return_value
        session.kv.find.return_value = self.stub_service_payload

        cs = ConsulScrape(service=self.service, port=8500)
        cs.get_config()

        # Setup the fake moto resources
        s3_resource = boto3.resource('s3')
        s3_resource.create_bucket(Bucket=cs.s3_bucket)

        cs.config_to_s3()

        # Check it got stored
        s3_object = s3_resource.Object(
            cs.s3_bucket,
            '{service}.config.json'.format(service=self.service)
        )

        keys = s3_object.get().keys()

        self.assertTrue(
            len(keys) > 0
        )

