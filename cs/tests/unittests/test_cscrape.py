# encoding: utf-8
"""
Unit tests placeholder
"""
from cs.consul_scrape import ConsulScrape
from cs.run import run
from moto import mock_s3
from unittest import TestCase

import mock
import boto3
import cs.config as config


class BaseTest(TestCase):
    """
    Container to not repeat setup
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


class TestRun(BaseTest):
    """
    Unit tests for the run command
    """
    @mock.patch('cs.consul_scrape.consulate.Consul')
    @mock_s3
    def test_run_command(self, mocked_class):
        """
        Test the run command pulls from consul and sends to s3
        """

        # Mock the consulate session class
        session = mocked_class.return_value
        session.kv.find.return_value = self.stub_service_payload

        # Setup the fake moto resources
        s3_resource = boto3.resource('s3')
        s3_resource.create_bucket(Bucket=ConsulScrape.s3_bucket)

        # Run the command
        run(service=['adsws'])

        # Check it got stored
        s3_object = s3_resource.Object(
            ConsulScrape.s3_bucket,
            '{service}.config.json'.format(service=self.service)
        )

        keys = s3_object.get().keys()

        self.assertTrue(
            len(keys) > 0
        )


class TestConsulScrape(BaseTest):
    """
    Unit tests for all of the main scrape methods
    """

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


class TestConfig(TestCase):
    """
    Dummy test case for config file
    """

    def test_values(self):
        """
        Test contains relevant values
        """

        self.assertIsInstance(config.CS_LOGGING, dict)
        self.assertIsInstance(config.S3_BUCKET, basestring)
        self.assertIsInstance(config.ENVIRONMENT, basestring)
        self.assertEqual(config.ENVIRONMENT, 'staging')
