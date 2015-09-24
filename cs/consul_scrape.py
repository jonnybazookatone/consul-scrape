# encoding: utf-8
"""
Base file for consul scrape
"""

import json
import boto3
import config
import consulate


class ConsulScrape(object):
    """
    Class that contains the relevant methods and properties to scrape consul
    content and dump to S3. More for tidiness than anything.
    """

    s3_bucket = config.S3_BUCKET
    environment = config.ENVIRONMENT

    def __init__(self, service, **kwargs):
        """
        Constructor

        :param service: service to be scraped from consul
        """
        self.config = {}
        self.session = self.consul_session(**kwargs)
        self.service = service if isinstance(service, list) else [service]
        self.search_terms = [
            'config/{service}/{environment}'.format(
                service=service,
                environment=self.environment
            ) for service in self.service
            ]

    @staticmethod
    def consul_session(**kwargs):
        """
        Start a consul session
        :param kwargs: parameters to be passed to consulate
        :return: session to consul
        """
        return consulate.Consul(**kwargs)

    def get_config(self):
        """
        Retrieves relevant keys from the consul service
        :return: list of dictionaries
        """
        [self.config.setdefault(service, self.session.kv.find(search_term))
         for service, search_term in zip(self.service, self.search_terms)]
        return self.config

    def config_to_s3(self):
        """
        Sends the contents of config to s3 storage
        """
        s3_resource = boto3.resource('s3')
        for service in self.service:
            s3_resource.Bucket(self.s3_bucket).put_object(
                Key='{service}.config.json'.format(service=service),
                Body=json.dumps(self.config[service])
            )
